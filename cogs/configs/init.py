import sqlite3

#You only have to run it once when you finish setting up the database
conn = sqlite3.connect('cogs/configs/configurations.db')
cursor = conn.cursor()

#create new table for it
cursor.execute('''
CREATE TABLE IF NOT EXISTS guild_configs (
    guild_id INTEGER PRIMARY KEY,
    profanity_switch INTEGER,
    auto_role_switch INTEGER,
    welcome_message TEXT,
    welcome_channel TEXT,
    leave_message TEXT,
    leave_channel TEXT
)
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS user_configs (
        user_id INTEGER PRIMARY KEY,
        guild_id INTEGER,
        profanity_count INTEGER,
        inactive_count INTEGER,
        FOREIGN KEY (guild_id) REFERENCES guild_configs (guild_id)
    )
    ''')

conn.commit()
conn.close()

print("Database initialized successfully.")