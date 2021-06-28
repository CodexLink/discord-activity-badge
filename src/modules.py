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

# # A set of functions used for intended proceses — modules.py

from dotenv import load_dotenv
from discord import Activity, ActivityType, Client as DiscordClient, DMChannel, Status
from discord.errors import NotFound
from elements.properties import client_intents as CLIENT_INTENTS
from utils import LoggerComponent
import os
from sys import argv
from asyncio import create_task, Task
from elements.constants import (
    DISCORD_ON_READY_MSG,
    DISCORD_DATA_CONTAINER,
    DISCORD_DATA_CONTAINER_ATTRS,
)

if (
    __name__ == "__main__" and len(argv) == 1
):  # argv check is temporary. Will remove later on.
    from elements.exceptions import IsolatedExecNotAllowed

    raise IsolatedExecNotAllowed

else:

    class DiscordClientHandler(DiscordClient):
        """An Async-Class Wrapper for handling Discord API to fetch User's Discord Rich Presence State."""

        async def on_ready(self) -> None:

            print(DISCORD_ON_READY_MSG % self.user)

            self.presence_task_loader = create_task(
                self.__preload()
            )  # Optional. Just an extra indicator.

            await self.__steps()  # Call this explicitly since we don't need users to interact with the bot.

        async def __preload_container(self) -> object:
            """
            Creates an object container (which is a class) that contains everything about the user and their properties that is related from this activity.

            Returns:
                object: Returns a referrable object to be used later.

            Notes:
                (1): The following class doesn't save anything about the user, it was just there to retain on runtime so that it can be referrable for future use of discord.py API.
                (2): If you are curious on what does this object contain, please check the elements.constants.py.
                (3): The object that gets returned is a freeze class, meaning, from how they are initialized, should stay like that.

            todo: ref on (3) -> elements.constants about this matter.
            """
            self.__client_container: object = type(
                DISCORD_DATA_CONTAINER, (object,), DISCORD_DATA_CONTAINER_ATTRS
            )
            return self.__client_container

        async def __preload(self) -> None:
            """
                Preloads attributes and properties to be used in the latter process.
            """
            await self.__preload_container()

            await self.change_presence(
                status=Status.online,
                activity=Activity(name=" your activities.", type=ActivityType.watching),
            )

        async def __steps(self) -> None:
            """
            Contains a set of async functions to run in order.

            Since this discord client won't be used as a bot but rather a processor, we will do the process
            by explicitly running certain commands even on the nature of async.

            todo: We can use an argument to surpress and error and render it anyway.
            """

            await self.presence_task_loader # Just wait, so that we can have our data saved in runtime.
            await self.__get_user_id() # Get the user first or else return a badge were User is not found. |
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

    class BadgeGenerator:
        """
        An async-class module that generate badge over-time.

        Pre-req:
        - DiscordClientHandler must finish before executing contents of this class.
        """

        pass

    # todo: Remove this later.
    load_dotenv("../.env")
    # instance = DiscordClientHandler(intents=CLIENT_INTENTS)
    # instance.run(os.environ.get("DISCORD_TOKEN"))
