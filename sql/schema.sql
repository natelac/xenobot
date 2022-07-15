PRAGMA foreign_keys = ON;

CREATE TABLE guilds(
  guild_id INTEGER PRIMARY KEY,
  guildname VARCHAR(32),
  guildowner INTEGER,
  created DATETIME
);

CREATE TABLE users(
  user_id INTEGER PRIMARY KEY,
  discriminator VARCHAR(32),
  created DATETIME,
  bot BOOLEAN
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
  inserted DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE usernames(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id INTEGER,
  username VARCHAR(32),
  inserted DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE nicknames(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id INTEGER,
  guild_id INTEGER,
  nickname VARCHAR(32),
  inserted DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE text_channels(
  channel_name VARCHAR(32) PRIMARY KEY,
  guild_id INTEGER,
  position INTEGER,
  mention VARCHAR(32),
  created DATETIME
);

CREATE TABLE text_channel_deletes(
  channel_id INTEGER PRIMARY KEY,
  deleted DATETIME
);

CREATE TABLE text_channel_edits(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name INTEGER,
  new_name varchar(32),
  edited DATETIME
);

CREATE TABLE messages(
  message_id INTEGER PRIMARY KEY,
  guild_id INTEGER REFERENCES guilds(guild_id),
  channel_name INTEGER,
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

CREATE TABLE reactions(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  message_id INTEGER,
  emoji VARCHAR(32),
  count INTEGER
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
