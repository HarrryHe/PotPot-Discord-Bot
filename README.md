![License](https://img.shields.io/github/license/HarrryHe/PotPot-Discord-Bot?label=License) ![Version](https://img.shields.io/github/v/release/HarrryHe/PotPot-Discord-Bot?label=Release&color=red) <a href="https://discord.gg/NQ6SDsEc"><img src="https://img.shields.io/discord/1271308212406059069?label=Discord&logo=discord&color=blue"></a>
# PotPot Discord Bot
PotPot is an open-source, integrated discord bot that includes 20+ server management commands to effectively manage your server, supports basic music playback from youtube, and offers a variety of fun mini-games, such as Russian Roulette, Trivia, and Number Guessing.

**My Website**: [https://harrryhe.github.io/harry.github.io](https://harrryhe.github.io/harry.github.io)  
**Contact Me**: [harry.he@temple.edu](harry.he@temple.edu)

# Setup

## Prerequisites
Internet  
Download ffmpeg (if possible)  
Python 3.9 or later  
Running `pip install -r requirements.txt` to install all required packages  
Create `.env` file  
Optional: VSCode

## Step 1: Customize Your Discord Bot

> 1. Create your Discord Bot at [Discord Developer Portal](https://discord.com/developers/applications)
- Log in to your Discord account.
- Click on `New Application` to create a new bot.
- Give your bot a name and click `Create.`
- In the left-hand menu, select `Bot` and then click on `Add Bot` to create the bot user.
- Confirm by clicking `Yes, do it!` if prompted.  

> 2. Configure Bot Settings (Under `Bot` Section)
- Token: Copy the bot token. Do not share this token publicly as it grants control over your bot.
- Enable All Intents.

> 3. Invite your Bot under `OAuth2 URL Generator`
- Select `bot`.
- Select `Administrator`.
- Copy, paste, and click your generated url.


## Step 2: Run Discord Bot Script

1. Before running our python script, copy your bot token into `.env` file as `DISCORD_BOT_TOKEN=Your Bot Token`.
2. Double check all packages are properly imported and installed.
3. Run `init.py` inside `cogs/configs` folder.
4. After running `init.py`, run `bot.py`.
5. Have fun.  
  
For more information about PotPot commands, send `-help` in your server while the bot is running.

# Commands
## Greetings Cog
- `-ping` Return the bot's latency in milliseconds.  
- `-welcome [setMessage/setChannel/removeChannel] [Contents]` Set welcoming message/channel or removes welcoming message channel.
- `-leave [setMessage/setChannel/removeChannel] [Contents]` Set leaving message/channel or removes leaving message channel.  

## Games Cog
The bot features a daily task system where users can catch animals that have escaped from the zoo to earn points. The game includes a ranking system that displays the user's points. Animals escape at random times, and users are notified when an escape occurs. The animals are categorized into different levels, each with a corresponding point value: Common (10 pts), Uncommon (20 pts), Rare (30 pts), Very Rare (40 pts), and Legendary (50 pts).  
***Note: This feature requires the bot to be deployed and kept online 24/7***.
- `-set_quest_channel [#channel name (text channel)]` Set daily game system channel for the guild.
- `-catch` Catch animals that were announced as escaped within approximately 30 minutes.
- `-roll [side number (>=3)]` Roll a {number}>= 3 sides dice.
- `-flip` Flip a coin.
- `-NumGuessGame` Start a guessing number game with buttons.
- `-RockPaperScissor` Start a rock paper scissor game.
- `-RussianRoulette` Start a Russian Roulette game.
- `-triviahelp` List trivia question categories ID.
- `-Trivia [categories ID]` Start a daily Trivia Question game.  

## General/Management Cog
- `-help` Show help menu.
- `-info` Show Guild information.
- `-clean [num/limit]` Clear {num/limit} of messages (Note: If only send `-clean` will let bot clean 100 messages as default value of limit).
- `-clean_user [@discord.member] [num/limit]` Clear certain {user} {num} of messages.
- `-profanity_trigger [please only input True/False]` Enable/disable profanity check (sensitive words will be prohibited, and users who send them will receive a 2-minute timeout).
- `-timeout [@discord.member] [minutes]` Timeout a {user} for {minutes}.
- `-timeout_remove [@discord.member]` Remove timeout of a {user}.
- `-poll [must be a string: "question"] [opt1] [opt2] ... [opt10]` Start a poll (Note: option number must be <= 10).
- `-poll_result [poll_message_id]` Show certain poll result by inputting poll message ID.
- `-set_trigger_channel [#discord.VoiceChannel]` Set the entry channel for temporary voice channel creation. When a user joins this specific channel, the bot will automatically create a temporary voice channel for them.
- `-lock_channel [#discord.TextChannel]` Lock a text channel.
- `-unlock_channel [#discord.TextChannel]` Unlock a text channel.
- `-create_role [name]` Create a role tag.
- `-add_role [@discord.Member] [discord.role]` Add {user} to a {role}.
- `-remove_role [@discord.Member] [discord.role]` Remove {user} from a {role}.
- `-prune [days]` Detect inactive members around {days}.  

## Music Cog
- `-join_vc` Invite bot to voice channel.
- `-leave_vc` Remove bot from voice channel and delete queue.
- `-play [search keywords]` Play a song.
- `-pause` Pause a song.
- `-resume` Resume a song.
- `-skip` Skip the current song.
- `queue` Show queue information.

## Hidden Commands (for test and develop purposes)
- `-load [extension]`
- `-unload [extension]`
- `-reload [extension]`

## Other
If you'd like to contribute, please contact me via email, or you can simply fork my project and submit a pull request. Thank you!



