import pathlib
import dotenv
import argparse
import dotenv
import os
from datetime import date
import datetime
from dotenv import load_dotenv
from bot import make_bot

# Default arguments
load_dotenv()
DEFAULT_GUILD = os.getenv('GUILD')
DEFAULT_DB_PATH = pathlib.Path(os.getenv('DB_PATH'))
FIFO = os.getenv('FIFO')
TOKEN = os.getenv('DISCORD_TOKEN')

def start(args):
    print("starting")
    print(args)
    bot = make_bot(args)
    bot.run(TOKEN)

def gather(args):
    print("gathering")
    print(args)

def stop():
    print("stopping")

# Parse arguments
parser = argparse.ArgumentParser(
        description="Controller for the discord bot")
parser.add_argument('-v', '--verbose',
        help=f'increase output verbosity',
        action='count', default=0)
parser.add_argument('-g', '--guild', type=str,
        help='name of guild to scrape data from',
        default=DEFAULT_GUILD)
parser.add_argument('-p', '--db_path', type=pathlib.Path,
        help='path to sqlite3 database to store data in',
        default=DEFAULT_DB_PATH)
subparsers = parser.add_subparsers(help='sub-command help')
parser_start = subparsers.add_parser('start', 
        help='start bot and collect data in the background')
parser_start.set_defaults(func=start)
parser_gather = subparsers.add_parser('gather',
        help=f'scrape existing data from discord servers, '
             f'defaults to .env values')
parser_gather.add_argument('-d', '--earliest_date', type=date.fromisoformat,
        help=f'farthest date back to scrape data from, '
             f'uses iso format <yyyy-mm-dd> '
             f'with a default of 4 weeks ago',
        default=(date.today() - datetime.timedelta(weeks=4)))
parser_stop = subparsers.add_parser('stop',
        help='stop the bot')
args = parser.parse_args()        
args.func(args)
