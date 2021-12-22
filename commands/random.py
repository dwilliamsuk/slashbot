## Discord Slash Command Required Imports
from main import discord
from flask_discord_interactions import (Response,
                                        CommandOptionType)
from main import logger
import threading

## Define the command and parameter(s) it requires
@discord.command(options=[{
    "name": "fact",
    "description": "Your chosen fact format my good sire",
    "type": CommandOptionType.STRING,
    "required": True,
    "choices": [
        {
            "name": "Random",
            "value": "random"
        },
        {
            "name": "Fact Of The Day",
            "value": "notsorandom"
        }
    ]
}])
def random(ctx, fact):
    "Random Facts!"
    logger.info(f"/random ran by user '{ctx.author.id}' in guild '{ctx.guild_id}' with parameter(s) '{fact}'")

    def command(fact):
        ## Command Specific Imports
        import requests
        ## Command Specific Imports
        embedtitle = "Random Fact!"
        url = "https://uselessfacts.jsph.pl/random.json"
        ## Get chosen fact type and setup accordingly 
        if fact == 'notsorandom':
            embedtitle = "Fact Of The Day!"
            url = "https://uselessfacts.jsph.pl/today.json"
        querystring = {"language":"en"}
        response = requests.request("GET", url, data='', params=querystring)
        ## Ensure response is valid and if not throw error
        if response.status_code != 200:
            ctx.send(Response(embed={
                "title": "Error",
                "description": "Unable to process request, please try again later"
            }))
            return
        ## If all is good send response to discord
        ctx.send(Response(embed={
            "title": embedtitle,
            "description": '``'+response.json()['text']+'``',
            "url": response.json()['permalink']
            }))
        return
    
    thread = threading.Thread(target=command, args=[fact])
    thread.start()

    return Response(deferred=True)
