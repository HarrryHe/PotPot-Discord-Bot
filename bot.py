import os
import discord
from discord.ext import commands

bot = commands.Bot(command_prefix='-', intents=discord.Intents.all())

@bot.event
async def on_ready():
    print("--Bot is Online--")
    await load_extensions()

@bot.command()
async def load(ctx, extension):
    bot.load_extension(f'cogs.{extension}')
    await ctx.send(f'load {extension} succeed')

@bot.command()
async def unload(ctx, extension):
    bot.unload_extension(f'cogs.{extension}')
    await ctx.send(f'unload {extension} succeed')

@bot.command()
async def reload(ctx, extension):
    bot.reload_extension(f'cogs.{extension}')
    await ctx.send(f'reload {extension} succeed')

async def load_extensions():
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py') and filename != "__init__.py" and filename != "helper.py":
            await bot.load_extension(f'cogs.{filename[:-3]}')

if __name__ == "__main__":
    bot.run(os.getenv("DISCORD_BOT_TOKEN"))
