import os
import discord
from discord.ext import commands
from flask import Flask
import threading

# 创建一个简单的 Flask 应用
app = Flask(__name__)

@app.route("/")
def home():
    return "Bot is running!"

# 启动 Flask 服务器的线程
def run_web_server():
    port = int(os.environ.get("PORT", 5000))  # 获取 PORT 环境变量，默认为 5000
    app.run(host="0.0.0.0", port=port)

# 在后台线程中启动 Web 服务
def start_web_server():
    thread = threading.Thread(target=run_web_server)
    thread.daemon = True
    thread.start()


bot = commands.Bot(command_prefix='-', intents=discord.Intents.all())

@bot.event
async def on_ready():
    print("--Bot is Online--")
    await load_extensions()

@bot.command()
async def load(ctx, extension):
    bot.load_extension(f'cogs.{extension}')
    await ctx.send(f'load {extension} succeed')

@bot.command()
async def unload(ctx, extension):
    bot.unload_extension(f'cogs.{extension}')
    await ctx.send(f'unload {extension} succeed')

@bot.command()
async def reload(ctx, extension):
    bot.reload_extension(f'cogs.{extension}')
    await ctx.send(f'reload {extension} succeed')

async def load_extensions():
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py') and filename != "__init__.py" and filename != "helper.py":
            await bot.load_extension(f'cogs.{filename[:-3]}')

if __name__ == "__main__":
    start_web_server()
    bot.run(os.getenv("DISCORD_BOT_TOKEN"))
