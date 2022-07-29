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
import errno
import shutil

from log_utils import sqlite3Logger

# Load defaults
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
DEFAULT_GUILD = os.getenv('GUILD')
DEFAULT_DB_PATH = pathlib.Path(os.getenv('DB_PATH'))
FIFO = os.getenv('FIFO')
COMMAND_PREFIX = '!'

class xenobot:
    # Initiallize the bot
    intents = discord.Intents.all()
    intents.members = True
    intents.presences = True
    intents.guilds = True
    intents.messages = True
    intents.reactions = True
    intents.typing = True
    intents.voice_states = True
    bot = commands.Bot(command_prefix=COMMAND_PREFIX, intents=intents)
    def __init__(self, args):
        self.args = args
        self.log_time = (60) * 5


        # Initialize logger
        self.sql_log = sqlite3Logger(args.db_path)

        # Change level of logging by verbosity
        levels = [logging.WARNING, logging.INFO, logging.DEBUG]
        level = levels[min(args.verbose, len(levels) -1)]
        logging.basicConfig(level=logging.CRITICAL, format='%(message)s')
        self.log = logging.getLogger('bot')
        self.log.setLevel(level=level)

    def run(self):
        self.bot.run(TOKEN)


    async def active_log(self, guild):
        while(True):
            await self.sql_log.log_guild_statuses(guild)
            await asyncio.sleep(LOG_TIME)

    async def read_fifo(self):
        if os.path.exists(FIFO):
            os.unlink(FIFO)
        os.mkfifo(FIFO)

        while(True):
            fifo = os.open(FIFO, os.O_NONBLOCK | os.O_RDONLY)
            buf = os.read(fifo, 100)
            if buf:
                content = buf.decode("utf-8")
                content = content.split("\n")
                self.log.info(f"READ: {content}")
            await asyncio.sleep(0.1)

    # ------------------------
    # Core Loop (on_ready)
    # ------------------------
    @bot.event
    async def on_ready():
        guild = discord.utils.get(bot.guilds, name=self.args.guild)
        if guild is None:
            self.log.error(f"Could not find guild: {GUILD}")
            await self.bot.close()
        else:
            self.log.info(f"Successfully connected to guild: {GUILD}")

        loop = asyncio.get_event_loop()
        loop.create_task(self.active_log(guild))
        loop.create_task(self.read_fifo())

    # ------------------------
    # Message events
    # ------------------------
    @bot.event
    async def on_message(msg):
        self.sql_log.log_message(msg)

    @bot.event
    async def on_raw_message_edit(payload):
        self.log.info(f"Cannot handle message edit: {payloadj}")
        #TODO
        # - Fetch message that was edited and pass it to sql_log
        #sql_log.log_message_edit(payload)
        pass

    @bot.event
    async def on_raw_message_delete(payload):
        self.sql_log.log_message_delete(payload)

    @bot.event
    async def on_raw_typing(payload):
        self.sql_log.log_typing(payload)

    # ------------------------
    # Reaction events
    # ------------------------
    @bot.event
    async def on_raw_reaction_add(payload):
        self.sql_log.log_reaction_add(payload)

    @bot.event
    async def on_raw_reaction_remove(payload):
        self.sql_log.log_reaction_delete(payload)

if __name__ == '__main__':
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
    bot = xenobot(args)
    bot.run()
