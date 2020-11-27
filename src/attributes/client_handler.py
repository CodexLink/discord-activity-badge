#
# # utils/client_handler.py, Created by Janrey "CodexLink" Licas
# ! A Singleton Class focused on Handling Discord in Client Mode.
# * For use both, workflow_entrypoint.py.

import discord
from handler_attributes import handler_intents

class DiscordClientHandler(discord.Client):
    async def on_ready(self):
        print("Client Bot {0}".format(self.user))
        # self.change_presence(status=discord.Status.online, activity=)

    async def on_message(self, message):
        print("Message from {0.author}: {0.content}".format(message))


if __name__ == "__main__":
    print("Preparing Discord Client Intents.")

    client = DiscordClientHandler(intent=handler_intents)
    client.run("None")