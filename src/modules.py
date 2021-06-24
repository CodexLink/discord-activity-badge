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
from discord import Activity, ActivityType, Client as DiscordClient, Status
from discord.errors import NotFound
from elements.properties import client_intents as CLIENT_INTENTS
from utils import LoggerComponent
import os
from sys import argv

if __name__ == "__main__" and len(argv) == 1: # argv check is temporary. Will remove later on.
    from elements.exceptions import IsolatedExecNotAllowed
    raise IsolatedExecNotAllowed

else:
    class DiscordClientHandler(DiscordClient, LoggerComponent):
        """ An Async-Class Wrapper for handling Discord API to fetch User's Discord Rich Presence State."""
        async def on_ready(self) -> None:

            print("Client Bot %s is now ready!" % self.user)

            # Create activity for the bot here.
            await self.change_presence(status=Status.online, activity=Activity(name=" your activities.", type=ActivityType.watching))
            # Run other processes.
            await self.get_user_id()        # Get the user first or else return a badge were User is not found.
            await self.get_guild_context()  # Once we have it, then get the guild context.


        async def get_user_id(self) -> None:
            try:
                self.userCtx = await self.fetch_user(os.environ.get("STATIC_TARGET_USER")) # Assume we got it once we received the data.

                print(type(self.userCtx)) # Do something here later.
                # Redundantly ensure that the self.userCtx is discord.user
                # if not isinstance(self.userCtx, discord.user.User):
                    # print("Yes, we wanna raise some error here.")
                    # raise


            except NotFound as Error: # Add custom error here.
                print(type(self.userCtx)) # Do something here later.


            print(self.userCtx)
            # # print(type(self.userCtx))
            print(self.userCtx.mutual_guilds)
            print(dir(self.userCtx))
            print(self.userCtx.id)
            print(self.userCtx.name)
            print(self.userCtx.discriminator)

        async def get_guild_context(self) -> None:
            """Get's the mutual guild of an existing Discord User and generate badge based from their activity"""

            # Before we get the guild context, check if we have the bot and the user reside on a certain guilds (ie. mutual guilds). Or else message them being an error or supressed.
            print(self.userCtx.mutual_guilds)
            b = self.get_guild(os.environ.get("TARGET_STATIC_GUILD"))
            b = self.get_guild(os.environ.get("ANOTHER_TARGET_GUILD"))
            print(b)

            # c = b.get_member(self.user_id.id)

            # print(c)
            # print(dir(c))
    #
            # print(c.activity)
            # print(c.acitivities)
    #
            # print(c.status)
            # print(c.web_status)
            # print(c.desktop_status)
            # print(c.mobile_status)
            # print(c.is_on_mobile())




    class BadgeGenerator(LoggerComponent):
        """
            An async-class module that generate badge over-time.

            Pre-req:
            - DiscordClientHandler must finish before executing contents of this class.
        """
        pass



    # Code Entrypoint.
    load_dotenv("../.env")
    instance = DiscordClientHandler(intents=CLIENT_INTENTS)
    instance.run(os.environ.get("DISCORD_TOKEN"))