#
# # utils/client_handler.py, Created by Janrey "CodexLink" Licas
# ! A Singleton Class focused on Handling Discord in Client Mode.
# * For use both, workflow_entrypoint.py.
import discord
from dotenv import load_dotenv
import os

class DiscordClientHandler(discord.Client):
    async def on_ready(self) -> None:

        self.user_id = None
        self.guild_context = None

        print("Client Bot %s is ready for scanning!" % self.user)

        print("Client Bot | Fetching ID.")
        # Once the Client Handler is ready. Run a certain functions that goes with the process.
        # self.change_presence(status=discord.Status.online, activity=)

        await self.get_user_id()
        await self.get_guild_context()

    async def on_message(self, message):
        print("Message from {0.author}: {0.content}".format(message))

    async def get_guild_context(self) -> None:
        b = self.get_guild(768387013647794186)
        # b = self.get_guild(684803928885428255)
        print(b)

        c = b.get_member(self.user_id.id)

        print(c)
        print(dir(c))

        print(c.activity)

        print(c.status)
        print(c.web_status)
        print(c.desktop_status)
        print(c.mobile_status)
        print(c.is_on_mobile())


    async def get_user_id(self) -> None:
        self.user_id = await self.fetch_user(298292688166584331)

        # print(self.user_id)
        # print(dir(self.user_id))
        # print(self.user_id.id)
        # print(self.user_id.name)
        # print(self.user_id.discriminator)


if __name__ == "__main__":
    load_dotenv("../../.env")
    # raise SystemExit("You're about to run a Properties Module which is not allowed! Run the src/entrypoint.py instead!")
    instance = DiscordClientHandler(intents=discord.Intents.all())
    instance.run(os.environ.get("DISCORD_TOKEN"))