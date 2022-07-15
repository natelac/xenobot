import sys
import os
import time
import asyncio

from discord.ext import commands
import discord
from dotenv import load_dotenv

# Set constants
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = 'Area 51' # The guild the bot
COMMAND_PREFIX = '!' # Is this still necessary?
LOG_TIME = (60) * 5 # Seconds between logs

# Intents the bot will use
intents = discord.Intents.all()
intents.members = True
intents.presences = True
intents.guilds = True
intents.messages = True
#intents.message_content = True
intents.reactions = True

# Initiallize the bot
bot = commands.Bot(command_prefix=COMMAND_PREFIX, intents=intents)

@bot.event
async def on_ready():
    """Print bot status and start logging."""
    print(f"{bot.user} has connected to Discord!")
    print(f"{bot.user} is connected to the following guild:")
    for guild in bot.guilds:
        print(f"\t{guild.name}(id: {guild.id})")
    print()
    guild = discord.utils.get(bot.guilds, name=GUILD)
    # Start actively logging
    while(True):
        log_guild_statuses(guild)
        await asyncio.sleep(LOG_TIME)

def log_guild_statuses(guild):
    """Log member statuses to file."""
    with open(f"{guild.id}_statuses.log", 'a+') as f:
        for member in guild.members:
            f.write(
                f"{member.id},"
                f"{member.raw_status},{time.time()}\n"
            )

def log_message(msg):
    """Log message to log-file."""
    with open(f"{msg.guild.id}_messages.log", 'a+') as f:
        f.write(
            f"{msg.id},{msg.channel.id},{msg.author.id},"
            f"{msg.content},{time.time()}\n"
        )

# I also need to log deletes? How to store in db?

def log_reaction_add(payload):
    """Log reaction to log-file."""
    # with open(f"{msg.guild.id}_reactions.log", 'a+') as f:
    #     f.write(
    #         f"{msg.id},{msg.channel.id},{msg.author.id},"
    #         f"{msg.content},{time.time()}\n"
    #     )
    pass

# ---
# Message events
# ---
@bot.event
async def on_message(msg):
    print(msg)
    log_message(msg)

@bot.event
async def on_raw_message_edit(payload):
    print(payload)

@bot.event
async def on_raw_message_delete(payload):
    print(payload)

@bot.event
async def on_raw_bulk_message_delete(payload):
    print(payload)

# ---
# Reaction events
# ---
@bot.event
async def on_raw_reaction_add(payload):
    print(payload)
    log_reaction_add(payload)

@bot.event
async def on_raw_reaction_remove(payload):
    print(payload)

@bot.event
async def on_raw_reaction_clear(payload):
    print(payload)

@bot.event
async def on_raw_reaction_clear_emoji(payload):
    print(payload)

# ---
# Run the bot
# ---
bot.run(TOKEN)
