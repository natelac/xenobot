#!/usr/bin/python3.8
import pathlib
import dotenv
import argparse
import dotenv
import os
from datetime import date
import datetime
from dotenv import load_dotenv
from bot import make_bot
import sys

if not (sys.version_info[0] == 3 and sys.version_info[1] >= 8):
    if not (sys.version_info[0] > 3):
        raise Exception("Python3.8 or above is required")

# Default arguments
load_dotenv()
DEFAULT_GUILD = os.getenv('GUILD')
DEFAULT_DB_PATH = pathlib.Path(os.getenv('DB_PATH'))
FIFO = pathlib.Path(os.getenv('FIFO'))
TOKEN = os.getenv('DISCORD_TOKEN')

def write_to_fifo(msg):
    if not pathlib.Path.exists(FIFO):
        print("No named pipe at:", FIFO)
        print("Restart the bot...") 
        return
    fd = os.open(FIFO, os.O_WRONLY)
    line = str.encode(msg + "\n")
    os.write(fd, line)

def start(args):
    bot = make_bot(args)
    bot.run(TOKEN)

def gather(args):
    line = "gather" + "," + str(args.earliest_date)
    write_to_fifo(line)

def stop(args):
    write_to_fifo("stop")

# Parse arguments
parser = argparse.ArgumentParser(
        description="Controller for the discord bot")
parser.add_argument('-v', '--verbose',
        help=f'increase output verbosity'
             f"more v's give more verbosity",
        action='count', default=0)
parser.add_argument('-g', '--guild', type=str,
        help='name of guild to log',
        default=DEFAULT_GUILD)
parser.add_argument('-p', '--db_path', type=pathlib.Path,
        help='path to sqlite3 database',
        default=DEFAULT_DB_PATH)
subparsers = parser.add_subparsers(help='sub-command help')
parser_start = subparsers.add_parser('start', 
        help='connect to discord.com and begin logging')
parser_start.add_argument('-v', '--verbose',
        help=f'increase output verbosity'
             f"more v's give more verbosity",
        action='count', default=argparse.SUPPRESS)
parser_start.set_defaults(func=start)
parser_gather = subparsers.add_parser('gather',
        help=f'scrape existing data from discord servers, '
             f'defaults to .env values')
parser_gather.add_argument('-d', '--earliest_date', type=date.fromisoformat,
        help=f'farthest date back to scrape data from, '
             f'uses iso format <yyyy-mm-dd> '
             f'with a default of 4 weeks ago',
        default=(date.today() - datetime.timedelta(weeks=4)))
parser_gather.add_argument('-v', '--verbose',
        help=f'increase output verbosity'
             f"more v's give more verbosity",
        action='count', default=argparse.SUPPRESS)
parser_gather.set_defaults(func=gather)
parser_stop = subparsers.add_parser('stop',
        help='stop the bot')
parser_stop.add_argument('-v', '--verbose',
        help=f'increase output verbosity'
             f"more v's give more verbosity",
        action='count', default=argparse.SUPPRESS)
parser_stop.set_defaults(func=stop)
args = parser.parse_args()        
args.func(args)
