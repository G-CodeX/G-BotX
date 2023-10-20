import asyncio
import os
import discord
from discord.ext import commands
import Config 
import time
intents = discord.Intents.all()
bot = commands.Bot(command_prefix= ".", intents= intents)

# TimeStamp
time_ = time.localtime()
timestamp = f"[{time_.tm_hour}:{time_.tm_min}:{time_.tm_sec}]       "

async def load_cogs():
    for filename in os.listdir("./Cogs"):
        if filename.startswith("__py"):
            return
        if filename.endswith(".py"):
            await bot.load_extension(f"Cogs.{filename[:-3]}")
        PrintEx(f"Loaded Cogs: {filename[:-3]}")
    return True

def PrintEx(string: str):
    print(f"{timestamp}{string}")
    return


def write_log(log: str):
    """
    Log function. You can print and write any log in client.log
    Ex: write_log("Bot Activated.") {First it write "Bot Activated" in the Client.log then it will print "Bot Activated" in the consol}
    """
    try: # {try:, except:} this is a normal error handeling function
        with open(Config.LOG_PATH, "a+t") as lw: # with function with grab the open module and access the client.log
            lw.write(f"{timestamp}{log}\n")
            return print(f"{timestamp}{log}")
    except Exception as e: # Exception contain the error and "as e" means it's defined by "e"
        raise print(f"{timestamp}{e}")

@bot.event
async def on_ready():
    PrintEx(f"{bot.user.name} is activated.")

    try: # Sync all slash(/) commands. Must needed
        synced = await bot.tree.sync()
        PrintEx(f"{bot.user.name} has synced {len(synced)} command(s)")
    except Exception as e:
        PrintEx(f"I Cannot sync any command(s) because of {e}")
    write_log(f"{bot.user.name} is activated.") # Simple Log write

async def main():
    await load_cogs()
    await bot.start(token= Config.TOKEN, reconnect= True)

asyncio.run(main())