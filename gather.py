#!/usr/bin/env/ python3.8

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

from log_utils import sqlite3Logger

# Parse the arguments
parser = argparse.ArgumentParser(
    description="Scrape existing data from discord servers")
parser.add_argument('-g', '--guild', type=str,
                    help='name of guild to scrape data from',
                    required=True)
parser.add_argument('-p', '--db_path', type=pathlib.Path,
                    help='path to sqlite3 database to store data in',
                    required=True)
parser.add_argument('-d', '--earliest_date', type=date.fromisoformat,
                    help=f'farthest date back to scrape data from, '
                         f'uses iso format <yyyy-mm-dd> '
                         f'with a default of 4 weeks ago',
                    default=(date.today() - datetime.timedelta(weeks=4)))
args = parser.parse_args()

# Setup the bot
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = args.guild

intents = discord.Intents.all()
intents.members = True
intents.presences = True
intents.guilds = True
intents.messages = True
intents.reactions = True

bot = commands.Bot(command_prefix='!',intents=intents)

@bot.event
async def on_ready():
    """Print bot status and start logging."""
    # Make sure bot can connect to discord and find guild
    guild = discord.utils.get(bot.guilds, name=GUILD)
    if guild is None:
        sys.exit(f"Could not find guild {GUILD}")

    # Start logging
    logger = sqlite3Logger(args.db_path)
    await logger.full_log_guild(guild, args.earliest_date)
    sys.exit("Done logging guild, messy exit");


def main(argv):
    bot.run(TOKEN)

if __name__ == "__main__":
    main(sys.argv)
