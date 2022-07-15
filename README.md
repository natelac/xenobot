# xenobot

## TODO

- BUGFIXES
  - Figure out what is getting converted (position 1?)
  - Figure out what's up with the datetime.datetime object, should it be converted to UTC before being passed?
- Track discord information
  - What guilds the bot is in
  - Information per guild
    - All user information
      - Log their public information, and when they change it and what to
      - Log of member statuses
    - All channel information
      - Log of messages sent, and by whom
      - Log when a channel is created/deleted/changed
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

## Questions
- Nickname vs username, can you track and log name changes across both? Is there an on_* command?
- Max character length of emoji
