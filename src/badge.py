"""
copyright 2021 janrey "codexlink" licas

licensed under the apache license, version 2.0 (the "license");
you may not use this file except in compliance with the license.
you may obtain a copy of the license at

	http://www.apache.org/licenses/license-2.0

unless required by applicable law or agreed to in writing, software
distributed under the license is distributed on an "as is" basis,
without warranties or conditions of any kind, either express or implied.
see the license for the specific language governing permissions and
limitations under the license.
"""

if __name__ == "__main__":
	from elements.exceptions import IsolatedExecNotAllowed

	raise IsolatedExecNotAllowed

else:
	import aiohttp
	from elements.constants import BADGE_BASE_URL
	from socket import error as SocketError, gaierror
	class BadgeConstructor:
		"""
		An async-class module that generate badge over-time.

		"""

		async def __init__(self) -> None: # todo: Remove this later if still unused.
			pass

		async def init_badge_services(self) -> None:

			self.request_session = aiohttp.ClientSession() # todo: Check if we should enable raise_for_status
			# Before instantiate, we need to make

			self.logger.debug(f"Instantiation of ClientSession is finished. Info:{self.request_session=}")

			__host_request_validation = await self.request_session.get(BADGE_BASE_URL)

			if __host_request_validation.status == 200:
				self.logger.info(f"Connection to service {BADGE_BASE_URL} is successful.")

			else:
				self.logger.critical(f"Cannot connect to service {BADGE_BASE_URL}. Please check the whole URL and try again. Info: {ConnErr=}")
				self.close()

		async def __validate(self) -> None:
			pass

		async def eval_data(self) -> None:
			pass

		async def service_status(self) -> None:
			pass

		async def return_payload(self) -> None:
			pass

		@property
		async def is_provider_up(self) -> None:
			pass