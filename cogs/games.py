import discord
from discord.ext import commands, tasks
from header import Cog_Extension
from discord.ui import Button, View
import asyncio
import requests
import random
import datetime
import json
from .helper import load_guild_config, save_guild_config, load_user_config, save_user_config

lock = asyncio.Lock()
utc = datetime.timezone.utc

class games(Cog_Extension):
    def __init__(self, bot):
        super().__init__(bot)
        self.guild_tasks = None
        self.caught_user = set()
        self.bot.loop.create_task(self.announce_animal())
        self.rank.start()

    @commands.command()
    @commands.has_permissions(manage_channels=True)
    async def set_quest_channel(self, ctx, channel: discord.TextChannel):
        config = await load_guild_config(ctx.guild.id)
        config['quest_channel'] = channel.id
        await save_guild_config(ctx.guild.id, config)
        await ctx.send(f"Quest channel set to {channel.mention}")

    def select_animal(self):
        try:
            f = open('utils/animal.json', mode='r', encoding='utf-8')
            data = json.load(f)
        except Exception as e:
            print(f"An error occurred: {e}")
            return
        choice = random.uniform(1,100)
        if choice <= 60:
            category = "common"
        elif choice <= 80:
            category = "uncommon"
        elif choice <= 91:
            category = "rare"
        elif choice <= 99.5:
            category = "very_rare"
        else:
            category = "legendary"
        return random.choice(list(data[category].items()))

    @tasks.loop(time=datetime.time(hour=8, minute=30, tzinfo=utc))
    async def rank(self):
        await self.bot.wait_until_ready()
        print("Rank is running")
        for guild in self.bot.guilds:
            guild_config = await load_guild_config(guild.id)
            quest_channel_id = guild_config.get('quest_channel')
            if quest_channel_id:
                channel = self.bot.get_channel(quest_channel_id)
                members = guild.members
                user_points = []
                #store all the members from the guild
                for member in members:
                    if member.bot:
                        continue
                    user_config = await load_user_config(guild.id, member.id)
                    user_point = user_config["user_point"]
                    user_points.append((member, user_point))
                
                #sort all the user_points in reverse order lambda meaning that it is a non-name temporary function usually with one line
                #it is sorted by user_point
                user_points.sort(key=lambda x: x[1], reverse=True)

                embed = discord.Embed(title="User Rank Board", description='Presenting rank information 8:30am everyday', timestamp=datetime.datetime.now(), color=0xddb6b8)
                for i, (member, points) in enumerate(user_points, start=1):
                        embed.add_field(name=f"{i}. {member.name}", value=f"{points} points", inline=False)
                await channel.send(embed=embed)

    async def announce_animal(self):
        await self.bot.wait_until_ready()
        while not self.bot.is_closed():
            #wait till the midnight to start this mission
            now = datetime.datetime.now()
            next_midnight = now.replace(hour=0, minute=0, second=0, microsecond=0) + datetime.timedelta(days=1)
            wait_time = (next_midnight - now).total_seconds()
            await asyncio.sleep(wait_time)

            time_intervals = []
            #cut the 24hrs into 10 periods
            time_period = 24 * 60 * 60 // 10
            #so we are planning to announce the animal escaping announcement 10 times a day randomly
            #generated random time in each period
            for i in range(10):
                start = i * time_period
                end = (i+1) * time_period - 1
                time_intervals.append(random.randint(start, end))
            time_intervals.sort()
            #Test
            print(time_intervals)

            #start interpret each announcement using for loop (total 10)
            for interval in time_intervals:
                now = datetime.datetime.now()
                target_time = now.replace(hour=0, minute=0, second=0, microsecond=0) + datetime.timedelta(seconds=interval)
                wait_time = (target_time - now).total_seconds()

                if wait_time < 0:
                    wait_time = 0
                await asyncio.sleep(wait_time)

                #initialization
                animal, points = self.select_animal()
                self.guild_tasks = {'animal': animal, 'points': points, 'time': datetime.datetime.now()}
                #make sure to clear all the users in the set that catches last animal
                self.caught_user.clear()

                #in each guilds
                for guild in self.bot.guilds:
                    config = await load_guild_config(guild.id)
                    quest_channel_id = config.get('quest_channel')
                    if quest_channel_id:
                        channel = self.bot.get_channel(quest_channel_id)
                        if channel:
                            await channel.send(f"An animal has escaped! It's a {animal}. Type \'-catch\' to catch it and earn {points} points! You have 30 minutes to catch it.")

    @commands.command()
    async def catch(self, ctx):
        guild_id = ctx.guild.id
        if self.guild_tasks:
            #avoid user repeating receive points
            if ctx.author.id in self.caught_user:
                await ctx.send("You have already caught this animal!")
                return
            #get which animal and what time and how many points user can earn
            animal, points, time = self.guild_tasks['animal'], self.guild_tasks['points'], self.guild_tasks['time']
            count_time = datetime.datetime.now() - time
            if count_time <= datetime.timedelta(minutes=30):
                user_config = await load_user_config(ctx.guild.id, ctx.author.id)
                user_config['user_point'] += points
                await save_user_config(ctx.author.id, ctx.guild.id, user_config)
                self.caught_user.add(ctx.author.id)
                await ctx.send(f"You caught {animal}! You earned {points} points! Your total points are now {user_config['user_point']}.")
            else:
                await ctx.send("The animal has escaped, you took too long!")
                self.guild_tasks = None

        else:
            await ctx.send("There is no escaping animal to catch right now")

    @commands.command()
    async def roll(self, ctx, side: int = 6):
        """Roll a {number}>= 3 sides dice."""
        if side < 3:
            await ctx.send("the sides of the dice must be above or equal to 3")
        else:
            result = random.randint(1, side)
            await ctx.send(f"result: {result}")

    @commands.command()
    async def flip(self, ctx):
        """Flip a coin."""
        result = random.choice(['heads', 'tails'])
        await ctx.send(f"result: {result}")

    @commands.command()
    async def NumGuessGame(self, ctx):
        """Start a guessing game with buttons."""
        view = GuessingGameView()
        await ctx.send("Click a button to guess the number between 0 and 9", view=view)

    @commands.command()
    async def RockPaperScissor(self, ctx):
        """Start a rock paper scissor game."""
        user = ctx.author
        choices = ["🖐️", "✌️", "✊"]
        choice = random.choice(choices)
        await ctx.send(f'{user.mention}, You choose: ')
        await ctx.send(f'{choice}')

    @commands.command()
    async def RussianRoulette(self, ctx):
        loading_bar = ""
        empty_bar = "░░" * 5
        temp_count = 5
        embed = discord.Embed(
        title='Russian Roulette Game', 
        description=f'Loading Bullet for -user- and -bot-\n[{loading_bar}{empty_bar}]', 
        color=0xddb6b8
    )
        embed.set_image(url="https://media1.tenor.com/m/zHJNFjLxqHcAAAAC/cdd.gif")
        message = await ctx.send(embed=embed)
        #these are actually useless commands but making the UI cooler
        for i in range(5):
            await asyncio.sleep(1)
            loading_bar += "██"
            temp_count -= 1
            empty_bar = "░░" * temp_count
            embed.description=f'Loading Bullet for -user- and -bot-\n[{loading_bar}{empty_bar}]'
            await message.edit(embed=embed)

        embed.description=f'bullet loaded into revolver\nnow spining cylinder...'
        await message.edit(embed=embed)
        await asyncio.sleep(3)
        # Update description and remove image
        embed.set_image(url=None)
        embed.description='-User- VS -Bot-'
        embed.insert_field_at(index=0, name=f'{ctx.author} 🤠', value='status: survive', inline=False)
        embed.insert_field_at(index=1, name=f'{self.bot.user.name} 🤖', value='status: survive', inline=False)
        embed.insert_field_at(index=2, name='Result Board', value='User\'s Turn', inline=False)
        view=RussianRouletteView()
        await message.edit(embed=embed, view=view)

    @commands.command()
    async def Trivia(self, ctx, *, category_choice: int = None):
        """Start a trivia game."""
        if category_choice != None:
            question_selected = get_trivia(1, category_choice)
            category = question_selected['category']
            question = question_selected['question']
            options = question_selected['options']
            correct_answer = question_selected['correct_answer']
            view = TriviaView(correct_answer, options)
            await ctx.send(f'Category: {category}\nQuestion: {question}', view=view)
        else:
            print("Cannot fetch data from database")
            return

    @commands.command()
    async def triviaHelp(self, ctx):
        """List trivia question categories ID"""
        embed=discord.Embed(title="Trivia Help Menu", description="List all the trivia question categories you need for -Trivia [category ID]", color=0xddb6b8, timestamp=datetime.datetime.now())
        embed.set_author(name="PotPot")
        categories = [
            ("General Knowledge", 9),
            ("Entertainment: Books", 10),
            ("Entertainment: Film", 11),
            ("Entertainment: Music", 12),
            ("Entertainment: Musicals & Theatres", 13),
            ("Entertainment: Television", 14),
            ("Entertainment: Video Games", 15),
            ("Entertainment: Board Games", 16),
            ("Science & Nature", 17),
            ("Science: Computers", 18),
            ("Science: Mathematics", 19),
            ("Mythology", 20),
            ("Sports", 21),
            ("Geography", 22),
            ("History", 23),
            ("Politics", 24),
            ("Art", 25),
            ("Celebrities", 26),
            ("Animals", 27),
            ("Vehicles", 28),
            ("Entertainment: Comics", 29),
            ("Science: Gadgets", 30),
            ("Entertainment: Japanese Anime & Manga", 31),
            ("Entertainment: Cartoon & Animations", 32),
        ]
        for name, id in categories:
            embed.add_field(name=f"{name}", value=f"ID: {id}", inline=False)
        await ctx.send(embed=embed)

