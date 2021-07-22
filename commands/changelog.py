## Discord Slash Command Required Imports
from main import discord
from flask_discord_interactions import (Response,
                                        CommandOptionType)
from main import logger

## Define the command and parameter(s) it requires
@discord.command()
def changelog(ctx):
    "Bot Changelog"
    logger.info(f"/changelog ran by user '{ctx.author.id}' in guild '{ctx.guild_id}' with parameter(s) ''")
    return Response(embed={
            "author": {
                "name": "SlashBot Changelog",
                "icon_url": "https://cdn.discordapp.com/app-icons/818189563536343081/6a04d974b41fa3ce18e87ef71dd4b5b9.png?size=256"
            },
            "fields": [
                {
                    "name": "26/05/2021",
                    "value": "Removed coverage command - Unused and frankly abuse of ofcom api"
                },
                {
                    "name": "26/05/2021",
                    "value": "Added changelog command"
                },
                {
                    "name": "26/05/2021",
                    "value": "Added fortune cookie command"
                },
                {
                    "name": "29/04/2021",
                    "value": "Added bin command"
                },
            ],
            })