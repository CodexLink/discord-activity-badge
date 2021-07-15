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

from asyncio import ensure_future, Future, sleep as asyncio_sleep, as_completed
from aiohttp import ClientSession
from typing import Any, Literal, Union, Optional
from json import load as JSON_SERIALIZE
from ast import literal_eval
from base64 import b64decode, b64encode
from elements.exceptions import SessionRequestHTTPError
from elements.constants import ResponseTypes, RESTResponse, DISCORD_CLIENT_INTENTS
from elements.typing import HttpsURL
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

		self._api_session = ClientSession()
		self.logger.debug(f"Instantiatied Class discord.Client with intents={DISCORD_CLIENT_INTENTS=}")

		await self.test_api_conn()

		self.logger.info(
			f"{AsyncRequestAPI.__name__} is ready for handling requests from Github API and Badgen API."
		)

	async def test_api_conn(self) -> None:
		__endpoints: list[str] = [os.environ["GITHUB_API_URL"], "https://badgen.net"]
		__responses: list[Future] = []

		for idx, each_endpoint in enumerate(__endpoints):
			self.logger.info(
				f"Attempting to Test Connection ({idx + 1}/{len(__endpoints)}) | {each_endpoint}..."
			)
			__responses.append(self._request(each_endpoint))

		for response in as_completed(__responses):
			_tasks = await response
			if not _tasks:
				raise SessionRequestHTTPError

			self.logger.info(f"Connection Response from {_tasks[0]} returned STATUS {_tasks[1]}!")

	async def github_api_connect(self) -> None:
		self.logger.info("Authenticating to Github API.")
		__conn : Future = await self._request(os.environ["GITHUB_API_URL"], data={os.environ["GITHUB_ACTOR"]: os.environ["INPUT_WORKFLOW_TOKEN"]}, should_return=ResponseTypes.IS_OKAY)

		if __conn:
			self.logger.info("Successfully Authenticated! (to Github API!)")

		self.logger.error("Unable to authenticate. Please check your credentials in Secrets!!!")
		os._exit(-1)

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

		elif should_return is ResponseTypes.RESP_STATUS:
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
