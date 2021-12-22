## Discord Slash Command Required Imports
from main import discord
from flask_discord_interactions import (Response,
                                        CommandOptionType)
from main import logger
import threading

## Define the command and parameter(s) it requires
@discord.command()
def invite(ctx):
    "Bot Invite"
    logger.info(f"/invite ran by user '{ctx.author.id}' in guild '{ctx.guild_id}' with parameter(s) ''")

    def command():
        ctx.send(Response(embed={
                "author": {
                    "name": "SlashBot",
                    "icon_url": "https://cdn.discordapp.com/app-icons/818189563536343081/6a04d974b41fa3ce18e87ef71dd4b5b9.png?size=256"
                },
                "description": "You can invite me by [clicking here](https://discord.com/api/oauth2/authorize?client_id=828301046207741974&scope=applications.commands)",
                }))
    
    thread = threading.Thread(target=command)
    thread.start()

    return Response(deferred=True)