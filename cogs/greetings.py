import discord
from discord.ext import commands
from header import Cog_Extension
import json
from .helper import load_guild_config, save_guild_config

#add_role
#auto_role

class greeting(Cog_Extension):
    @commands.Cog.listener()
    async def on_member_join(self, member):
        config = await load_guild_config(member.guild.id)
        print(f'{member} joined.')
        channel = discord.utils.get(member.guild.channels, name=config['welcome_channel'])
        if channel:
            welcome_message = config['welcome_message']
            if '{user}' in welcome_message:
                welcome_message = welcome_message.format(user=member.mention)
            await channel.send(welcome_message)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        print(f'{member} removed.')
        config = await load_guild_config(member.guild.id)
        channel = discord.utils.get(member.guild.channels, name=config['leave_channel'])
        if channel:
            leave_message = config['leave_message']
            if '{user}' in leave_message:
                leave_message = leave_message.format(user=member)
            await channel.send(leave_message)

    @commands.Cog.listener()
    async def on_message(self, message):
        if not message.author.bot:
            try:
                f = open('utils/on_msg.json', mode='r', encoding='utf-8')
                data = json.load(f)
            except Exception as e:
                print(f"An error occurred: {e}")
                return
            msg = message.content.lower()
            if msg in data:
                await message.channel.send(data[msg])

    @commands.command()
    async def ping(self, ctx):
        """Returns the bot's latency in milliseconds."""
        latency = self.bot.latency * 1000  # Convert to milliseconds
        await ctx.send(f'Latency: {latency:.2f}ms')

    #Welcome msg set up
    @commands.command()
    async def welcome(self, ctx, action: str, *, content: str = None):
        """Set up Bot Welcoming message/channel"""
        config = await load_guild_config(ctx.guild.id)
        if action == 'setMessage':
            config['welcome_message'] = content
            await ctx.send(f"Welcome message set to: {content}")
        elif action == 'setChannel':
            config['welcome_channel'] = content
            await ctx.send(f"Welcome channel set to: {content}")
        elif action == 'removeChannel':
            config['welcome_channel'] = None
            await ctx.send(f"Welcome channel removed")
        else:
            await ctx.send(f'Unknown Command')
        await save_guild_config(ctx.guild.id, config)
    
    #Leave msg set up
    @commands.command()
    async def leave(self, ctx, action: str, *, content=None):
        """Set up Bot removing message/channel"""
        config = await load_guild_config(ctx.guild.id)
        if action == 'setMessage':
            config['leave_message'] = content
            await ctx.send(f"Leave message set to: {content}")
        elif action == 'setChannel':
            config['leave_channel'] = content
            await ctx.send(f"Leave channel set to: {content}")
        elif action == 'removeChannel':
            config['leave_channel'] = None
            await ctx.send(f"Leave channel removed")
        else:
            await ctx.send(f'Unknown Command')
        await save_guild_config(ctx.guild.id, config)

async def setup(bot):
    await bot.add_cog(greeting(bot))
