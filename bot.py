# bot.py
import os

import discord
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client()

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

# @client.event
# async def on_presence_update(before, after):
#     if before.status != after.status:
#         print(
#             f'User {before.name} has changed their status'
#             f' from {before.status} to {after.status}'
#     else:
#         print(
#             f'User {before.name} has changed their activity'
#             f' from {before.activity} to {after.activity}'

client.run(TOKEN)


