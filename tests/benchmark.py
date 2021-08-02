import discord
from timeit import default_timer

from dotenv import load_dotenv, find_dotenv
from os import environ, _exit


class MyClient(discord.Client):
	async def on_ready(self):
		print("Logged on as", self.user)
		await self.close()
		print(f"Startup time is {default_timer()}.")

load_dotenv(find_dotenv(filename="../.env", raise_error_if_not_found=True))
client = MyClient()
client.run(environ["INPUT_DISCORD_BOT_TOKEN"])