# --- Num Guessing Game ---
# This is to show the view in discord
class GuessingGameView(View):
    def __init__(self):
        super().__init__()
        self.targetNumber = random.randint(0, 9)
        self.lose_count = 0
        for i in range(10):
            self.add_item(numButton(i, self))
        self.add_item(stopButton())

# stop button class
class stopButton(Button):
    def __init__(self):
        super().__init__(label="Stop", style=discord.ButtonStyle.red)
    
    async def callback(self, interaction: discord.Interaction):
        await interaction.response.edit_message(content="Game Canceled.", view=None)

# num button class
class numButton(Button):
    def __init__(self, number, game_view):
        super().__init__(label=str(number), style=discord.ButtonStyle.green, emoji="❓")
        self.number = number
        self.game_view = game_view

    async def callback(self, interaction: discord.Interaction):
        if self.number == self.game_view.targetNumber:
            await interaction.response.edit_message(content=f"Congratulations! You guessed the correct number: {self.number}", view=None)
        else:
            self.game_view.lose_count += 1
            if self.game_view.lose_count >= 3:
                await interaction.response.edit_message(content=f"Sorry, you've guessed wrong 3 times. The correct number was {self.game_view.targetNumber}. Game over!", view=None)
            else:
                await interaction.response.edit_message(content=f"Sorry, {self.number} is not the correct number. Try again!")

