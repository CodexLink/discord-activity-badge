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
"""

if __name__ == "__main__":
    from elements.exceptions import IsolatedExecNotAllowed

    raise IsolatedExecNotAllowed

from ast import literal_eval
from asyncio import sleep
from logging import Logger
from os import _exit as terminate
from typing import Any, Optional, Union

from aiohttp import BasicAuth, ClientResponse, ClientSession

from elements.constants import (
    COMMIT_REQUEST_PAYLOAD,
    DISCORD_CLIENT_INTENTS,
    REQUEST_HEADER,
    ExitReturnCodes,
    GithubRunnerActions,
)
from elements.typing import (
    Base64String,
    HttpsURL,
    READMEContent,
    READMEIntegritySHA,
    READMERawContent,
)


class AsyncGithubAPILite:
    # * The following variables are declared for weak reference since there's no hint-typing inheritance.

    envs: Any
    logger: Logger

    """
    This child class is a scratch implementation based from Github API. It was supposed to be a re-write implementation of PyGithub for async,
    but I just realized that I only need some certain components. This class also contains session for all HTTPS requests and that includes Badgen.
	"""

    async def __ainit__(self) -> None:
        """
        Asynchronous init for instantiating other classes, if there's another one behind the MRO, which is the DiscordClientHandler.
        This also instantiates aiohttp.ClientSession for future requests.
        """

        self._api_session: ClientSession = ClientSession()
        self.logger.info("ClientSession for API Requests has been instantiated.")

        super().__init__()
        self.logger.info(
            f"Discord Client Instantiatied with intents={DISCORD_CLIENT_INTENTS=}"
        )

        self.logger.info(
            f"{AsyncGithubAPILite.__name__} is done initializing other elements."
        )

    async def exec_api_actions(
        self,
        action: GithubRunnerActions,
        data: Optional[list[Union[READMEIntegritySHA, READMERawContent]]] = None,
    ) -> Union[None, list[Union[READMEIntegritySHA, Base64String]]]:
        """
        A method that handles every possible requests by packaging required components into one. This was done so that we only have to call the method without worrying anything.

        Args:
            action (GithubRunnerActions): The action to perform. Choices should be FETCH_README and COMMIT_CHANGES.
            data (Optional[list[tuple[READMEIntegritySHA, READMERawContent]]] , optional): The data required for COMMIT_CHANGES.
            Basically it needs the old README SHA integrity and the new README in the form of Base64 (READMERawContent). Defaults to None.

        Returns:
            Union[None, list[Union[READMEIntegritySHA, Base64String]]]: This expects to return a list of READMEIntegritySHA and Base64 straight from b64decode or None.
        """

        if action in GithubRunnerActions:
            # We setup paths for HttpsURL with the use of these two varaibles.
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
                    else "contents/README.md",
                )
            )

            # When making requests, we might want to loop whenever the data that we receive is malformed or have failed to send.
            while True:
                http_request: ClientResponse = await self._request(
                    repo_path, action, data=data if data is not None else None
                )

                try:
                    if http_request.ok:
                        suffix_req_cost: str = (
                            "Remaining Requests over Rate-Limit (%s/%s)"
                            % (
                                http_request.headers["X-RateLimit-Remaining"],
                                http_request.headers["X-RateLimit-Limit"],
                            )
                        )

                        # For this action, decode the README (base64) in utf-8 (str) then sterilized unnecessary newline.
                        if action is GithubRunnerActions.FETCH_README:
                            read_response: bytes = http_request.content.read_nowait()
                            serialized_response: dict = literal_eval(
                                read_response.decode("utf-8")
                            )

                            self.logger.info(
                                f"Github Profile ({user_repo}) README has been fetched. | {suffix_req_cost}"
                            )
                            return [
                                serialized_response["sha"],
                                Base64String(
                                    serialized_response["content"].replace("\n", "")
                                ),
                            ]

                        # Since we commit and there's nothing else to modify, just output that the request was success.
                        elif action is GithubRunnerActions.COMMIT_CHANGES and data is Base64String(data):  # type: ignore # It explicitly wants to typecast `str`, which renders the condition false.
                            self.logger.info(
                                f"README Changes from ({user_repo}) has been pushed through! | {suffix_req_cost}"
                            )
                            return None

                    # If any of those conditions weren't met, retry again.
                    else:
                        self.logger.warning(
                            "Conditions were not met, continuing again after 3 seconds (as a penalty)."
                        )
                        await sleep(0.6)
                        continue

                # Same for this case, but we assert that the data received is malformed.
                except SyntaxError as e:
                    self.logger.error(
                        f"Fetched Data is either incomplete or malformed. Attempting to re-fetch... | Info: {e} at line {e.__traceback__.tb_lineno}." # type: ignore
                    )

                    await sleep(0.6)
                    continue

                # Whenever we tried too much, we don't know if we are rate-limited, because the request will make the ClientResponse.ok set to True.
                # So for this case, we special handle it by identifying the message.
                except KeyError as e:
                    if serialized_response["message"].startswith(
                        "API rate limit exceeded"
                    ):
                        self.logger.critical(
                            f"Request accepted but you are probably rate-limited by Github API. Did you keep on retrying or you are over-committing changes? | More Info: {e} at line {e.__traceback__.tb_lineno}." # type: ignore
                        )
                        terminate(ExitReturnCodes.RATE_LIMITED_EXIT)

        else:
            self.logger.critical(
                f"The given value on `action` parameter is invalid! Ensure that the `action` is `{GithubRunnerActions}`!"
            )
            terminate(ExitReturnCodes.ILLEGAL_CONDITION_EXIT)

    async def _request(
        self,
        url: HttpsURL,
        action_type: GithubRunnerActions,
        data: Optional[list[Union[READMEIntegritySHA, READMERawContent]]] = None,
    ) -> ClientResponse:
        """
        An inner-private method that handles the requests by using packaged header and payload, necessarily for requests.

        Args:
            url (HttpsURL): The URL String to make Request.
            action_type (GithubRunnerActions): The type of action that is recently passed on `exec_api_actions().`
            data (Optional[list[Union[READMEIntegritySHA, READMERawContent]]], optional): The argument given in `exec_api_actions()`, now handled in this method.. Defaults to None.

        Returns:
            ClientResponse: The raw response given by the aiohttp.REST_METHODS. Returned without modification to give the receiver more options.
        """

        if action_type in GithubRunnerActions:
            self.logger.info(
                (
                    "Attempting to Fetch README from Github API <<< {0}/{0} ({1})".format(
                        self.envs["GITHUB_ACTOR"], url
                    )
                    if action_type is GithubRunnerActions.FETCH_README
                    else "Attempting to Commit Changes of README from Github API >>> {0}/{0} ({1})".format(
                        self.envs["GITHUB_ACTOR"], url
                    )
                )
                if GithubRunnerActions.COMMIT_CHANGES
                else None
            )

            # # This dictionary is applied when GithubRunnerActions.COMMIT_CHANGES was given in parameter `action`.
            extra_contents: REQUEST_HEADER = {
                "headers": {"Accept": "application/vnd.github.v3+json"},
                "auth": BasicAuth(
                    self.envs["GITHUB_ACTOR"], self.envs["WORKFLOW_TOKEN"]
                ),
            }

            # # This dictionary is applied when GithubRunnerActions.COMMIT_CHANGES was given in parameter `action`.
            data_context: COMMIT_REQUEST_PAYLOAD = (
                {
                    "content": READMEContent(bytes(data[1]).decode("utf-8")) if data is not None else None,  # type: ignore # Keep in mind that the type-hint is already correct, I don't know what's the problem.]
                    "message": self.envs["COMMIT_MESSAGE"],
                    "sha": READMEIntegritySHA(str(data[0]))
                    if data is not None
                    else None,
                    "committer": {
                        "name": "Discord Activity Badge",
                        "email": "discord_activity@discord_bot.com",
                    },
                }
                if action_type is GithubRunnerActions.COMMIT_CHANGES
                else {
                    "content": READMEContent(""),
                    "message": "",
                    "sha": READMEIntegritySHA(""),
                    "committer": {"name": "", "email": ""},
                }
            )

            http_request: ClientResponse = await getattr(
                self._api_session,
                "get" if action_type is GithubRunnerActions.FETCH_README else "put",
            )(url, json=data_context, allow_redirects=False, **extra_contents)

            # todo: Make this clarified or confirmed. We don't have a case to where we can see this in action.
            if http_request.ok:
                return http_request

            else:
                # ! Sometimes, we can exceed the rate-limit request per time. We have to handle the display error instead from the receiver of this request.
                _resp_raw: ClientResponse = (
                    http_request  # Supposed to be ClientResponse
                )
                _resp_ctx: dict = literal_eval(str(_resp_raw))

                self.logger.debug(_resp_ctx)
                terminate(ExitReturnCodes.EXCEPTION_EXIT)

        else:
            self.logger.critical(
                f"An Enum invoked on `action` parameter ({action_type.name}) is invalid! This is probably an issue from the developer, please contact the developer as possible."
            )
            terminate(ExitReturnCodes.ILLEGAL_CONDITION_EXIT)
