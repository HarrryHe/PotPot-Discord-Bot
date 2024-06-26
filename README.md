@discord.ui.button(label="Pull The Trigger", style=discord.ButtonStyle.green)
    async def trigger_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        #get the embed from the content
        await asyncio.sleep(1)
        embed = interaction.message.embeds[0]

        user_result = self.my_gun[0]
        bot_result = self.bot_gun[0]
        #when user lose
        if user_result == 'bullet' and bot_result == 'empty':
            embed.set_field_at(index=0, name=f'{interaction.user} 💀💥', value='status: DEAD', inline=False)
            embed.set_field_at(index=2, name='Result Board', value='User lose, Bot win!', inline=False)
            await interaction.response.edit_message(embed=embed, view=None)
            await interaction.followup.send('Well, partner, looks like this ain\'t your lucky day. But the West always has a second chance!')
        elif user_result == 'empty' and bot_result == 'bullet':
            embed.set_field_at(index=1, name=f'{interaction.client.user.name} 💀💥', value='status: DEAD', inline=False)
            embed.set_field_at(index=2, name='Result Board', value='User win, Bot lose!', inline=False)
            await interaction.response.edit_message(embed=embed, view=None)
            word = random.choice(['Looks like Lady Luck is on your side, partner!', 'You\'re as lucky as a horse with a golden horseshoe!'])
            await interaction.followup.send(f'YOU WIN! {word}')
        elif user_result == 'bullet' and bot_result == 'bullet':
            embed.set_field_at(index=0, name=f'{interaction.user} 💀💥', value='status: DEAD', inline=False)
            embed.set_field_at(index=1, name=f'{interaction.client.user.name} 💀💥', value='status: DEAD', inline=False)
            embed.set_field_at(index=2, name='Result Board', value='Tie!', inline=False)
            await interaction.response.edit_message(embed=embed, view=None)
            await interaction.followup.send('A standoff like this deserves another round. Are you ready to duel again?')
        else:
            embed.set_field_at(index=2, name='Result Board', value='Both Survived! Good luck on next shot!', inline=False)
            await interaction.response.edit_message(embed=embed)
            goodluck = random.choice(['No bullet this time, partner. Your luck\'s holding strong!', 'Another empty chamber. Fortune favors the bold, keep going!', 'You dodged the bullet, just like a true gunslinger!'])
            followup_message = await interaction.followup.send(goodluck)
            await asyncio.sleep(2)
            await followup_message.delete()  

        self.my_gun.pop(0)
        self.bot_gun.pop(0)
        await asyncio.sleep(1)