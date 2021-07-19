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

import os
from ast import literal_eval
from asyncio import Future, as_completed, ensure_future, sleep as asyncio_sleep
from base64 import b64decode, b64encode
from json import load as JSON_SERIALIZE
from typing import Any, Optional, Union

from aiohttp import BasicAuth, ClientSession

from elements.constants import (
    DISCORD_CLIENT_INTENTS,
    GithubRunnerActions,
    ResponseTypes,
)
from elements.exceptions import (
    SessionRequestHTTPError,
    SessionRequestStatusAssertFailed,
)
from elements.typing import Base64, HttpsURL, ResolvedHTTPResponse


class AsyncRequestAPI:
    """
    A set of async functions that handles API handler. This includes Github API and Badgen API.
    The class has the prefix "Static" because of its inability to register other APIs during Runtime.
    I didn't designed the Class to be dynamic but it can be possible for future use. Keep note of other function
    raising 'NotImplemented'.
    """

    async def __ainit__(self) -> None:

        self._api_session: ClientSession = ClientSession()
        await asyncio_sleep(0.001)
        self.logger.info("Instantiated ClientSession for API Requests.")

        super().__init__()  # Required?
        self.logger.info(
            f"Instantiatied Discord Client with the following intents={DISCORD_CLIENT_INTENTS=}"
        )

        self._test_api_task: Future = ensure_future(self.test_api_conn())

        await asyncio_sleep(0.001)
        self.logger.info(
            f"{AsyncRequestAPI.__name__} is ready for handling requests from Github API and Badgen API."
        )

    async def test_api_conn(self) -> None:
        __endpoints: list[HttpsURL] = [
            self.envs["GITHUB_API_URL"],
            "https://badgen.net",
        ]
        __responses: list[Future] = []

        for idx, each_endpoint in enumerate(__endpoints):
            self.logger.info(
                f"Attempting to Test Connection ({idx + 1}/{len(__endpoints)}) | {each_endpoint}..."
            )
            __responses.append(
                self._request(
                    each_endpoint,
                    rest_response=GithubRunnerActions.TEST_CONN_APIS,
                    should_return=ResponseTypes.IS_OKAY,
                )
            )

        for response in as_completed(__responses):
            _tasks = await response

            # todo: We can make something out of this better.
            if not _tasks[1]:
                raise SessionRequestHTTPError

            self.logger.info(
                "Connection Response from {0} is {1}!".format(
                    _tasks[0], "OKAY" if _tasks[1] else "NOT OKAY"
                )
            )

        self.logger.info("Test API Connection as been completed!")

    async def github_api_connect(self) -> None:
        self.logger.info("Authenticating to Github API...")

        __conn = await self._request(  # todo: To be annotated soon.
            self.envs["GITHUB_API_URL"],
            GithubRunnerActions.AUTH_GITHUB_API,
            should_return=ResponseTypes.RESPONSE,
        )

        self.logger.debug(
            "Github Auth User Info | Requests Left over Rate Limit: {0}/{1}".format(
                __conn.headers["X-RateLimit-Remaining"],
                __conn.headers["X-RateLimit-Limit"],
            )
        )

        if __conn.ok:
            self.logger.info("Successfully Authenticated to Github API!")
            return

        self.logger.error(
            "Unable to authenticate. Please check your credentials in Secrets!!!"
        )
        os._exit(-1)

    async def exec_api_actions(self, actions: GithubRunnerActions) -> Union[Any, ResolvedHTTPResponse]:

        # TODO: Check what to try-catch here.
        if actions is GithubRunnerActions.FETCH_README:
            __user_repo = (
                "{0}/{0}".format(self.envs["GITHUB_ACTOR"])
                if not len(self.envs["PROFILE_REPO"])
                else "{0}".format(self.envs["PROFILE_REPO"])
            )
            __repo_path = "{0}/repos/{1}/readme".format(
                self.envs["GITHUB_API_URL"], __user_repo
            )

            self.logger.info(
                f"Fetching User's Github Profile Repository ({__user_repo})..."
            )

            # todo: Annotate this later.
            while True:
                try:
                    __fetch_readme: Future = await self._request(
                        __repo_path, GithubRunnerActions.FETCH_README
                    )

                    # * Give user an option whether we want to decode the b64 or not.

                    __read_resp: bytes = __fetch_readme.content.read_nowait()
                    __serialized_resp: dict = literal_eval(__read_resp.decode("utf-8"))

                    __sresp_content: Base64 = __serialized_resp["content"].replace(
                        "\n", ""
                    )
                    self.logger.info(
                        f"Github Profile ({__user_repo}) README has been fetched."
                    )
                    return __sresp_content

                except SyntaxError as RecvCtx:
                    self.logger.error(
                        "Received Data (from README) is malformed. Retrying to fetch again..."
                    )
                    self.logger.debug(
                        "Technical Error on Malformed Data: %s" % (RecvCtx)
                    )
                    continue

                except KeyError as RecvCtx:  # todo: Create an exception for this one. GithubAPIRateLimited
                    if __serialized_resp["message"].startswith(
                        "API rate limit exceeded"
                    ):
                        self.logger.critical(
                            f"You are potentially Rate Limited by Github API. Did you keep on retrying or you are over-committing changes? | More Info: {RecvCtx}"
                        )
                        os._exit(-1)

    async def _request(
        self,
        url: HttpsURL,
        rest_response: GithubRunnerActions,
        should_return: ResponseTypes = ResponseTypes.RESPONSE,
    ) -> Union[
        list[Union[str, bool, int]], Any
    ]:  # Subject to change, for typing.Any since I don't know what type is it..

        if self._api_session.closed:
            self.logger.critical("Session has been closed! Reenabling...")
            await self._reopen_conn()
            self.logger.critical("Session has been opened! Processing requests...")

        # todo: DRY.

        if rest_response is GithubRunnerActions.TEST_CONN_APIS:
            _http_request = await self._api_session.get(url)

        # ! REMINDER, CHECK IF SAME FUNCTIONALITY OF IS FROM IN WITH THE SET OF LIST.
        elif rest_response in [
            GithubRunnerActions.AUTH_GITHUB_API,
            GithubRunnerActions.FETCH_README,
        ]:
            _http_request = await self._api_session.get(
                url,
                auth=BasicAuth(self.envs["GITHUB_ACTOR"], self.envs["WORKFLOW_TOKEN"]),
            )

        if not _http_request.ok: # todo: Make this clarified or confirmed. We don't have a case to where we can see this in action.
            self.logger.critical(_http_request.status, _http_request.content)
            _resp_raw: bytes = _http_request
            _resp_ctx: dict = literal_eval(_resp_raw)
            raise SessionRequestStatusAssertFailed(_http_request.response)

        if should_return is ResponseTypes.IS_OKAY:
            return [url, _http_request.ok]

        elif should_return is ResponseTypes.RESPONSE_STATUS:
            return [url, _http_request.status]

        elif should_return is ResponseTypes.RESPONSE:
            return _http_request

        else:
            self.logger.critical(
                "Specified `should_return` is invalid or haven't implemented yet. Please check the function for more information."
            )
            os._exit(-1)

    async def _reopen_conn(
        self,
    ):  # This is temporary, but if it ever happen that it was closed, enable it again.
        await self.__ainit__()

    async def close_conn(self):
        await self._api_session.close()
