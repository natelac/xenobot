def set_intents():
    # Intents the bot will use
    intents = discord.Intents.all()
    intents.members = True
    intents.presences = True
    intents.guilds = True
    intents.messages = True
    intents.message_content = True
    intents.reactions = True
