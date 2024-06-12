import discord
from discord.ext import commands
from header import Cog_Extension
from discord.ui import Button, View
import random

numGuessing_loseCount = 0

class games(Cog_Extension):
    @commands.command()
    async def NumGuessGame(self, ctx):
        """Start a guessing game with buttons."""
        view = GuessingGameView()
        await ctx.send("Click a button to guess the number between 0 and 9!", view=view)



# --- Num Guessing Game ---

#This is to show the view in discord
class GuessingGameView(View):
    def __init__(self):
        super().__init__()
        self.lose_count = 0
        self.targetNumber = random.randint(0, 9)
        for i in range(10):
            self.add_item(numButton(i, self.targetNumber))
    
    @discord.ui.button(label="Stop", style=discord.ButtonStyle.red)
    async def stop(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.edit_message(content="Game Canceled.", view=None)

#num button instances
class numButton(Button):
    def __init__(self, number, targetNumber):
        super().__init__(label=str(number), style=discord.ButtonStyle.green, emoji="❓")
        self.number = number
        self.targetNumber = targetNumber

    async def callback(self, interaction: discord.Interaction):
        global numGuessing_loseCount
        if self.number == self.targetNumber:
            await interaction.response.edit_message(content=f"Congratulations! You guessed the correct number: {self.number}", view=None)
        else:
            numGuessing_loseCount += 1
            if numGuessing_loseCount >= 3:
                await interaction.response.edit_message(content=f"Sorry, you've guessed wrong 3 times. The correct number was {self.targetNumber}. Game over!", view=None)
                numGuessing_loseCount = 0
            else:
                await interaction.response.send_message(f"Sorry, {self.number} is not the correct number. Try again!", ephemeral=True)

async def setup(bot):
    await bot.add_cog(games(bot))