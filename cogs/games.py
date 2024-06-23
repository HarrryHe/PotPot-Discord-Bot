import discord
from discord.ext import commands
from header import Cog_Extension
from discord.ui import Button, View
import requests
import random
import datetime

class games(Cog_Extension):
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

async def setup(bot):
    await bot.add_cog(games(bot))
