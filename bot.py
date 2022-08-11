import sys
import os
import time
import asyncio
import argparse
import pathlib
import logging
from dotenv import load_dotenv

from discord.ext import commands
import discord

from log_utils import sqlite3Logger

# Check python version is 3.8 or greater
if sys.version_info < (3, 8):
    raise Exception("Python3.8 or above is required")

# Load defaults variables
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
DEFAULT_GUILD = os.getenv('GUILD')
DEFAULT_DB_PATH = pathlib.Path(os.getenv('DB_PATH'))
FIFO = pathlib.Path(os.getenv('FIFO'))
COMMAND_PREFIX = os.getenv('COMMAND_PREFIX')


def make_bot(args):
    """Return a runnable discord bot"""
    intents = discord.Intents.all()
    intents.members = True
    intents.presences = True
    intents.guilds = True
    intents.messages = True
    intents.reactions = True
    intents.typing = True
    intents.voice_states = True
    bot = xenobot(COMMAND_PREFIX, intents, args)
    return bot


class xenobot(commands.Bot):
    """The bot class for interacting with discord.com

    The bots functions are distributed between this class and the class
    "sql_cog". This was done because without cogs, the event loop get's broken.
    """
    def __init__(self, command_prefix, intents, args):
        super().__init__(command_prefix=command_prefix, intents=intents)
        self.add_cog(sql_cog(self, args))

        # Change level of logging by verbosity
        levels = [logging.WARNING, logging.INFO, logging.DEBUG]
        level = levels[min(args.verbose, len(levels) - 1)]
        logging.basicConfig(level=logging.CRITICAL, format="%(message)s")
        self.log = logging.getLogger("bot")
        self.log.setLevel(level=level)

    async def cleanup(self):
        """Removes the named pipe"""
        if os.path.exists(FIFO):
            os.remove(FIFO)

    async def close(self):
        """Stops the bot cleanly"""
        self.log.info("\nStopping bot")
        await self.cleanup()
        await super().close()


class sql_cog(commands.Cog):
    """Discord cog class for logging data to the sqlite3 database"""
    def __init__(self, bot, args):
        self.bot = bot
        self.args = args
        self.log_time = (60) * 5
        self.sql_log = sqlite3Logger(args.db_path)
        self.make_fifo()

    def make_fifo(self):
        """Creates the named pipe, or resets it if it already exists"""
        pathlib.Path.mkdir(FIFO.parent, parents=True, exist_ok=True)
        if os.path.exists(FIFO):
            os.remove(FIFO)
        try:
            os.mkfifo(FIFO)
        except OSError:
            return

    async def active_log_loop(self, guild):
        """Actively logs discord information"""
        while True:
            await self.sql_log.log_guild_statuses(guild)
            await asyncio.sleep(self.log_time)

    async def read_fifo_loop(self):
        """Reads from the named pipe.

        Since `os.open()` blocks the entire program (and asyncio does not seem
        to be able to handle this), the looping is done at
        manual intervals of 0.1 seconds.
        """
        while True:
            if os.path.exists(FIFO):
                fifo = os.open(FIFO, os.O_NONBLOCK | os.O_RDONLY)
                buf = os.read(fifo, 100)
                if buf:
                    content = buf.decode("utf-8")
                    lines = content.split("\n")[:-1]
                    self.bot.log.info(f"Recieved commands: {lines}")

                    async def switch_gather(args):
                        print(args)
                        await self.sql_log.full_log_guild(
                                self.args.guild, args[1])

                    async def switch_stop(args):
                        await self.bot.close()

                    for line in lines:
                        args = line.split(",")
                        options = {
                                "gather": switch_gather,
                                "stop": switch_stop
                                }
                        await options[args[0]](args)

                await asyncio.sleep(0.1)
            else:
                self.bot.log.error("Cannot read named pipe")
                await self.bot.close()
                return

    @commands.Cog.listener()
    async def on_ready(self):
        """Starts the loops on successfull connection to discord.com"""
        guild = discord.utils.get(self.bot.guilds, name=self.args.guild)
        if guild is None:
            self.bot.log.error(f"Could not find guild: {self.args.guild}")
            await self.bot.close()
        else:
            self.bot.log.info(
                    f"Successfully connected to guild: {self.args.guild}")

        loop = asyncio.get_event_loop()
        loop.create_task(self.active_log_loop(guild))
        loop.create_task(self.read_fifo_loop())

    @commands.Cog.listener()
    async def on_message(self, msg):
        self.sql_log.log_message(msg)

    @commands.Cog.listener()
    async def on_raw_message_edit(self, payload):
        self.bot.log.info(f"Cannot handle message edit: {payload}")
        # TODO
        # - Fetch message that was edited and pass it to sql_log
        # sql_log.log_message_edit(payload)
        pass

    @commands.Cog.listener()
    async def on_raw_message_delete(self, payload):
        self.sql_log.log_message_delete(payload)

    @commands.Cog.listener()
    async def on_raw_typing(self, payload):
        self.sql_log.log_typing(payload)

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        self.sql_log.log_reaction_add(payload)

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        self.sql_log.log_reaction_delete(payload)


if __name__ == "__main__":
    # Parse arguments
    parser = argparse.ArgumentParser(
        description="Monitor the discord server for new data"
    )
    parser.add_argument(
        "-g",
        "--guild",
        type=str,
        help="name of guild to log",
        default=DEFAULT_GUILD,
    )
    parser.add_argument(
        "-p",
        "--db_path",
        type=pathlib.Path,
        help="path to sqlite3 database",
        default=DEFAULT_DB_PATH,
    )
    parser.add_argument(
        "-v",
        "--verbose",
        help=f"increase output verbosity",
        action="count",
        default=0,
    )
    args = parser.parse_args()
    bot = make_bot(args)
    bot.run(TOKEN)
