## Discord Slash Command Required Imports
from main import discord
from flask_discord_interactions import (Response,
                                        CommandOptionType)
from main import logger

## Define the command and parameter(s) it requires
@discord.command()
def dog(ctx):
    "Random Dog"
    logger.info(f"/dog ran by user '{ctx.author.id}' in guild '{ctx.guild_id}' with parameter(s) ''")
    import requests
    BASEURL = 'https://dog.ceo/api'
    ENDPOINT = f'{BASEURL}/breeds/image/random'
    response = requests.request("GET", ENDPOINT)
    if response.status_code != 200:
        return Response(embed={"title": "Error!", "description": "Dog bit the cables. Try again later."})
    jsonresp = response.json()
    return Response(embed={
        "image": {"url": f"{jsonresp['message']}"}
    })
