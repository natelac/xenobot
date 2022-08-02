#!/usr/bin/python3.8

"""Data scraping script for discord, loads data into an sqlite3 db
"""

import argparse
import asyncio
from datetime import date
import datetime
from discord.ext import commands
import discord
from dotenv import load_dotenv
import os
import pathlib
import sys
import time
import logging

from log_utils import sqlite3Logger

if not (sys.version_info[0] == 3 and sys.version_info[1] >= 8):
    if not (ssy.version_info[0] > 3):
        raise Exception("Python3.8 or above is required")

# Default arguments
DEFAULT_GUILD = "Area 51"
DEFAULT_DB_PATH = pathlib.Path("var/xenodb.sqlite3")

# Parse arguments
parser = argparse.ArgumentParser(
    description="Scrape existing data from discord servers"
)
parser.add_argument(
    "-g", "--guild", type=str,
    help="name of guild to scrape data from",
    default=DEFAULT_GUILD,
)
parser.add_argument(
    "-p",
    "--db_path",
    type=pathlib.Path,
    help="path to sqlite3 database to store data in",
    default=DEFAULT_DB_PATH,
)
parser.add_argument(
    "-d",
    "--earliest_date",
    type=date.fromisoformat,
    help=f"farthest date back to scrape data from, "
    f"uses iso format <yyyy-mm-dd> "
    f"with a default of 4 weeks ago",
    default=(date.today() - datetime.timedelta(weeks=4)),
)
parser.add_argument(
    "-v",
    "--verbose",
    help=f"increase output verbosity, " f"more v's give more verbosity",
    action="count",
    default=0,
)

args = parser.parse_args()

# Change level of logging by verbosity
# https://stackoverflow.com/a/34065768
levels = [logging.WARNING, logging.INFO, logging.DEBUG]
level = levels[min(args.verbose, len(levels) - 1)]
logging.basicConfig(level=logging.CRITICAL, format="%(message)s")
log = logging.getLogger("bot")
log.setLevel(level=level)

# Setup the bot
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
GUILD = args.guild

# Setup intents
intents = discord.Intents.all()
intents.members = True
intents.presences = True
intents.guilds = True
intents.messages = True
intents.reactions = True

# Initialize the bot
bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    """Print bot status and start logging."""
    # Make sure bot can connect to discord and find guild
    guild = discord.utils.get(bot.guilds, name=GUILD)
    if guild is None:
        log.error(f"Could not find guild: {GUILD}")
        await bot.close()

    # Start logging
    sql_log = sqlite3Logger(args.db_path)
    await sql_log.full_log_guild(guild, args.earliest_date)
    await bot.close()

# def main(argv):
#   bot.run(TOKEN)

# if __name__ == "__main__":
#   main(sys.argv)

bot.run(TOKEN)
