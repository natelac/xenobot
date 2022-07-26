import sys
import os
import time
import asyncio
import argparse

from discord.ext import commands
import discord
from dotenv import load_dotenv

import pathlib
import logging

from log_utils import sqlite3Logger

# -----------------------
# Arguments and Logging
# -----------------------
# Default arguments
DEFAULT_GUILD = "Area 51"
DEFAULT_DB_PATH = pathlib.Path("var/xenodb.sqlite3")

# Parse arguments
parser = argparse.ArgumentParser(
        description="Monitor the discord server for new data")
parser.add_argument('-g', '--guild', type=str,
                    help='name of guild to scrape data from',
                    default=DEFAULT_GUILD)
parser.add_argument('-p', '--db_path', type=pathlib.Path,
                    help='path to sqlite3 database to store data in',
                    default=DEFAULT_DB_PATH)
parser.add_argument('-v', '--verbose',
                    help=f"increase output verbosity, "
                         f"more v's give more verbosity",
                    action="count", default=0)

args = parser.parse_args()

# Change level of logging by verbosity
levels = [logging.WARNING, logging.INFO, logging.DEBUG]
level = levels[min(args.verbose, len(levels) -1)]
logging.basicConfig(level=logging.CRITICAL, format='%(message)s')
log = logging.getLogger('bot')
log.setLevel(level=level)


# -----------------------
# Initialize Bot and 
# Variables
# -----------------------
# Set constants
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = args.guild # The guild the bot
COMMAND_PREFIX = '!'# Is this still necessary?
LOG_TIME = (60) * 5 # Seconds between logs

# Intents the bot will use
intents = discord.Intents.all()
intents.members = True
intents.presences = True
intents.guilds = True
intents.messages = True
intents.reactions = True
intents.typing = True
intents.voice_states = True

# Initiallize the bot
bot = commands.Bot(command_prefix=COMMAND_PREFIX, intents=intents)

# Initialize logger
sql_log = sqlite3Logger(args.db_path)

# ------------------------
# Core Loop (on_ready)
# ------------------------
@bot.event
async def on_ready():
    guild = discord.utils.get(bot.guilds, name=GUILD)
    if guild is None:
        log.error(f"Could not find guild: {GUILD}")
        await bot.close()
    else:
        log.info(f"Successfully connected to guild: {GUILD}")

   # Start actively logging
    while(True):
        # TODO:
        # - Add logic here to recieve a shutdown command then run bot.close()
        await sql_log.log_guild_statuses(guild)
        await asyncio.sleep(LOG_TIME)

# ------------------------
# Message events
# ------------------------
@bot.event
async def on_message(msg):
    sql_log.log_message(msg)

@bot.event
async def on_raw_message_edit(payload):
    log.info(f"Cannot handle message edit: {payloadj}")
    #TODO
    # - Fetch message that was edited and pass it to sql_log
    #sql_log.log_message_edit(payload)
    pass

@bot.event
async def on_raw_message_delete(payload):
    sql_log.log_message_delete(payload)

@bot.event
async def on_raw_typing(payload):
    sql_log.log_typing(payload)

# ------------------------
# Reaction events
# ------------------------
@bot.event
async def on_raw_reaction_add(payload):
    sql_log.log_reaction_add(payload)

@bot.event
async def on_raw_reaction_remove(payload):
    sql_log.log_reaction_delete(payload)

@bot.event
async def on_raw_reaction_clear(payload):
    log.info(f"Cannot handle reaction clears: {payload}")

@bot.event
async def on_raw_reaction_clear_emoji(payload):
    log.info(f"Cannot handle reaction emoji clears: {payload}")

# ------------------------
# Run the bot
# ------------------------
bot.run(TOKEN)
