import discord
from discord.ext import commands
from header import Cog_Extension
from profanity_check import predict
from datetime import timedelta
import datetime
import sqlite3
from .greetings import load_guild_config, save_guild_config

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

    @commands.command()
    async def info(self, ctx):
        embed = discord.Embed(title="Server Information", description=f'Server ID: {ctx.guild.id}', timestamp=datetime.datetime.now(), color=0xddb6b8)
        embed.set_author(name="PotPot", icon_url=self.bot.user.display_avatar.url)
        if ctx.guild.icon is not None:
            embed.set_thumbnail(url=ctx.guild.icon.url)
        else:
            embed.set_thumbnail(url="https://via.placeholder.com/150")
        embed.add_field(name="Server Owner", value=ctx.guild.owner, inline=False)
        embed.add_field(name="Total Members", value=ctx.guild.member_count, inline=False)
        embed.add_field(name="Total Channels", value=len(ctx.guild.channels), inline=False)
        embed.add_field(name="Total Roles", value=len(ctx.guild.roles), inline=False)
        embed.set_footer(text='\u200b')
        await ctx.send(embed=embed)

    #clean {num} messages
    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def clean(self, ctx, limit: int = 100):
        await ctx.channel.purge(limit=limit)
        await ctx.send("Purge success", delete_after=5)
    
    @commands.command()
    @commands.has_permissions(manage_messages=True)
    #clean {num} messages up to 100 from {member}
    async def clean_user(ctx, member: discord.Member, limit: int = 100):
        def check(m):
            return m.author == member

        deleted = await ctx.channel.purge(limit=limit, check=check)
        await ctx.send(f'Deleted {len(deleted)} messages from {member.mention}.', delete_after=5)
    
    #Open up or close down the profanity checker
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def profanity_trigger(self, ctx, switch: bool=False):
        config = load_guild_config(ctx.guild.id)
        if switch is True:
            config["profanity_switch"] = 1
        else:
            config["profanity_switch"] = 0
        save_guild_config(ctx.guild.id, config)
    
    async def apply_timeout(self, user: discord.Member, minutes: int):
        await user.timeout(timedelta(minutes=minutes))

    #Currently only for 
    @commands.Cog.listener()
    async def on_message(self, message):
        guild_config = load_guild_config(message.guild.id)
        if message.author == self.bot.user:
            return
        #on message profanity checker
        if guild_config["profanity_switch"] == 1:
            if predict([message.content])[0] == 1:
                config = load_user_config(message.guild.id, message.author.id)
                await message.delete()
                #To input database right here store which guild which user and how many counts in sqlite
                await self.apply_timeout(message.author, 3)
                if message.author.top_role >= self.bot.user.author.top_role:
                    await message.channel.send(f"You can only moderate members below your role")         
                await message.channel.send(f'{message.author.mention} used bad words. 3 min TIMEOUT applied! :3')
                await message.channel.send('Please keeping the rule otherwise will be auto kicked out!!!')
                config["profanity_count"] += 1
                save_user_config(message.author.id, message.guild.id, config)

    #---TIME OUT SECTION---
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def timeout(self, ctx, user: discord.Member, minutes: int):
        self.apply_timeout(user,minutes)
        ctx.send(f'{minutes} timeout applied to {user}')

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def timeout_remove(self, ctx, user: discord.Member, minutes = 0):
        self.apply_timeout(user,0)
        ctx.send(f'{user} timeout removed')

    @commands.command()
    async def poll(self, ctx, question: str, *options: str):

        if not question:
            await ctx.send("You must input your vote description")
            return

        if len(options) > 10:
            await ctx.send("You can only provide up to 10 options.")
            return

        if len(options) < 2:
            await ctx.send("You must provide at least two options.")
            return
        
        if len(options) == 2:
            reaction = ('👍', '👎')
        else:
            reaction = ('1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣', '🔟')[:len(options)]
        
        embed = discord.Embed(title=question, description= f'{ctx.message.author} create a vote section', color=0xddb6b8)

        for i, option in enumerate(options):
            embed.add_field(name=f"Option {i + 1}", value=f"{reaction[i]} {option}", inline=False)
        
        poll_message = await ctx.send(embed=embed)

        for i in reaction:
            await poll_message.add_reaction(i)

        embed.set_footer(text='Poll ID: {}'.format(poll_message.id))
        await poll_message.edit(embed=embed)

    @commands.command()
    async def poll_result(self, ctx, poll_message_id: int):
        try:
            poll_message = await ctx.fetch_message(poll_message_id)
        except discord.NotFound:
            await ctx.send("Poll message not found.")
            return
        
        if not poll_message.embeds:
            await ctx.send("The provided message ID does not contain an embed.")
            return
        
        reactionList = ('👍', '👎', '1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣', '🔟')
        vote_result = {}
        embed = poll_message.embeds[0]

        for reaction in poll_message.reactions:
            if reaction.emoji in reactionList:
                # Subtract bot's own reaction
                vote_result[reaction.emoji] = reaction.count - 1
        
        results = ""

        for field in embed.fields:
            emoji = field.value.split()[0]
            results += f'\n{field.value} has {vote_result.get(emoji)} votes\n'

        await ctx.send(f"Poll results: {embed.title}\n {results}")

    @commands.command()
    @commands.has_permissions(manage_channels=True)
    async def set_trigger_channel(self, ctx, channel: discord.VoiceChannel):
        config = load_guild_config(ctx.guild.id)
        config['trigger_channel'] = channel.id
        if config['trigger_channel'] is not None:
            category = discord.utils.get(ctx.guild.categories, name="Temporary Channels")
            if category is None:
                await ctx.guild.create_category("Temporary Channels")
        save_guild_config(ctx.guild.id, config)
        await ctx.send(f'Trigger Channel for temporary voice channel creation set to {channel}')

    #auto create a temporary channel for user while joining certain channel
    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        #read the trigger channel id from database and set the channel name 
        channel_name = f'{member.display_name}\'s temp channel'
        trigger_channel_id = load_guild_config(member.guild.id)['trigger_channel']
        #check if there is trigger id or not
        if trigger_channel_id is None:
            print("Trigger Channel is None")
            return

        if after.channel and after.channel.id == trigger_channel_id:
            category = discord.utils.get(member.guild.categories, name="Temporary Channels")
            new_channel = await member.guild.create_voice_channel(name=channel_name, category=category)
            await member.move_to(new_channel)

        if before.channel and before.channel.category.name == "Temporary Channels":
            if len(before.channel.members) == 0:
                await before.channel.delete()

async def setup(bot):
    await bot.add_cog(general(bot))