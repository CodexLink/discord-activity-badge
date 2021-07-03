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

    	# By this point, there are a variety of Activities. We need to select one and avail to resolve from what the user wants.
    	# First let's evaluate what user wants to display in their badge.
		# todo: We need a parameter that PREFER_CUSTOM_ACTIVITY_OVER_PRESENCE.

		# First we have to understand that, the way how discord displays the status of user by order.
		# CustomActivity (Custom Status) > Activity (Rich Presence) > Game (Game)
		# The way how Discord.py stores activities: CustomActivity(Custom Status) > Game (Game) > Activity (Rich Presence)

		# We will follow how Discord Client displays it.

		"""
			Example:
			Set of Activities:  (<CustomActivity name='I wanna hug and pat teri~' emoji=<PartialEmoji animated=True name='TeriPats' id=???>>,
			<Game name='Honkai Impact 3'>,
			<Activity type=<ActivityType.playing: 0> name='osu!' url=None details=None application_id=??? session_id=None emoji=None>,
			<Activity type=<ActivityType.playing: 0> name='Visual Studio Code' url=None details='Editing client.py: 165:79 (211)' application_id=??? session_id='??? emoji=None>)
		"""

		# todo: Let's push this one on the BadgeGenerator instead.
		# if os.environ.get("PREFERRED_ACTIVITY_TO_DISPLAY") in ["ALL_ACTIVITIES", "CUSTOM_ACTIVITY", "RICH_PRESENCE", "GAME_ACTIVITY"]:
		# pass
		# else:
		# 	self.logger.error("The supplied value of PREFERRED_ACTIVITY_TO_DISPLAY is invalid. Please check the documentation, check your workflow secret/input and try again.")
		# 	os._exit(-7)

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