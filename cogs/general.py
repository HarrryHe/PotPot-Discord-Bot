import discord
from discord.ext import commands
from header import Cog_Extension
from profanity_check import predict
from datetime import timedelta
import sqlite3
from greetings import load_guild_config, save_guild_config


#DB DESIGN General Information:
#User_ID Primary
#Guild_ID Primary
#Profanity_count INT
#profanity_switch: bool
#inactive_count: bool

def load_user_config(guild_id, user_id):
    conn = sqlite3.connect('cogs/configs/configurations.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM user_configs WHERE guild_id = ? AND user_id = ?', (guild_id, user_id))
    row = cursor.fetchone()
    print("Cursor fetch succeeded.")
    conn.close()
    if row:
        return {
            "guild_id": row[1],
            "user_id": row[0],
            "profanity_count": row[2],
            "inactive_count": row[3]
        }
    else:
        return {
            "guild_id": guild_id,
            "user_id": user_id,
            "profanity_count": 0,
            "inactive_count": 0
        }
    
def save_user_config(user_id, guild_id, config):
    conn = sqlite3.connect('cogs/configs/configurations.db')
    cursor = conn.cursor()
    
    cursor.execute('''
    INSERT OR REPLACE INTO user_configs (user_id, guild_id, profanity_count, inactive_count)
    VALUES (?, ?, ?, ?)
    ''', (user_id, guild_id, config['profanity_count'], config['inactive_count']))
    
    conn.commit()
    conn.close()

profanity_check: bool

class general(Cog_Extension):

    async def apply_timeout(self, user: discord.Member, minutes: int):
        await user.edit(timed_out_until=discord.utils.utcnow() + timedelta(minutes=minutes))
    
    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def clean(self, ctx, num: int = 1):
        await ctx.channel.purge(limit=num, delete_after=5)
    

    #Open up or close down the profanity checker
    @commands.command()
    async def profanityChecker(self, ctx, switch: bool=False):
        config = load_guild_config(ctx.guild.id)
        if switch is True:
            config["profanity_switch"] = 1
        else:
            config["profanity_switch"] = 0
        save_guild_config(ctx.guild.id, config)
    
    async def apply_timeout(self, user: discord.Member, minutes: int):
        await user.timeout(timedelta(minutes=minutes))

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return
        #on message profanity checker
        #Currently Just not input database, Because database under constructed
        if profanity_check is True:
            if predict([message.content])[0] == 1:
                await message.delete()
                #To input database right here store which guild which user and how many counts in sqlite
                await self.apply_timeout(message.author, 3)
                await message.channel.send(f'{message.author.mention} used bad words, 3 min TIMEOUT applied! :3!!!')
                await message.channel.send('Please keeping the rule otherwise will be auto kicked out!!!')
        
    

async def setup(bot):
    await bot.add_cog(general(bot))