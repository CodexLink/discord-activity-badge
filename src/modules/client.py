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

# # utils/client_handler.py, Created by Janrey "CodexLink" Licas
# ! A Singleton Class focused on Handling Discord in Client Mode.
# * For use both, workflow_entrypoint.py.
import discord
from dotenv import load_dotenv
import os
import logging

class DiscordClientHandler(discord.Client):
    async def on_ready(self) -> None:

        print("Client Bot %s is ready for processing!" % self.user)

        # Create activity for the bot here.
        await self.change_presence(status=discord.Status.online, activity=discord.Activity(name=" your activities.", type=discord.ActivityType.watching))
        # Run other processes.
        await self.get_user_id()        # Get the user first or else return a badge were User is not found.
        await self.get_guild_context()  # Once we have it, then get the guild context.


    async def get_user_id(self) -> None:
        try:
            self.userCtx = await self.fetch_user(os.environ.get("STATIC_TARGET_USER")) # Assume we got it once we received the data.

            print(type(self.userCtx)) # Do something here later.
            # Redundantly ensure that the self.userCtx is discord.user
            if not isinstance(self.userCtx, discord.user.User):
                print("Yes, we wanna raise some error here.")
                # raise


        except discord.errors.NotFound as Error: # Add custom error here.
            print(type(self.userCtx)) # Do something here later.


        # z = self.user_id.mutual_guilds
        # print(z)

        # print(self.user_id)
        # # print(type(self.user_id))
        # print(self.user_id.mutual_guilds)
        # print(dir(self.user_id))
        # print(self.user_id.id)
        # print(self.user_id.name)
        # print(self.user_id.discriminator)

    async def get_guild_context(self) -> None:
        """Get's the mutual guild of an existing Discord User and generate badge based from their activity"""

        # Before we get the guild context, check if we have the bot and the user reside on a certain guilds (ie. mutual guilds). Or else message them being an error or supressed.
        # print(self.userCtx.mutual_guilds)
        # b = self.get_guild(os.environ.get("TARGET_STATIC_GUILD"))
        # b = self.get_guild(os.environ.get("ANOTHER_TARGET_GUILD"))
        # print(b)

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



if __name__ == "__main__":
    load_dotenv("../../.env")

    # To be added in logs later.


    logger = logging.getLogger('discord')
    logger.setLevel(logging.DEBUG)
    handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
    handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
    logger.addHandler(handler)
    instance = DiscordClientHandler(intents=discord.Intents.all())
    instance.run(os.environ.get("DISCORD_TOKEN"))

raise SystemExit("You're about to run a Properties Module which is not allowed! Run the src/entrypoint.py instead!")