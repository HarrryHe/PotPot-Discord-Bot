import discord
from discord.ext import commands
from header import Cog_Extension
from profanity_check import predict

class general(Cog_Extension):
    
    commands.command()
    async def clean(self, ctx, *,num: int = 1):
        await ctx.channel.purge(limit=num)

async def setup(bot):
    await bot.add_cog(general(bot))