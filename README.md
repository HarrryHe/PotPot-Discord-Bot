Currently Under Constructed

@discord.ui.button(label="Stop", style=discord.ButtonStyle.red)
    async def stop(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.edit_message(content="Game Canceled.", view=None)

        for category, category_id in categories.items():
            print(f"Category: {category}, ID: {category_id}")
            await ctx.send(f"Category: {category}, ID: {category_id}")