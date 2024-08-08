import sqlite3
import aiosqlite
import asyncio

async def load_guild_config(guild_id):
    async with aiosqlite.connect('cogs/configs/configurations.db') as db:
        async with db.execute('SELECT * FROM guild_configs WHERE guild_id = ?', (guild_id,)) as cursor:
            row = await cursor.fetchone()
            print("cursor fetch succeeded.")
            if row:
                return {
                    "guild_id": row[0],
                    "profanity_switch": row[1],
                    "auto_role_switch": row[2],
                    "welcome_message": row[3],
                    "welcome_channel": row[4],
                    "leave_message": row[5],
                    "leave_channel": row[6],
                    "trigger_channel": row[7],
                    "quest_channel": row[8]
                }
            else:
                return {
                    "guild_id": guild_id,
                    "profanity_switch": 0,
                    "auto_role_switch": 1,
                    "welcome_message": "Welcome to the server, {user}!",
                    "welcome_channel": None,
                    "leave_message": "Goodbye, {user}!",
                    "leave_channel": None,
                    "trigger_channel": None, 
                    "quest_channel": None
                }

#Save Configuration to the sqlite
async def save_guild_config(guild_id, config):
    async with aiosqlite.connect('cogs/configs/configurations.db') as db:
        await db.execute('''
            INSERT OR REPLACE INTO guild_configs (guild_id, profanity_switch, auto_role_switch, welcome_message, welcome_channel, leave_message, leave_channel, trigger_channel, quest_channel)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            guild_id,
            config['profanity_switch'],
            config['auto_role_switch'],
            config['welcome_message'],
            config['welcome_channel'],
            config['leave_message'],
            config['leave_channel'],  
            config['trigger_channel'],
            config['quest_channel']
        ))
        await db.commit()
        print("Database commit succeed")

#user load
async def load_user_config(guild_id, user_id):
    async with aiosqlite.connect('cogs/configs/configurations.db') as db:
        async with db.execute('SELECT * FROM user_configs WHERE guild_id = ? AND user_id = ?', (guild_id, user_id)) as cursor:
            row = await cursor.fetchone()
            print("Cursor fetch succeeded.")
            if row:
                return {
                    "guild_id": row[1],
                    "user_id": row[0],
                    "profanity_count": row[2],
                    "user_point": row[3]
                }
            else:
                return {
                    "guild_id": guild_id,
                    "user_id": user_id,
                    "profanity_count": 0,
                    "user_point": 0
                }
    
async def save_user_config(user_id, guild_id, config):
    async with aiosqlite.connect('cogs/configs/configurations.db') as db:
    
        await db.execute('''
        INSERT OR REPLACE INTO user_configs (user_id, guild_id, profanity_count, user_point)
        VALUES (?, ?, ?, ?)
        ''', (user_id, guild_id, config['profanity_count'], config['user_point']))
        await db.commit()
        print("Database commit succeed")