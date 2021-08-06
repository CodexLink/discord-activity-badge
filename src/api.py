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

# For Commiting the Changes: https://docs.github.com/en/rest/reference/repos#create-or-update-file-contents
# For Fetching the File:

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
        self.is_auth: bool = False
        self._request_iterator: list[
            Any
        ] = []  # # Subject for removal in Post-Development.

        self.logger.info("ClientSession for API Requests has been instantiated.")

        super().__init__()
        self.logger.info(
            f"Instantiatied Discord Client with the following intents={DISCORD_CLIENT_INTENTS=}"
        )

        self.logger.info(
            f"{AsyncGithubAPI.__name__} is done initializing other elements."
        )

    async def exec_api_actions(
        self,
        action: GithubRunnerActions,
        data: Union[
            Optional[BadgeStructure], Optional[Base64String]
        ] = None,  # ! I don't know if this should be okay.
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
                    "readme" if action is GithubRunnerActions.FETCH_README else "contents/",
                )
            )

            while True:
                http_request: ClientResponse = await self._request(repo_path, action)

                try:
                    if http_request.ok:

                        if action is GithubRunnerActions.FETCH_README:
                            # * Give user an option whether we want to decode the b64 or not.
                            __read_resp: bytes = http_request.content.read_nowait()
                            __serialized_resp: dict = literal_eval(
                                __read_resp.decode("utf-8")
                            )

                            __sresp_content: Base64String = __serialized_resp[
                                "content"
                            ].replace("\n", "")

                            self.logger.info(
                                f"Github Profile ({user_repo}) README has been fetched."
                            )

                            return __sresp_content

                        elif action is GithubRunnerActions.COMMIT_CHANGES and data is Base64String(data):  # type: ignore
                            pass

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
        rest_response: GithubRunnerActions,
        should_return: ResponseTypes = ResponseTypes.RESPONSE,
    ) -> Union[
        list[Union[HttpsURL, ClientResponseOK, ClientResponseStatus]], ClientResponse
    ]:
        if rest_response in GithubRunnerActions:
            self.logger.info(
                (
                    "Attempting to Fetch README on {0}/{0} from Github API ({1})".format(
                        self.envs["GITHUB_ACTOR"], url
                    )
                    if rest_response is GithubRunnerActions.FETCH_README
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

            http_request: ClientResponse = await getattr(
                self._api_session,
                "get" if rest_response is GithubRunnerActions.FETCH_README else "put",
            )(url, allow_redirects=True, **extra_contents)

            req_cost: str = "Requests Left over Rate Limit: {0}/{1}".format(
                http_request.headers["X-RateLimit-Remaining"],
                http_request.headers["X-RateLimit-Limit"],
            )

            if not self.is_auth:
                if http_request.ok:
                    self.logger.info("Authenticated in Github API! %s." % req_cost)

                    if http_request.headers["Vary"].__contains__(
                        "Authorization"
                    ) and bool(http_request.headers.get("X-OAuth-Scopes")):
                        self.is_auth = True
                else:
                    self.logger.debug(req_cost)

        else:
            self.logger.critical(
                f"Enums invoked ({rest_response.name}) is invalid. Please report this to the developer."
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

        # ! These returns are implemented for future projects.
        if should_return is ResponseTypes.IS_OKAY:
            return [url, ClientResponseOK(http_request.ok)]

        elif should_return is ResponseTypes.RESPONSE_STATUS:
            return [url, ClientResponseStatus(http_request.status)]

        elif should_return is ResponseTypes.RESPONSE:
            return http_request

        else:
            self.logger.critical(
                "Specified `should_return` is invalid or haven't implemented yet. Please check the function for more information."
            )
            exit(-1)
