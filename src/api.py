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

from asyncio import (
	as_completed,
	ensure_future,
	Future,
	sleep as asyncio_sleep,
)
from aiohttp import ClientSession
from typing import Any, Literal, Union, Optional
from json import load as JSON_SERIALIZE
from ast import literal_eval
from base64 import b64decode, b64encode
from elements.exceptions import SessionRequestHTTPError
from elements.constants import (
	GithubRunnerActions,
	ResponseTypes,
	RESTResponse,
	DISCORD_CLIENT_INTENTS,
)
from elements.typing import HttpsURL, Base64
import os


class AsyncRequestAPI:
	"""
	A set of async functions that handles API handler. This includes Github API and Badgen API.
	The class has the prefix "Static" because of its inability to register other APIs during Runtime.
	I didn't designed the Class to be dynamic but it can be possible for future use. Keep note of other function
	raising 'NotImplemented'.
	"""

	async def __ainit__(self) -> None:
		super().__init__()  # Required?
		self.logger.debug(
			f"Instantiatied Class discord.Client with intents={DISCORD_CLIENT_INTENTS=}"
		)

		self._api_session: ClientSession = ClientSession()
		self._github_fetched_data : Any = None

		await asyncio_sleep(0.001)
		self._test_api_task: Future = ensure_future(self.test_api_conn())

		self.logger.info(
			f"{AsyncRequestAPI.__name__} is ready for handling requests from Github API and Badgen API."
		)

	async def test_api_conn(self) -> None:
		__endpoints: list[HttpsURL] = [
			self.resolved_envs["GITHUB_API_URL"],
			"https://badgen.net",
		]
		__responses: list[Future] = []

		for idx, each_endpoint in enumerate(__endpoints):
			self.logger.info(
				f"Attempting to Test Connection ({idx + 1}/{len(__endpoints)}) | {each_endpoint}..."
			)
			__responses.append(
				self._request(
					each_endpoint, should_return=ResponseTypes.RESPONSE_STATUS
				)
			)

		for response in as_completed(__responses):
			_tasks = await response
			if not _tasks:
				raise SessionRequestHTTPError

			self.logger.info(
				f"Connection Response from {_tasks[0]} returned STATUS {_tasks[1]}!"
			)

		self.logger.info(
			"Test API Connection as been completed! Ready to use those API!"
		)

	async def github_api_connect(self) -> None:
		self.logger.info("Authenticating to Github API.")

		__conn: Future = await self._request(
			self.resolved_envs["GITHUB_API_URL"],
			data={
				self.resolved_envs["GITHUB_ACTOR"]: self.resolved_envs["WORKFLOW_TOKEN"]
			},
			should_return=ResponseTypes.IS_OKAY,
		)

		if __conn:
			self.logger.info("Successfully Authenticated! (to Github API!)")
			return

		self.logger.error(
			"Unable to authenticate. Please check your credentials in Secrets!!!"
		)
		os._exit(-1)

	async def github_action_repo(
		self, actions: GithubRunnerActions, return_ctx: bool = False
	) -> Any:

		# TODO: Check what to try-catch here.
		if actions is GithubRunnerActions.FETCH_README:
			__user_repo = "{0}/{0}".format(self.resolved_envs["GITHUB_ACTOR"]) if not len(self.resolved_envs["PROFILE_REPO"]) else "{0}".format(self.resolved_envs["PROFILE_REPO"])
			__repo_path = (
				"{0}/repos/{1}/readme".format(self.resolved_envs["GITHUB_API_URL"], __user_repo)
			)
			__fetch_readme: Future = await self._request(__repo_path)

			# * Give user an option whether we want to decode the b64 or not.

			__read_resp: bytes = __fetch_readme.content.read_nowait()
			__serialized_resp: dict = literal_eval(__read_resp.decode("utf-8"))
			__sresp_content: Base64 = __serialized_resp["content"].replace("\n", "")

			self._github_fetched_data = __serialized_resp
			self.logger.info(f"Github Profile ({__user_repo}) README has been fetched.")




	async def _request(
		self,
		url: HttpsURL,
		rest_response: RESTResponse = RESTResponse.GET,
		data: Optional[dict[str, Any]] = {},
		headers: Optional[dict[str, Any]] = {},
		should_return: ResponseTypes = ResponseTypes.RESPONSE,
		status_asserts: Optional[int] = 200,  # Might be removed later.
	) -> Any:  # Subject to change.

		if self._api_session.closed:
			self.logger.critical("Session has been closed! Reenabling...")
			await self._reopen_conn()
			self.logger.critical("Session has been opened! Processing requests...")

		if rest_response is RESTResponse.GET:
			_http_request = await self._api_session.get(url)

		if should_return is ResponseTypes.IS_OKAY:
			return [url, _http_request.ok]

		elif should_return is ResponseTypes.RESPONSE_STATUS:
			return [url, _http_request.status]

		elif should_return is ResponseTypes.RESPONSE:
			return _http_request

		else:
			self.logger.critical(
				"Specified `should_return` is invalid. Please check the function for more information."
			)
			os._exit(-1)

	async def _reopen_conn(
		self,
	):  # This is temporary, but if it ever happen that it was closed, enable it again.
		await self.__ainit__()

	async def close_conn(self):
		await self._api_session.close()
