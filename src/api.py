"""
Copyright 2021 Janrey "CodexLink" Licas

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

	http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.


# This is potential rewrite for PyGithub, which makes it async.
"""

if __name__ == "__main__":
    from elements.exceptions import IsolatedExecNotAllowed

    raise IsolatedExecNotAllowed

from os import _exit as exit
from ast import literal_eval
from asyncio import (
    Future,
    Task,
    as_completed,
    create_task,
    sleep as asyncio_sleep,
    wait,
)
from base64 import b64decode, b64encode
from json import load as JSON_SERIALIZE
from typing import Any, Coroutine, Optional, Tuple, Union

from aiohttp import BasicAuth, ClientResponse, ClientSession

from elements.constants import (
    DISCORD_CLIENT_INTENTS,
    GithubRunnerActions,
    ResponseTypes,
)
from elements.exceptions import (
    SessionRequestHTTPError,
    SessionRequestStatusAssertFailed,
)
from elements.typing import (
    BadgeStructure,
    Base64Bytes,
    Base64String,
    ClientResponseOK,
    ClientResponseStatus,
    HttpsURL,
    HttpsURLPath,
    ResolvedClientResponse,
    ResponseJson,
)
from logging import Logger


class AsyncGithubAPI:
    # * The following variables are declared since there's no typing hint inheritance.
    logger: Logger
    envs: Any

    """
	A set of async functions that handles API handler. This includes Github API and Badgen API.
	The class has the prefix "Static" because of its inability to register other APIs during Runtime.
	I didn't designed the Class to be dynamic but it can be possible for future use. Keep note of other function
	raising 'NotImplemented'.
	"""

    async def __ainit__(self) -> None:

        self._api_session: ClientSession = ClientSession()
        self.logger.info("ClientSession for API Requests has been instantiated.")

        super().__init__()
        self.logger.info(
            f"Discord Client Instantiatied with intents={DISCORD_CLIENT_INTENTS=}"
        )

        self.logger.info(
            f"{AsyncGithubAPI.__name__} is done initializing other elements."
        )

    async def exec_api_actions(
        self,
        action: GithubRunnerActions,
        data: list[str, Union[Optional[BadgeStructure], Optional[Base64String]]] = None,
    ) -> Union[Any, ResolvedClientResponse, Base64Bytes]:

        # TODO: Check what to try-catch here.

        # First, we go through mutliple if statements to queue those requests up.
        # Second, we have an iterator that process those.

        # Before, a ClientResponse Type.

        ### DISCLAIMER
        # ! Starting at this point, until EOF, changes may be done during post-development.
        # ! I'm taking so much time to see the difference about these two and how to adjust other async tasks.

        if action in GithubRunnerActions:
            user_repo = (
                "{0}/{0}".format(self.envs["GITHUB_ACTOR"])
                if self.envs["PROFILE_REPOSITORY"] is None
                else "{0}".format(self.envs["PROFILE_REPOSITORY"])
            )
            repo_path: HttpsURL = HttpsURL(
                "{0}/repos/{1}/{2}".format(
                    self.envs["GITHUB_API_URL"],
                    user_repo,
                    "readme"
                    if action is GithubRunnerActions.FETCH_README
                    else "contents/README.md",  # # !A
                )
            )

            while True:
                http_request: ClientResponse = await self._request(
                    repo_path, action, data=data if data is not None else None
                )

                try:
                    if http_request.ok:

                        suffix_req_cost: str = "Request Used over Remaining (%s/%s)" % (
                            http_request.headers["X-RateLimit-Remaining"],
                            http_request.headers["X-RateLimit-Limit"],
                        )
                        if action is GithubRunnerActions.FETCH_README:
                            # * Give user an option whether we want to decode the b64 or not.
                            __read_resp: bytes = http_request.content.read_nowait()

                            __serialized_resp: dict = literal_eval(
                                __read_resp.decode("utf-8")
                            )

                            self.logger.info(
                                f"Github Profile ({user_repo}) README has been fetched. | {suffix_req_cost}"
                            )

                            return [
                                __serialized_resp["sha"],
                                Base64String(
                                    __serialized_resp["content"].replace("\n", "")
                                ),
                            ]  # todo: Change the return type of the function later!

                        elif action is GithubRunnerActions.COMMIT_CHANGES and data is Base64String(data):  # type: ignore
                            self.logger.info(
                                f"README Changes from ({user_repo}) has been pushed through! | {suffix_req_cost}"
                            )
                            break

                    else:
                        self.logger.warn(
                            "Conditions not met, continuing again after 3 seconds (as a penalty)."
                        )
                        await asyncio_sleep(0.6)

                except SyntaxError as RecvCtx:
                    self.logger.error(
                        f"Fetched Data is either incomplete or malformed. Attempting to re-fetch... | Info: {RecvCtx}"
                    )

                    await asyncio_sleep(0.6)
                    continue

                except KeyError as RecvCtx:  # todo: Create an exception for this one. GithubAPIRateLimited
                    if __serialized_resp["message"].startswith(
                        "API rate limit exceeded"
                    ):
                        self.logger.critical(
                            f"Request accepted but you are probably rate-limited by Github API. Did you keep on retrying or you are over-committing changes? | More Info: {RecvCtx}"
                        )
                        exit(-1)

        else:  # todo: Annotate this later.
            self.logger.critical(f"action is {action.name}")
            exit(0)

    async def _request(
        self,
        url: HttpsURL,
        action_type: GithubRunnerActions,
        data: Optional[list[Union[Base64String, str]]] = None,
    ) -> Union[
        list[Union[HttpsURL, ClientResponseOK, ClientResponseStatus]], ClientResponse
    ]:
        if action_type in GithubRunnerActions:
            self.logger.info(
                (
                    "Attempting to Fetch README on {0}/{0} from Github API ({1})".format(
                        self.envs["GITHUB_ACTOR"], url
                    )
                    if action_type is GithubRunnerActions.FETCH_README
                    else "Attempting to Commit Changes of README from Github API >>> {0}/{0} ({1})".format(
                        self.envs["GITHUB_ACTOR"], url
                    )
                )
                if GithubRunnerActions.COMMIT_CHANGES
                else "This might be invalid!"
            )

            extra_contents: dict[str, Union[dict[str, str], BasicAuth]] = {
                "headers": {"Accept": "application/vnd.github.v3+json"},
                "auth": BasicAuth(
                    self.envs["GITHUB_ACTOR"], self.envs["WORKFLOW_TOKEN"]
                ),
            }

            data_context: Union[HttpsURL, ResponseJson] = (
                {
                    "content": data[1].decode("utf-8") if data is not None else None,
                    "message": self.envs["COMMIT_MESSAGE"],
                    "sha": data[0] if data is not None else None,
                    "committer": {
                        "name": "Discord Activity Badge",
                        "email": "discord_activity@discord_bot.com",
                    },
                }
                if action_type is GithubRunnerActions.COMMIT_CHANGES
                else {}
            )

            http_request: ClientResponse = await getattr(
                self._api_session,
                "get" if action_type is GithubRunnerActions.FETCH_README else "put",
            )(url, json=data_context, allow_redirects=False, **extra_contents)

        else:
            self.logger.critical(
                f"Enums invoked ({action_type.name}) is invalid. Please report this to the developer."
            )
            exit(-1)

        if (
            not http_request.ok
        ):  # todo: Make this clarified or confirmed. We don't have a case to where we can see this in action.

            # ! Sometimes, we can exceed the rate-limit request per time. We have to handle the display error instead from the receiver of this request.

            _resp_raw: ClientResponse = http_request  # Supposed to be ClientResponse
            _resp_ctx: dict = literal_eval(str(_resp_raw))

            self.logger.debug(_resp_ctx)
            # raise SessionRequestStatusAssertFailed(_http_request.response)

        else:
            return http_request
