import discord
from discord.ext import commands
from header import Cog_Extension

class event(Cog_Extension):
    @commands.Cog.listener()
    async def on_member_join(self, member):
        print(f'{member} joined.')
        channel = member.guild.system_channel
        if channel is not None:
            await channel.send(f'{member.mention} joined. Welcome!')
    
    @commands.Cog.listener()
    async def on_member_remove(self, member):
        print(f'{member} removed.')
        channel = member.guild.system_channel
        if channel is not None:
            await channel.send(f'{member} removed. Goodbye!')

    @commands.command()
    async def ping(self, ctx):
        """Returns the bot's latency in milliseconds."""
        latency = self.bot.latency * 1000  # Convert to milliseconds
        await ctx.send(f'Latency: {latency:.2f}ms')

async def setup(bot):
    await bot.add_cog(event(bot))
