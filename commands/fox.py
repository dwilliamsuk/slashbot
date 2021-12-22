## Discord Slash Command Required Imports
from main import discord
from flask_discord_interactions import (Response,
                                        CommandOptionType)
from main import logger
import threading

## Define the command and parameter(s) it requires
@discord.command()
def fox(ctx):
    "Random Fox"
    logger.info(f"/fox ran by user '{ctx.author.id}' in guild '{ctx.guild_id}' with parameter(s) ''")

    def command():
        import requests
        BASEURL = 'https://randomfox.ca'
        ENDPOINT = f'{BASEURL}/floof/'
        response = requests.request("GET", ENDPOINT)
        if response.status_code != 200:
            ctx.send(Response(embed={"title": "Error!", "description": "Fox bit the cables. Try again later."}))
            return
        jsonresp = response.json()
        ctx.send(Response(embed={
            "image": {"url": f"{jsonresp['image']}"}
        }))
        return

    thread = threading.Thread(target=command)
    thread.start()

    return Response(deferred=True)
