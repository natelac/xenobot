# Xenobot: A Discord Server Logging Bot

A bot used for collecting discord user and channel information including messages and reactions. Data can be collected actively or it can be collected passively as it is posted to the discord server.

## Setup

Requires python3.8 or above.

Run `pip install .` to install using `setup.py`.

Only guarenteed to work using Linux.

## Usage

### Creating the Database

First initialize the database by using `bin/xenodb create`. This will create a database at `var/xenodb.sqlite3` from the sql schema and views stored in `sql/schema` and `sql/views` respectively.

You can access the data by running `sqlite3 var/xenodb.sqlite3`, and using any sqlite3 commands to access the data.

If the database ever gets messed up, you can run `bin/xenodb destroy` to delete the database or `bin/xenodb reset` to destroy it and create another one. However, it will delete any information stored.

### Collecting Data

It is recommended that you run all of the bot commands with atleast level 1 verbosity, i.e. `-v`. 

To start monitoring the server, run `bin/xenobot start -v`. If you don't want the command to block the terminal, run `nohup bin/xenobot start -v > log 2>&1 &`. This command will store the output of the bot to log file called `log` that you can read. If you start the server while it is already running it can cause the previous bot to get ghosted by the new one. Use `ps aux` to find any hanging processes and `kill <PID>` to stop them. 

To stop the bot run `bin/xenobot stop`

To collect existing data on your discord server run `bin/xenobot gather <yyyy-mm-dd>` where the date is the furthest back you want to gather data. It defaults to 4 weeks ago. This command will only work if the bot is currently running.

If you only want to collect existing data, you can run `python3 gather.py <yyyy-mm-dd> -v`. That command will not monitor the server, and will stop blocking the terminal when it is done running.

### Creating Custom Logging

To monitor more discord information you can add any bot listener function supported by the `discord.py` API to the `sql_cog` class in `bot.py`. Then add the sql query to `log_utils.py`. You can find a list of supported `discord.py` API calls at the [web docs](https://discordpy.readthedocs.io/en/latest/api.html#)

## Known Bugs

- Running gather multiple times will create duplicates in some rows, this can be fixed by using `SELECT DISTINCT` in your sqlite3 queries.

## Future Features
- Using "crontab -e" to make a cron job for the bot!!!
- Fix duplicate values for "gather.py"
  - I think it's just things that have incremental primary keys?
- Make a config file
  - Set time intervals for active monitoring
  - Set default earliest\_date for gathering data
  - Store default DB\_PATH and GUILD
  - Add whitelist/blacklists to channels/users etc.
- Comment code and files better
- Make more useful views
  - Most recent logged nickname
  - Count of emojis to all users messages
- Make python analytics tools
  - Folder called "analytics"
  - Render "aesthetic" graphs
    - Bar charts
      - Most messages
      - Most @'ed
      - Most swears
      - Number of messages by day of the week
      - Number of messages by month of the year
      - Top poster by channel
      - Reaction stuff
    - Line plots
      - Number of messages week by week throughout the years
- Track discord information
  - What guilds the bot is in
  - Information per guild
    - All user information
      - Log their public information, and when they change it and what to
      - Log of member statuses
    - All channel information
      - Log of messages sent, and by whom
      - Log when a channel is created/deleted/changed
      - Log when a user is typing
    - All voice channel information
      - Log voice channel messages
      - Log of users joining/leaving a voice channel
- White elephant
  - Make an alert about the white elephant and telling people how to join
    - Take interactions on the message to prompt the bot to DM
    - DM asks for persons address to ship the package
  - At a certain date, calculate who is with who and send out the DM's informing people who their matches are
- Clean up plex
  - Remove movies/seasons of shows that go unwatched
  - Track when movies are created, when they are last watched, and how many people have watched it
  - Weight time to removal by how many people have watched it
  - Start a poll in discord on whether or not the movie should be removed
    - Have two reactions, one for keep and one for remove
    - If nobody votes keep, get rid of it
    - If anyone votes keep, weight how much longer it gets to stay by how many vote keep
    - If people are voting keep and remove, weight how much longer it stays by the ratio of the vote
      - This could be a bit toxic, but the idea is that there is limited space, so people are voting for how to distribute the space
    - Contested movies should be voted on sooner than uncontested movies, so that the bot doesn't spam.
- Get a backup system working
