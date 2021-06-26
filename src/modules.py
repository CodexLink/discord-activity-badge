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

from tkinter import W
from venv import create
from dotenv import load_dotenv
from discord import Activity, ActivityType, Client as DiscordClient, DMChannel, Status
from discord.errors import NotFound
from elements.properties import client_intents as CLIENT_INTENTS
from utils import LoggerComponent
import os
from sys import argv
from asyncio import create_task, Task
if (
    __name__ == "__main__" and len(argv) == 1
):  # argv check is temporary. Will remove later on.
    from elements.exceptions import IsolatedExecNotAllowed

    raise IsolatedExecNotAllowed

else:

    class DiscordClientHandler(DiscordClient):
        """An Async-Class Wrapper for handling Discord API to fetch User's Discord Rich Presence State."""

        async def on_ready(self) -> None:

            print("Client Bot %s is now ready!" % self.user)

            # Create activity for the bot here.
            self.presence_tasks = create_task(self.__preload()) # Optional. This is just an extra sprinkle.

            await self.__steps()

        async def __preload(self) -> None:  # Preload Anything Here.
            await self.change_presence(
                status=Status.online,
                activity=Activity(name=" your activities.", type=ActivityType.watching),
            )

        async def __steps(self) -> None:
            """ Contains a set of functions to run in order. Still retains async for other modules."""
            __usr_ctx = (
                await self.__get_user_id()
            )  # Get the user first or else return a badge were User is not found. | # todo: We can use an argument to surpress and error and render it anyway.

            print("User ID > ", __usr_ctx)

            await self.__get_guild_context()  # Once we have it, then get the guild context.

        async def __get_user_id(self) -> None:
            """ Gets the Discord Information from the User and will encapsulated by a Class."""
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

            print("After > ", self.presence_tasks, type(self.presence_tasks))

            # c = b.get_member(self.user_id.id)

            # print(c)
            # print(dir(c))

        @property
        def is_presence_loaded(self) -> None: # for now
            print(self.presence_tasks.done())
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

    # Code Entrypoint.
    load_dotenv("../.env")

    # # REMOVE THIS LATER.
    instance = DiscordClientHandler(intents=CLIENT_INTENTS)
    instance.run(os.environ.get("DISCORD_TOKEN"))
