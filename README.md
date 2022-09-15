# Xenobot: A Discord Server Logging Bot

A bot used for collecting discord user and channel information including messages and reactions. Data can be collected from the server logs or it can come from monitoring.

## Setup

Requires python3.8 or above.

Run `pip install .` to install using `setup.py`.

Only guarenteed to work using Linux.

Rename the file `.env_example` to `.env` after adding your bot's discord token and adding the name of the guild to monitor.

## Usage

### Creating the Database

First initialize the database by using `bin/xenodb create`. This will create a database at `var/xenodb.sqlite3` from the sql schema and views stored in `sql/schema` and `sql/views` respectively.

You can access the data by running `sqlite3 var/xenodb.sqlite3`.

If the database ever gets messed up, you can run `bin/xenodb destroy` to delete the database or `bin/xenodb reset` to destroy it and create another one. However, it will delete any information stored.

### Collecting Data

It is recommended that you run all of the bot commands with atleast level 1 verbosity, i.e. `-v`. 

To start monitoring the server, run `bin/xenobot start -v`. If you don't want the command to block the terminal, run `nohup bin/xenobot start -v > log 2>&1 &`. This command will store the output of the bot to log file called `log` that you can read. If you start the server while it is already running, it can cause the previous bot to get ghosted by the new one. Use `ps aux` to find any hanging processes and `kill <PID>` to stop them. 

To stop the bot run `bin/xenobot stop`

To collect existing data on your discord server run `bin/xenobot gather <yyyy-mm-dd>` where the date is the furthest back you want to gather data. It defaults to 4 weeks ago. This command will only work if the bot is currently running.

If you only want to collect existing data (and do not need the server monitored), you can run `python3 gather.py <yyyy-mm-dd> -v`. That command will not monitor the server, and will stop blocking the terminal when it is done running.

### Creating Custom Logging

To monitor more discord information you can add any bot listener function supported by the `discord.py` API to the `sql_cog` class in `bot.py`. Then add the sql query to `log_utils.py`. You can find a list of supported `discord.py` API calls at the [discord.py web docs](https://discordpy.readthedocs.io/en/latest/api.html#).

## Known Bugs

- Running gather multiple times will create duplicates in some rows, this can be fixed by using `SELECT DISTINCT` in your sqlite3 queries.
- The setup.py probably doesn't work, you probably need to use venv's to
  guarentee python3.8 is run

## Future Features
- A python analytics tool
- Easy to use backup system
- Easy to use config file
- Add more useful views

### Sub-tools
- White elephant
- Plex cleanup
- Guide for cron-jobs
