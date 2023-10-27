import os
import discord
from discord.ext import commands
import Config
from Config import PrintEx, write_log
import time
intents = discord.Intents.all()
bot = commands.Bot(command_prefix= ".", intents= intents)


@bot.event
async def setup_hook():
    for filename in os.listdir("./Cogs"):
        if filename.endswith(".py"):
            await bot.load_extension(f"Cogs.{filename[:-3]}")
        PrintEx(f"Loaded Cogs: {filename[:-3]}")

@bot.event
async def on_ready():
    PrintEx(f"{bot.user.name} is activated.")
    try: # Sync all slash(/) commands. Must needed
        synced = await bot.tree.sync()
        PrintEx(f"{bot.user.name} has synced {len(synced)} command(s)")
    except Exception as e:
        PrintEx(f"I Cannot sync any command(s) because of {e}")
    write_log(f"{bot.user.name} is activated.") # Simple Log write


bot.run(token= Config.TOKEN, reconnect= True, log_handler= None)