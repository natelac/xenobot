PRAGMA foreign_keys = ON;

CREATE TABLE guilds(
  guild_id INTEGER PRIMARY KEY,
  guildname VARCHAR(32),
  guildtag VARCHAR(4)
);

CREATE TABLE users(
  user_id INTEGER PRIMARY KEY,
  discriminator INTEGER
);

CREATE TABLE guild_members(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id INTEGER,
  guild_id INTEGER
);

CREATE TABLE user_statuses(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id INTEGER,
  status VARCHAR(32),
  time DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE usernames(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id INTEGER,
  username VARCHAR(32)
);

CREATE TABLE nicknames(
  id INTEGER PRIMARY KEY AUTOICNREMENT,
  user_id INTEGER,
  nickname VARCHAR(32)
);

CREATE TABLE channels(
  channel_id INTEGER PRIMARY KEY,
  guild_id INTEGER,
  name INTEGER,
  created DATETIME
);

CREATE TABLE message_adds(
  message_id INTEGER PRIMARY KEY,
  guild_id INTEGER REFERENCES guilds(guild_id),
  channel_id INTEGER,
  author_id INTEGER,
  content VARCHAR(2000),
  created DATETIME
);

CREATE TABLE message_deletes(
  message_id INTEGER PRIMARY KEY,
  deleted DATETIME
);

CREATE TABLE message_edits(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  message_id INTEGER,
  new_content VARCHAR(2000),
  edited DATETIME
);

CREATE TABLE reaction_adds(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  message_id INTEGER,
  user_id INTEGER,
  reaction VARCHAR(32),
  created DATETIME
);

CREATE TABLE reaction_deletes(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  message_id INTEGER,
  user_id INTEGER,
  deleted DATETIME 
);

CREATE TABLE typing(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id INTEGER,
  time DATETIME DEFAULT CURRENT_TIMESTAMP
);
