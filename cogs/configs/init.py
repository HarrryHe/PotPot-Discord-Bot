import sqlite3

#You only have to run it once when you finish setting up the database
conn = sqlite3.connect('cogs/configs/configurations.db')
cursor = conn.cursor()

#create new table for it
cursor.execute('''
CREATE TABLE IF NOT EXISTS greeting_configs (
    guild_id INTEGER PRIMARY KEY,
    welcome_message TEXT,
    welcome_channel TEXT,
    leave_message TEXT,
    leave_channel TEXT
)
''')

conn.commit()
conn.close()

print("Database initialized successfully.")