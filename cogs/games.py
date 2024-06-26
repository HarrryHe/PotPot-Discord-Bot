import discord
from discord.ext import commands
from header import Cog_Extension
from discord.ui import Button, View
import asyncio
import requests
import random
import datetime

lock = asyncio.Lock()

class games(Cog_Extension):

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
        await asyncio.sleep(1)
        embed = interaction.message.embeds[0]
        #disable the button for amount of time
        button.disabled = True
        await interaction.response.edit_message(embed=embed, view=self)

        #user's turn
        result = self.gun[0]
        if result == 'bullet':
            embed.set_field_at(index=0, name=f'{interaction.user} 💀💥', value='status: DEAD', inline=False)
            embed.set_field_at(index=2, name='Result Board', value='User lose, Bot win!', inline=False)
            await interaction.response.edit_message(embed=embed, view=None)
            await interaction.followup.send('Well, partner, looks like this ain\'t your lucky day. But the West always has a second chance!')
            return
        else:
            await interaction.followup.send('Phew! That was close, cowboy! Keep riding high! It\'s bot turn now.')
        embed.set_field_at(index=2, name='Result Board', value='Bot\'s Turn', inline=False)
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
            await interaction.followup.send('The West is tough, but so are you. Congratulations on your victory!')
            return
        else:
            await interaction.followup.send('The bot missed its shot. It\'s your turn now, partner!')
        embed.set_field_at(index=2, name='Result Board', value='User\'s Turn', inline=False)

        #Giving the button back to the user
        button.disabled = False
        await interaction.response.edit_message(embed=embed, view=self)
        await asyncio.sleep(1)
    
    @discord.ui.button(label="Quit Like A Coward", style=discord.ButtonStyle.red)
    async def quit_callback(self, interaction: discord.Interaction, button: discord.ui.Button, ):
        await interaction.response.edit_message(content="Game Canceled.", view=None)
    
async def setup(bot):
    await bot.add_cog(games(bot))
