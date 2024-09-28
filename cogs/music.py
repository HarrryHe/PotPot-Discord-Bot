from header import Cog_Extension
import discord
from discord.ext import commands, tasks
from discord.ui import Button, View
import asyncio
import yt_dlp

#set up (Kinda confused on where I can check all the options)
ytdl_format_options = {
    'format': 'bestaudio/best',
    'noplaylist': True,
}

#create youtubeDL instance
ytdl = yt_dlp.YoutubeDL(ytdl_format_options)

class music(Cog_Extension):
    def __init__(self, bot):
        self.bot = bot
        self.queues = {}
        self.current = None
        self.voice_clients = {}

    #add songs into queue
    def add_to_queue(self, guild_id, song):
        if guild_id not in self.queues:
            self.queues[guild_id] = []
        self.queues[guild_id].append(song)

    #call_back function
    async def play_next(self, ctx):

        guild_id = ctx.guild.id

        if guild_id not in self.queues or not self.queues[guild_id]:
            return
        
        #pop the first song from queues' guild list
        song = self.queues[guild_id].pop(0)
        url = song['url']
        title = song['title']

        #let the voice client play the song, and after it finished call the function itself until theres no song left
        source = discord.FFmpegPCMAudio(url, options='-vn')
        ctx.voice_client.play(source, after=lambda e: self.bot.loop.create_task(self.play_next(ctx)))
        await ctx.send(f'Now playing: {title}')
        
    
    #invoke bot into voice channel
    @commands.command(name="join_vc")
    async def join(self, ctx):
        """Invite bot to voice channel"""
        if ctx.author.voice is None:
            await ctx.send("Sorry you are not in a voice channel", delete_after=5)
            return

        else:
            channel = ctx.author.voice.channel
            guild_id = ctx.guild.id
            voice_client = await channel.connect()
            self.voice_clients[guild_id] = voice_client
    
    #disconnect bot from voice channel
    @commands.command(name="leave_vc")
    async def leave(self, ctx):
        """Remove bot from voice channel and delete queue"""
        if ctx.guild.id in self.voice_clients:
            await self.voice_clients[ctx.guild.id].disconnect()
            #delete the queue from [ctx] guild
            del self.voice_clients[ctx.guild.id]
            del self.queues[ctx.guild.id]

    @commands.command(name="play")
    async def play(self, ctx, *, search: str):
        """Play a song"""
        #repeat the 'join' function
        if ctx.author.voice is None:
            await ctx.send("Sorry you are not in a voice channel", delete_after=5)
            return

        elif ctx.author.voice and ctx.guild.id not in self.voice_clients:
            channel = ctx.author.voice.channel
            guild_id = ctx.guild.id
            voice_client = await channel.connect()
            self.voice_clients[guild_id] = voice_client
        
        voice_client = self.voice_clients[ctx.guild.id]

        async with ctx.typing():
            loop = asyncio.get_event_loop()
            data = await loop.run_in_executor(None, lambda: ytdl.extract_info(f"ytsearch:{search}",download=False))
            print(data)
            if 'entries' in data:
                data = data['entries'][0]

            url = data['url']
            title = data['title']
            song = {'url': url, 'title': title}
            uploader = data.get('uploader', 'Unknown')
            description = data.get('description', 'No description available')
            thumbnail = data.get('thumbnail')
            duration = data.get('duration')
            self.add_to_queue(ctx.guild.id, song)

            await ctx.send(f'Added {title} to the queue.')

            if not voice_client.is_playing() and not voice_client.is_paused():
                embed = discord.Embed(title=f"Now Playing: {title}", url=url, description=description, color=0xddb6b8)
                embed.set_author(name=f"Uploaded By: {uploader}")
                embed.set_thumbnail(url=thumbnail)
                embed.add_field(name="Duration", value=duration, inline=False)

                view = View()

                #Pause Button Implementation
                async def pause_button_callBack(interaction: discord.Interaction):
                    await self.pause(ctx)
                    await interaction.response.send_message("Paused the song.", ephemeral=True)

                pauseButton = Button(label="Pause", emoji="⏸️", style=discord.ButtonStyle.red)
                pauseButton.callback = pause_button_callBack
                view.add_item(pauseButton)

                #Resume Button Implementation
                async def resume_button_callBack(interaction: discord.Interaction):
                    await self.resume(ctx)
                    await interaction.response.send_message("Resumed the song.", ephemeral=True)

                resumeButton = Button(label="Resume", emoji="▶️", style=discord.ButtonStyle.green)
                resumeButton.callback = resume_button_callBack
                view.add_item(resumeButton)

                #Skip Button Implementation
                async def skip_button_callback(interaction: discord.Interaction):
                    await self.skip(ctx)
                    await interaction.response.send_message("Resumed the song.", ephemeral=True)

                skipButton = Button(label="Skip", emoji="⏭️", style=discord.ButtonStyle.green)
                skipButton.callback = skip_button_callback
                view.add_item(skipButton)
                
                await ctx.send(embed=embed, view=view)
                await self.play_next(ctx)

    @commands.command(name="pause")
    async def pause(self, ctx):
        """Pause a song"""
        if ctx.guild.id not in self.voice_clients:
            await ctx.send("Bot is not in a voice channel.", delete_after=5)
            return
        
        voice_client = self.voice_clients[ctx.guild.id]
        if voice_client.is_playing():
            voice_client.pause()
            await ctx.send("Paused the current song.")
        else:
            await ctx.send("No audio is playing.", delete_after=5)

    @commands.command(name="resume")
    async def resume(self, ctx):
        """Resume a song"""
        if ctx.guild.id not in self.voice_clients:
            await ctx.send("Bot is not in a voice channel.", delete_after=5)
            return
        
        voice_client = self.voice_clients[ctx.guild.id]
        if voice_client.is_paused():
            voice_client.resume()
            await ctx.send("Resumed the current song.")
        else:
            await ctx.send("The audio is not paused.", delete_after=5)

    @commands.command(name="skip")
    async def skip(self, ctx):
        """Skip the current song"""
        voice_client = self.voice_clients[ctx.guild.id]
        if voice_client and voice_client.is_playing():
            voice_client.stop()
            await ctx.send("Skipped the current song.")
        else:
            await ctx.send("No audio is playing.", delete_after=5)

    #show the current queue
    @commands.command()
    async def queue(self, ctx):
        """Show queue information"""
        queue = self.queues[ctx.guild.id]
        if queue:
            queue_str = '\n'.join([f"{idx + 1}. {song['title']}" for idx, song in enumerate(queue)])
            await ctx.send(f"Current Queue: \n {queue_str}")
        else:
            await ctx.send("The queue is empty.", delete_after=5)


#UI Class Implementation
class playView(View):
    def __init__(self):
        super.__init__()

async def setup(bot):
    await bot.add_cog(music(bot))
