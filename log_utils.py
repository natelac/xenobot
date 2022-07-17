"""Utilities for logging discord information to a sqlite3 database
"""
import pathlib
import sqlite3
from datetime import datetime

class sqlite3Logger:
    def __init__(self, db_path):
        try:
            self.conn = sqlite3.connect(db_path)
        except:
            print(f"Could not open sqlite3 connection for: {db_path}")
            raise
        self.cur = self.conn.cursor()

    def insert_row(self, sql, vals):
        try:
            #print(f"insert {sql} {vals}")
            self.cur.execute(sql, vals)
            self.conn.commit()
        except Exception as e:
            print(f"Error inserting row: {e}")

    async def full_log_guild(self, guild, earliest_date):
        """Iteratively logs all relevant information in a guild"""
        self.log_guild(guild)

        for member in guild.members:
            self.log_user(member)
            self.log_username(member)
            self.log_nickname(member, guild)
            self.log_guild_member(member, guild)

        for channel in guild.text_channels:
            self.log_text_channel(channel)
            try:
                messages = [message async for message in channel.history(
                            after=datetime.combine(
                                earliest_date,
                                datetime.min.time()))]
            except Exception as e:
                print(f"Error fetching message: {e}")
                continue

            for message in messages:
                self.log_message(message)
                for reaction in message.reactions:
                    self.log_reaction(reaction)

    # Guilds
    def log_guild(self, guild):
        sql = """ INSERT INTO guilds(guild_id, guildname, guildowner, created)
                  VALUES(?,?,?,?) """
        vals = guild.id, guild.name, guild.owner_id, guild.created_at
        self.insert_row(sql, vals)

    # Users
    def log_user(self, user):
        sql = """ INSERT INTO users(user_id, discriminator, created, bot)
                  VALUES(?,?,?,?) """
        vals = user.id, user.discriminator, user.created_at, user.bot
        self.insert_row(sql, vals)

    def log_username(self, user):
        sql = """ INSERT INTO usernames(user_id, username)
                  VALUES(?,?) """
        vals = user.id, user.name
        self.insert_row(sql, vals)

    def log_nickname(self, member, guild):
        sql = """ INSERT INTO nicknames(user_id, guild_id, nickname)
                  VALUES(?,?,?) """
        vals = member.id, guild.id, member.display_name
        self.insert_row(sql, vals)

    # Guild members
    def log_guild_member(self, member, guild):
        sql = """ INSERT INTO guild_members(user_id, guild_id)
                  VALUES(?,?) """
        vals = member.id, guild.id
        self.insert_row(sql, vals)

    def log_user_status(self, member):
        pass

    # Channels
    def log_text_channel(self, channel):
        sql = """ INSERT INTO text_channels(channel_name, guild_id, position, mention, created)
                  VALUES(?,?,?,?,?) """
        vals = channel.name, channel.guild.id, channel.position, \
                channel.mention, channel.created_at
        self.insert_row(sql, vals)

    def log_channel_delete(self, payload):
        pass

    def log_channel_edit(self, payload):
        pass

    # Messages
    def log_message(self, msg):
        sql = """ INSERT INTO messages(message_id, guild_id, channel_name,
                    author_id, content, created)
                  VALUES(?,?,?,?,?,?) """
        vals = msg.id, msg.guild.id, msg.channel.name, msg.author.id, \
                msg.content, msg.created_at
        try:
            self.cur.execute(sql, vals)
            self.conn.commit()
        except Exception as e:
            print(e)
            #print(vals)
        #self.insert_row(sql, vals)

    def log_message_delete(self, payload):
        pass

    def log_message_edit(self, payload):
        pass

    # Reactions
    def log_reaction(self, reaction):
        sql = """ INSERT INTO reactions(message_id, emoji, count)
                  VALUES(?,?,?) """
        # Checks for type of emoji?
        emoji = str(reaction.emoji)
        vals = reaction.message.id, emoji, reaction.count
        self.insert_row(sql, vals)

    def log_reaction_delete(self, payload):
        pass

    def log_reaction_edit(self, payload):
        pass

    # Typing
