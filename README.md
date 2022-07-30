# xenobot

A bot used for gathering 

## TODO
- Figure out if there is a way to check if the bot process is running so you
  can make alternate decisions
- Finish "controller.py gather"
  - Have it write in named pipe --OR--
  - Have it create and close a bot to gather data
- Don't spend too much time on the above two, focus on polishing everything in
  general

## Future Features
- Using "crontab -e" to make a cron job for the bot!!!
- Standardize logging (fx log.info vs log.debug) 
- Fix duplicate values for "gather.py"
  - I think it's just things that have incremental primary keys?
- Make a config file
  - Set time intervals for active monitoring
  - Set default earliest\_date for gathering data
  - Store default DB\_PATH and GUILD
  - Add whitelist/blacklists to channels/users etc.
- Comment code and files better
- Implement passive logging
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
