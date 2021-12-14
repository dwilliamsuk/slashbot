## Discord Slash Command Required Imports
from main import discord
from flask_discord_interactions import (Response,
                                        CommandOptionType)
from main import logger
import threading

## Define the command and parameter(s) it requires
@discord.command()
def fortune(ctx):
    "Fortune Cookie Advice"
    logger.info(f"/fortune ran by user '{ctx.author.id}' in guild '{ctx.guild_id}' with parameter(s) ''")

    def command():
        import requests
        BASEURL = 'https://api.adviceslip.com'
        ENDPOINT = f'{BASEURL}/advice'
        response = requests.request("GET", ENDPOINT)
        if response.status_code != 200:
            ctx.send(Response(embed={"title": "Error!", "description": "Ran out of fortune cookies!"}))
        jsonresp = response.json()
        ctx.send(Response(embed={
            "title": "You crack open your fortune cookie and find within...",
            "description": f"\"{jsonresp['slip']['advice']}\""
        }))

    thread = threading.Thread(target=command)
    thread.start()

    return Response(deferred=True)