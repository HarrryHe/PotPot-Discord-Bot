![License](https://img.shields.io/github/license/HarrryHe/PotPot-Discord-Bot?label=License) ![Version](https://img.shields.io/github/v/release/HarrryHe/PotPot-Discord-Bot?label=Release) <a href="https://discord.gg/NQ6SDsEc"><img src="https://img.shields.io/discord/1271308212406059069?label=Discord&logo=discord&color=blue"></a>
# PotPot Discord Bot
PotPot is an open-source, integrated discord bot that includes 20+ server management commands to effectively manage your server, supports basic music playback from youtube, and offers a variety of fun mini-games, such as Russian Roulette, Trivia, and Number Guessing.

**My Website**: [https://harrryhe.github.io/harry.github.io](https://harrryhe.github.io/harry.github.io)  
**Contact Me**: [harry.he@temple.edu](harry.he@temple.edu)

# Setup

## Prerequisite
Internet  
Python 3.9 or later  
Running `pip3 install -r requirements.txt` to install all required packages
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

1. Before running our python script, copy your bot token into `env` as `DISCORD_BOT_TOKEN=Your Bot Token`.
2. Double check all packages are properly imported and installed.
3. Run `init.py` inside `cogs/configs` folder.
4. After running `init.py`, run `bot.py`.
5. Have fun.  
For more information on PotPot commands, send `-help` under your server while the script is running.


