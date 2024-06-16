import discord
from discord.ext import commands
from header import Cog_Extension
import os, json
import sqlite3

def load_config(guild_id):
    conn = sqlite3.connect('cogs/configs/configurations.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM greeting_configs WHERE guild_id = ?', (guild_id,))
    row = cursor.fetchone()
    print("cursor fetch successed.")
    conn.close()
    if row:
        return {
            "welcome_message": row[1],
            "welcome_channel": row[2],
            "leave_message": row[3],
            "leave_channel": row[4]
        }
    else:
        return {
            "welcome_message": "Welcome to the server, {user}!",
            "welcome_channel": None,
            "leave_message": "Goodbye, {user}!",
            "leave_channel": None
        }

#Save Configuration to the sqlite
def save_config(guild_id, config):
    conn = sqlite3.connect('cogs/configs/configurations.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT OR REPLACE INTO greeting_configs (guild_id, welcome_message, welcome_channel, leave_message, leave_channel)
        VALUES (?, ?, ?, ?, ?)
    ''', (guild_id, config['welcome_message'], config['welcome_channel'], config['leave_message'], config['leave_channel']))
    conn.commit()
    print("Database commit successed")
    conn.close()

class greeting(Cog_Extension):
    @commands.Cog.listener()
    async def on_member_join(self, member):
        config = load_config(member.guild.id)
        print(f'{member} joined.')
        channel = discord.utils.get(member.guild.channels, name=config['welcome_channel'])
        if channel:
            welcome_message = config['welcome_message'].format(user=member.mention)
            await channel.send(welcome_message)
    
    @commands.Cog.listener()
    async def on_member_remove(self, member):
        print(f'{member} removed.')
        config = load_config(member.guild.id)
        channel = discord.utils.get(member.guild.channels, name=config['leave_channel'])
        if channel:
            leave_message = config['leave_message'].format(user=member)
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
            if message.content in data:
                await message.channel.send(data[message.content])

    @commands.command()
    async def ping(self, ctx):
        """Returns the bot's latency in milliseconds."""
        latency = self.bot.latency * 1000  # Convert to milliseconds
        await ctx.send(f'Latency: {latency:.2f}ms')

    #Welcome msg set up
    @commands.command()
    async def welcome(self, ctx, action: str, *, content: str = None):
        """Set up Bot Welcoming message/channel"""
        config = load_config(ctx.guild.id)
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
        save_config(ctx.guild.id, config)
    
    #Leave msg set up
    @commands.command()
    async def leave(self, ctx, action: str, *, content=None):
        """Set up Bot removing message/channel"""
        config = load_config(ctx.guild.id)
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
        save_config(ctx.guild.id, config)

async def setup(bot):
    await bot.add_cog(greeting(bot))
