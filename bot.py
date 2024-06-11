import os
import discord
from discord.ext import commands

bot = commands.Bot(command_prefix='-', intents=discord.Intents.all())

@bot.event
async def on_ready():
    print("--Bot is Online--")
    await load_extensions()

async def load_extensions():
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py') and filename != "__init__.py":
            await bot.load_extension(f'cogs.{filename[:-3]}')


if __name__ == "__main__":
    bot.run(os.getenv("DISCORD_BOT_TOKEN"))