# --- Trivia Game ---
#Get the category, but right now it is abandoned
def get_trivia_categories():
    url = "https://opentdb.com/api_category.php"
    categories = {}
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        for category in data["trivia_categories"]:
            categories[category["name"]] = category["id"]
    else:
        print(f'{response} Connection Failed.')
    return categories

#get trivia question by using requests, then using .json to make it readable
def get_trivia(amount, category_choice):
    url = f"https://opentdb.com/api.php?amount={amount}&category={category_choice}"
    response = requests.get(url)
    data = response.json()
    question_selected = {}
    #Although here can be implemented more easier but right now just keep it
    if data["response_code"] == 0:
        info = data["results"][0]
        category = info['category']
        question = info['question']
        correct_answer = info['correct_answer']
        incorrect_answers = info['incorrect_answers']
        options = [correct_answer] + incorrect_answers
        #shuffle the answer to make sure the answers are random
        random.shuffle(options)

        question_selected = {
            'category': category,
            'question': question,
            'correct_answer': correct_answer,
            'incorrect_answers': incorrect_answers,
            'options': options
        }
    else:
        print('Connection Failed.')

    return question_selected

#Trivia Button view
class TriviaView(View):
    def __init__(self, correct_answer, options):
        super().__init__()
        self.correct_answer = correct_answer
        self.options = options
        for i in self.options:
            self.add_item(TriviaButton(i, self.correct_answer))

