"""Utilities for logging discord information to a sqlite3 database
"""
import pathlib
import sqlite3
from datetime import datetime
import logging

# Setup logger
log = logging.getLogger("bot")

class sqlite3Logger:
    def __init__(self, db_path):
        try:
            self.conn = sqlite3.connect(db_path)
        except:
            log.error(f"Could not open sqlite3 connection for: {db_path}")
            raise
        self.cur = self.conn.cursor()

    def insert_row(self, sql, vals):
        try:
            self.cur.execute(sql, vals)
            self.conn.commit()
        except Exception as e:
            log.debug(f"Could not insert row: {e}")

    async def full_log_guild(self, guild, earliest_date):
        """Iteratively logs all relevant information in a guild"""
        log.info(f"Logging guild '{guild.name}'")
        self.log_guild(guild)

        log.info(f"Logging members")
        for member in guild.members:
            log.debug(f"Logging user '{member.name}'")
            self.log_user(member)
            self.log_username(member)
            self.log_nickname(member, guild)
            self.log_guild_member(member, guild)

        for channel in guild.text_channels:
            log.info(f"Logging channel '{channel.name}'")
            self.log_text_channel(channel)
            try:
                messages = [message async for message in channel.history(
                            limit=None,
                            after=datetime.combine(
                                earliest_date,
                                datetime.min.time()))]
            except Exception as e:
                log.info(f"Could not fetch message: {e}")
                continue
            for message in messages:
                log.debug(f"Logging message from timestamp '{message.created_at}'")
                self.log_message(message)
                for reaction in message.reactions:
                    log.debug(f"Logging reaction '{reaction.emoji}'")
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

    # Guild members
    def log_guild_member(self, member, guild):
        sql = """ INSERT INTO guild_members(user_id, guild_id)
                  VALUES(?,?) """
        vals = member.id, guild.id
        self.insert_row(sql, vals)

    def log_nickname(self, member, guild):
        sql = """ INSERT INTO nicknames(user_id, guild_id, nickname)
                  VALUES(?,?,?) """
        vals = member.id, guild.id, member.display_name
        self.insert_row(sql, vals)

    def log_user_status(self, member):
        sql = """ INSERT INTO user_statuses(user_id, status)
                  VALUES(?,?) """
        pass

    # Channels
    def log_text_channel(self, channel):
        sql = """ INSERT INTO text_channels(channel_id, channel_name, guild_id, position, mention, created)
                  VALUES(?,?,?,?,?,?) """
        vals = channel.id, channel.name, channel.guild.id, channel.position, \
               channel.mention, channel.created_at
        self.insert_row(sql, vals)

    def log_text_channel_add(self, channel):
        self.log_text_channel(channel)

    def log_channel_delete(self, payload):
        #TODO
        sql = """ INSERT INTO text_channel_deletes(channel_name, guild_id,
                      position, mention, created)
                  VALUES(?,?,?,?,?) """
        pass

    def log_channel_edit(self, payload):
        #TODO
        sql = """ INSERT INTO text_channel_deletes(channel_name, deleted)
                  VALUES(?,?) """
        pass

    # Messages
    def log_message(self, msg):
        log.debug(f"Logging message '{msg.id}'")
        sql = """ INSERT INTO messages(message_id, guild_id, channel_id,
                      author_id, content, created)
                  VALUES(?,?,?,?,?,?) """
        vals = msg.id, msg.guild.id, msg.channel.name, msg.author.id, \
                msg.content, msg.created_at
        self.insert_row(sql, vals)

    def log_message_delete(self, payload):
        log.debug(f"Logging deletion of message '{payload.message_id}'")
        sql = """ INSERT INTO message_deletes(message_id)
                  VALUES(?) """
        vals = (payload.message_id,)
        self.insert_row(sql, vals)

    def log_message_edit(self, edited_msg):
        log.debug(f"Logging edit of message '{edited_msg.id}'")
        sql = """ INSERT INTO message_edits(message_id, new_content, edited)"""
        vals = edited_msg.id, edited_msg.content, edited_msg.edited_at
        self.insert_row(sql, vals)

    def log_message_add(self, msg):
        return self.log_message(msg)

    # Reactions
    def log_reaction(self, reaction):
        emoji = str(reaction.emoji)
        log.debug(f"Logging reaction '{emoji}' on message "
                  f"'{reaction.message.id}'")
        sql = """ INSERT INTO reactions(message_id, emoji, count)
                  VALUES(?,?,?) """
        vals = reaction.message.id, emoji, reaction.count
        self.insert_row(sql, vals)

    def log_reaction_add(self, payload):
        emoji = str(payload.emoji)
        log.debug(f"Logging reaction emoji '{emoji}' added by user "
                  f"'{payload.user_id}'")
        sql = """ INSERT INTO reaction_adds(message_id, user_id, emoji)
                  VALUES(?,?,?) """
        vals = payload.message_id, payload.user_id, emoji
        self.insert_row(sql, vals)

    def log_reaction_delete(self, payload):
        emoji = str(payload.emoji)
        log.debug(f"Logging reaction emoji '{emoji}' deleted by user "
                  f"'{payload.user_id}'")
        sql = """ INSERT INTO reaction_deletes(message_id, user_id, emoji)
                  VALUES(?,?,?) """
        vals = payload.message_id, payload.user_id, emoji
        self.insert_row(sql, vals)

    # Typing
