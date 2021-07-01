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

from discord import Activity, ActivityType, Client as DiscordClient, DMChannel, Status
from discord.errors import NotFound
import logging
import os
from asyncio import create_task, Task
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
			) # No need to await this one.

			create_task((self.change_presence(
				status=Status.online,
				activity=Activity(name=" your activities.", type=ActivityType.watching),
			))) # Let this one do the work.

			self.logger.info(f"Instance of {DiscordClientHandler.__name__} has finished doing tasks asynchronously. Ready to call DiscordClientHandler__process_presence_data() to start processing.")


		async def __process_presence_data(self) -> None:
			"""
			Contains a set of async functions to run in order.

			Since this discord client won't be used as a bot but rather a processor, we will do the process
			by explicitly running certain commands even on the nature of async.

			todo: We can use an argument to surpress and error and render it anyway.
			"""

			await self.presence_task_loader  # Just wait, so that we can have our data saved in runtime.
			await self.__get_user_id()  # Get the user first or else return a badge were User is not found. |
			await self.__get_guild_context()  # Once we have it, then get the guild context.

		async def __get_user_id(self) -> None:
			"""Gets the Discord Information from the User and will encapsulated by a Class."""
			try:
				self.userCtx = await self.fetch_user(
					os.environ.get("STATIC_TARGET_USER")
				)  # Assume we got it once we received the data.

				print(type(self.userCtx))  # Do something here later.
				# Redundantly ensure that the self.userCtx is discord.user
				# if not isinstance(self.userCtx, discord.user.User):
				# print("Yes, we wanna raise some error here.")
				# raise

				# await self.userCtx.create_dm()
				# await self.userCtx.send("Hello, this is a test.")

			except NotFound as Error:  # Add custom error here.
				print("Error here.")
				return
				print(type(self.userCtx))  # Do something here later.

			print(self.userCtx)
			# # print(type(self.userCtx))
			print(self.userCtx.mutual_guilds)

			print(dir(self.userCtx))
			print(self.userCtx.id)
			print(self.userCtx.name)
			print(self.userCtx.discriminator)

		async def __get_guild_context(self) -> None:
			"""Get's the mutual guild of an existing Discord User and generate badge based from their activity"""

			# Before we get the guild context, check if we have the bot and the user reside on a certain guilds (ie. mutual guilds). Or else message them being an error or supressed.
			print(self.userCtx.mutual_guilds)
			b = self.get_guild(os.environ.get("TARGET_STATIC_GUILD"))
			b = self.get_guild(os.environ.get("ANOTHER_TARGET_GUILD"))
			print(b)

			# todo: We check if the task is good here. Use await on that particular task.
			# print(
			#     "After > ", self.presence_task_loader, type(self.presence_task_loader)
			# )

			# c = b.get_member(self.user_id.id)

			# print(c)
			# print(dir(c))

		@property
		def is_presence_loaded(self) -> None:  # for now
			print(self.presence_task_loader.done())
			return

	#
	# print(c.activity)
	# print(c.acitivities)
	#
	# print(c.status)
	# print(c.web_status)
	# print(c.desktop_status)
	# print(c.mobile_status)
	# print(c.is_on_mobile())