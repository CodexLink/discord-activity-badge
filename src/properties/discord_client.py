#
# # utils/client_handler.py, Created by Janrey "CodexLink" Licas
# ! A Singleton Class focused on Handling Discord in Client Mode.
# * For use both, workflow_entrypoint.py.

import discord

class DiscordClientHandler(discord.Client):
    async def on_ready(self) -> None:
        print("Client Bot {0}".format(self.user))
        # self.change_presence(status=discord.Status.online, activity=)

    async def on_message(self, message):
        print("Message from {0.author}: {0.content}".format(message))


if __name__ == "__main__":
    raise SystemExit("You're about to run a Properties Module which is not allowed! Run the src/entrypoint.py instead!")