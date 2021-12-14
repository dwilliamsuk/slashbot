## Discord Slash Command Required Imports
from main import discord
from flask_discord_interactions import (Response,
                                        CommandOptionType)

import asyncio
import json

## !!
## This command is still in development and will not have any explanations, 
## I am waiting on discord to implement more channel info so I can check if the channel is marked NSFW.
## NEEDS THREADING IF EVER COMPLETED
## !!

## Define the command and parameter(s) it requires
@discord.command(options=[{
    "name": "query",
    "description": "What you would like to search for",
    "type": CommandOptionType.STRING,
    "required": True
    },
])
def r34(ctx, query):
    "Rule34 Image Search"
    import random
    resp = asyncio.run(get_sin(query))
    if resp == None:
        return Response(embed={
            "title": "Error",
            "description": f"No images found with query: '{query}'",
            "footer": dict(icon_url=ctx.author.avatar_url, 
            text="Command Run By " + ctx.author.username + '#' + ctx.author.discriminator),
        })
    chosenpost = resp[random.randint(0, len(resp))]
    return Response(embed={
        "title": "Rule34 Search Results",
        "description": '"'+query+'"',
        "image": {"url": chosenpost.file_url},
        "footer": dict(icon_url=ctx.author.avatar_url, 
        text="Command Run By " + ctx.author.username + '#' + ctx.author.discriminator),
        })

async def get_sin(sin):
    import rule34
    loop = asyncio.get_event_loop()
    r34 = rule34.Rule34(loop)
    resp = await r34.getImages(tags=f"{sin} -video")
    return resp