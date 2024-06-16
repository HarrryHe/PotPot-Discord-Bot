Currently Under Constructed

@discord.ui.button(label="Stop", style=discord.ButtonStyle.red)
    async def stop(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.edit_message(content="Game Canceled.", view=None)

        for category, category_id in categories.items():
            print(f"Category: {category}, ID: {category_id}")
            await ctx.send(f"Category: {category}, ID: {category_id}")


miona
can use as a reference
Commands:

General

/help - List all of the available commands for the bot

/premium - Purchase premium.

/avatar [user] - Get avatar of a person.

/banner [user] - Get banner of a person.

/match  - Get two matcing profile pictures or banners.

/pfp  - Sends an image with the desired type.

/stock - See how many pictures are in our library.

Greeting

/welcome setmessage - Edit the welcome message.

/welcome setchannel  - Set the welcome channel.

/welcome removechannel - Stops sending welcome messages in a channel.

/welcome placeholders - Show all placeholders that can be used.

/welcome test - Send a test welcome message.

/leave setmessage - Edit the leave message.

/leave setchannel  - Set the leave channel.

/leave removechannel - Stops sending leave messages in a channel.

/leave placeholders - Show all placeholders that can be used.

/leave test - Send a test leave message.

/poj start  [channel] - Pings user on join.

/poj stop [channel] - Stop pining on join.

AutoPost

/autopfp start  [channel] - Automatically sends an images in the channel.

/autopfp stop [channel] - Remove AutoPFP feature from a channel.

/autopfp list - List all active autopfp channels.

/automeme start  [channel] - Automatically sends memes in the channel.

/automeme stop [channel] - Remove AutoMeme feature from a channel.

Moderation

/ban  [time] [reason] - Ban someone from the server.

/unban  [reason] - Unban a member.

/softban  [reason] - Kicks a user from the server and deletes a days worth of their messages.

/kick  [reason] - Kick a member from the server.

/mute  [time] [reason] - Prevent user from sending messages.

/unmute  [reason] - Unmute a member.

/warn  [reason] - Warn a member.

/clear  [filter] - Bulk clear messages from a channel.

/slowmode  [channel] - Change the slowmode duration of a channel.

/lockdown [time] - Lock down the current channel.

/case  - View informations about a punishment case.

/mod-logs  - Set the moderation logs channel.

/punishments [user] - Show the punishments of a user

/muted-role [role] - Creates a muted role, or sets an existing role to use.

Roles

/auto-role add  - Adds role to the auto-role list.

/auto-role remove  - Removes role from the auto-role list.

/auto-role list - View all roles from auto-role list.

/mass-role add   - Add a role to a single member or all members in a role.

/mass-role remove   - Remoove a role from a single member or all members in a role.

/mass-role stop - Stop a running mass-role action.

/mass-role status - See the status of a mass-role action.


def load_config(guild_id):
    file_path = f'cogs/configs/{guild_id}.json'
    if os.path.isfile(file_path):
        f = open(file_path, 'r')
        return json.load(f)
    else:
        return {
            "welcome_message": "Welcome to the server, {user}!",
            "welcome_channel": None,
            "leave_message": "Goodbye, {user}!",
            "leave_channel": None
        }
        
def save_config(guild_id, config):
    file_path = f'cogs/configs/{guild_id}.json'
    with open(file_path, mode='w') as f:
        json.dump(config, f, indent=4)