#Trivia Button callback when click the button
class TriviaButton(Button):
    def __init__(self, label, is_correct):
        super().__init__(label=str(label), style=discord.ButtonStyle.green, emoji="🫡")
        self.label = label
        self.is_correct = is_correct

    async def callback(self, interaction: discord.Interaction):
        if self.label == self.is_correct:
            await interaction.response.edit_message(view=None)
            await interaction.followup.send(f"Congratulations! You are correct! It is {self.is_correct}")
        else:
            await interaction.response.edit_message(view=None)
            await interaction.followup.send(f"Oops! The correct answer is {self.is_correct}")

# --- Russian Roulette View ---
class RussianRouletteView(View):
    def __init__(self):
        super().__init__()
        self.gun = ['empty', 'empty', 'empty', 'empty', 'empty', 'bullet']
        random.shuffle(self.gun)

    @discord.ui.button(label="Pull The Trigger", style=discord.ButtonStyle.green)
    async def trigger_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = interaction.message.embeds[0]

        #disable the button for amount of time
        button.disabled = True
        await interaction.response.edit_message(embed=embed, view=self)

        #user's turn
        result = self.gun[0]
        if result == 'bullet':
            embed.set_field_at(index=0, name=f'{interaction.user} 💀💥', value='status: DEAD', inline=False)
            embed.set_field_at(index=2, name='Result Board', value='User lose, Bot win!', inline=False)
            await interaction.edit_original_response(embed=embed, view=None)
            await interaction.followup.send('You Lose! Well, partner, looks like this ain\'t your lucky day. But the West always has a second chance!')
            return
        else:
            followup_message = await interaction.followup.send('Phew! That was close, cowboy! Keep riding high! It\'s bot turn now.')
            await asyncio.sleep(2)
            await followup_message.delete()

        embed.set_field_at(index=2, name='Result Board', value='Bot\'s Turn. Bot thinking...', inline=False)
        await interaction.edit_original_response(embed=embed, view=self)

        random.shuffle(self.gun)
        result = self.gun[0]
        #Bot's turn
        #Bot pretend to think
        await asyncio.sleep(2)
        if result == 'bullet':
            embed.set_field_at(index=1, name=f'{interaction.client.user.name} 💀💥', value='status: DEAD', inline=False)
            embed.set_field_at(index=2, name='Result Board', value='Bot lose, User win!', inline=False)
            await interaction.edit_original_response(embed=embed, view=None)
            await interaction.followup.send('You Win! The West is tough, but so are you. Congratulations on your victory!')
            return
        else:
            followup_message = await interaction.followup.send('The bot missed its shot. It\'s your turn now, partner!')
            await asyncio.sleep(2)
            await followup_message.delete()
        embed.set_field_at(index=2, name='Result Board', value='User\'s Turn', inline=False)

        #Giving the button back to the user
        button.disabled = False
        await interaction.edit_original_response(embed=embed, view=self)
        random.shuffle(self.gun)
    
    @discord.ui.button(label="Quit Like A Coward", style=discord.ButtonStyle.red)
    async def quit_callback(self, interaction: discord.Interaction, button: discord.ui.Button, ):
        await interaction.response.edit_message(content="Game Canceled.", embed=None, view=None)

async def setup(bot):
    await bot.add_cog(games(bot))