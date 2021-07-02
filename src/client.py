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

# # A set of functions used for intended proceses — modules.py

from stat import FILE_ATTRIBUTE_ARCHIVE
from discord import Activity, ActivityType, Client as DiscordClient, Status
from discord.errors import Forbidden, NotFound
from discord.user import User
from discord.guild import Guild
import logging
import os
from asyncio import create_task, Future, Task, Queue
from typing import Any
from elements.constants import (
	DISCORD_ON_READY_MSG,
	DISCORD_DATA_CONTAINER,
	DISCORD_DATA_CONTAINER_ATTRS,
)

if __name__ == "__main__":
	from elements.exceptions import IsolatedExecNotAllowed

	raise IsolatedExecNotAllowed

else:

	class DiscordClientHandler(DiscordClient):
		"""An Async-Class Wrapper for handling Discord API to fetch User's Discord Rich Presence State."""

		async def on_ready(self) -> None:
			"""
			Creates an object container (which is a class) that contains everything about the user and their properties that is related from this activity.

			Returns:
											object: Returns a referrable object to be used later.

			Preloads attributes and properties to be used in the latter process.

			Notes:
											(1): The following class doesn't save anything about the user, it was just there to retain on runtime so that it can be referrable for future use of discord.py API.
											(2): If you are curious on what does this object contain, please check the elements.constants.py.
											(3): The object that gets returned is a freeze class, meaning, from how they are initialized, should stay like that.

			todo: ref on (3) -> elements.constants about this matter.
			"""
			self.logger.info(DISCORD_ON_READY_MSG % self.user)

			self.__client_container: object = type(
				DISCORD_DATA_CONTAINER, (object,), DISCORD_DATA_CONTAINER_ATTRS
			)  # Creates a container for use later. No need to await this one.
			# todo: Try to resolve other missing things with typing later.

			create_task(
				(
					self.change_presence(
						status=Status.online,
						activity=Activity(
							name=" your activities.", type=ActivityType.watching
						),
					)
				)
			)  # Changes the bot's presence concurrently.

			self.logger.info(
				f"Instance of {DiscordClientHandler.__name__} has finished setting tasks asynchronously. Access to ... (property) is now allowed."
			)

			# Get the user first, then get the guild context.
			await self.get_presence_via_guild(await self.__get_user())

		async def __get_user(self) -> User:
			"""Gets the Discord Information from the User and will encapsulated by a Class."""
			self.logger.info(
				"Step 1 of 2 | Attempting to fetch discord user's info for validation use."
			)

			try:
				__user_info__ = await self.fetch_user(
					os.environ.get("STATIC_TARGET_USER")
				)

				print(type(__user_info__))

				self.__client_container.__usr__["id"] = __user_info__.id
				self.__client_container.__usr__["name"] = __user_info__.name
				self.__client_container.__usr__[
					"discriminator"
				] = __user_info__.discriminator

				# await __user_info__.create_dm()
				# await __user_info__.send("Hello, this is a test.")

				self.logger.info(
					"Finished fetching user information. (id, name, and discriminator)"
				)

				return __user_info__

			except NotFound:  # Add custom error here.
				self.logger.error(
					"The user cannot be found. Are you sure you have typed your ID properly?"
				)
				os._exit(-2)

		async def get_presence_via_guild(self, _fetched_user: User) -> None:
			"""Get's the mutual guild of an existing Discord User and generate badge based from their activity"""
			# Before we get the guild context, check if we have the bot and the user reside on a certain guilds (ie. mutual guilds). Or else message them being an error or supressed.

			self.logger.info(
				"Step 2 of 2 | Attempting to fetch guild context from where the bot also resides."
			)

			try:
				if _fetched_user.mutual_guilds is None:
					self.logger.error(f"Discord User doesn't have any Mutual Guilds with {self.user}. Please add the bot to your server and try again.")
					os._exit(-3)

				if type(_fetched_user.mutual_guilds[0]) != Guild:
					self.logger.critical(f"The list of mutual guild is expected to be {Guild} but received a type {type(_fetched_user.mutual_guilds)}")
					os._exit(-4)

				c = _fetched_user.mutual_guilds[0].get_member(_fetched_user.id)

				# todo: Create options, on what to display. Either CustomActivity or Activity or Mixed. Depending to user.

				print(c.activity)
				print(c.activities)

				print(c.status)
				print(c.web_status)
				print(c.desktop_status)
				print(c.mobile_status)
				print(c.is_on_mobile())


			self.logger.info("Step 2 of 2 | Done.")
