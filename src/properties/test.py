from discord.ext.commands import Bot
from discord import Member
from dotenv import load_dotenv
import os

bot = Bot('!')

@bot.command(pass_context=True, name='status')
async def status(ctx, member: Member):
    await bot.say(str(member.status))

load_dotenv("../../.env")
bot.run(os.environ.get("DISCORD_BOT_TOKEN"))