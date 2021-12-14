## Discord Slash Command Required Imports
from main import discord
from main import logger
from flask_discord_interactions import (Response,
                                        CommandOptionType)
import threading

## Define the command and parameter(s) it requires
@discord.command()
def info(ctx):
    "Bot Info"
    logger.info(f"/info ran by user '{ctx.author.id}' in guild '{ctx.guild_id}' with parameter(s) ''")

    def command():
        ctx.send(Response(embed={
                "author": {
                    "name": "SlashBot",
                    "icon_url": "https://cdn.discordapp.com/app-icons/818189563536343081/6a04d974b41fa3ce18e87ef71dd4b5b9.png?size=256"
                },
                "fields": [
                    {
                        "name": "What?",
                        "value": "SlashBot is a bot that uses the new discord slash commands stuffs that aims to be a sort of swiss army knife bot"
                    },
                    {
                        "name": "Why?!",
                        "value": "NotSoBot was wank and I liked the image commands to terror people"
                    },
                    {
                        "name": "Where?!?!?!?!",
                        "value": "SlashBot runs off Google Cloud Run"
                    },
                    {
                        "name": "WHOMST?!?!?!?!",
                        "value": "https://github.com/TheJaffaMeme"
                    },
                ],
                }))
    
    thread = threading.Thread(target=command)
    thread.start()

    return Response(deferred=True)
