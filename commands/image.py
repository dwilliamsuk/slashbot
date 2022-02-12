## Discord Slash Command Required Imports
from main import discord
from flask_discord_interactions import (Response,
                                        CommandOptionType,
                                        ActionRow,
                                        Button,
                                        ButtonStyles)
from main import logger
import threading
import urllib
import os
import redis
import json
from duckduckgo_search import ddg_images

if os.environ["REDIS_CACHE"] == "True":
    redisIP = os.environ["REDIS_IP"]
    redisPort = os.environ["REDIS_PORT"]
    redisAuth = os.environ["REDIS_AUTH"]
    cacheDB = redis.Redis(host=redisIP, port=redisPort, password=redisAuth, db=0)

## Image search function
def quacksearch(query, num=0):
    query = str(query)
    cleanQuery = urllib.parse.quote_plus(query)

    if os.environ["REDIS_CACHE"] == "True":
        databaseResponse = cacheDB.get(cleanQuery)
        if databaseResponse != None:
            databaseResponse = json.loads(databaseResponse.decode("utf-8"))
            return databaseResponse[num]

    searchres = ddg_images(keywords=query, safesearch='Off', max_results=100)
    if len(searchres) == 0:
        return False

    if os.environ["REDIS_CACHE"] == "True":
        cacheDB.set(cleanQuery, json.dumps(searchres), ex=300)

    return searchres[num]

## Define the command and parameter(s) it requires
@discord.command(options=[{
    "name": "query",
    "description": "What you would like to search for",
    "type": CommandOptionType.STRING,
    "required": True
    }
])
def image(ctx, query):
    "Image Search using DuckDuckGo"
    logger.info(f"/image ran by user '{ctx.author.id}' in guild '{ctx.guild_id}' with parameter(s) '{query}'")

    def command(query):
        ## Error checking if response is invalid
        num = 0
        searchres = quacksearch(query, num)
        if searchres == False:
            ctx.send(Response(embed={
                "title": "Error",
                "description": "Unable to process request, please try again later"
            }))
            return
        ## If all is good send the image search result
        ctx.send(Response(embed={
            "title": "Image Search Results",
            "description": f"[{str(searchres['title'])}]({str(searchres['url'])})",
            "image": {"url": searchres['image']}
            },
            components=[
                ActionRow(components=[
                    Button(
                        style=ButtonStyles.PRIMARY,
                        custom_id=[handle_back, query, num],
                        emoji={
                            "id": "848383585962819585",
                            "name": "Back"
                        }
                    ),
                    Button(
                        style=ButtonStyles.PRIMARY,
                        custom_id=[handle_fwd, query, num],
                        emoji={
                            "id": "848383585374830623",
                            "name": "Forward"
                        }
                    ),
                    Button(
                        style=ButtonStyles.PRIMARY,
                        custom_id=[handle_rand, query, num],
                        emoji={
                            "id": "848380144338993174",
                            "name": "Random"
                        }
                    )
                ])
            ]
        ))
        return

    thread = threading.Thread(target=command, args=[query])
    thread.start()

    return Response(deferred=True)

@discord.custom_handler(custom_id='fwd-5f35-441a-b699-f0438ee24ab0')
def handle_fwd(ctx, query, num: int):
    num = num+1
    if num > 100: num = 0
    searchres = quacksearch(query, num)
    if searchres == False:
            ctx.send(Response(embed={
                "title": "Error",
                "description": "Unable to Process Request, Please Try Again Later (Rate Limited)"
            }))
            return
    return Response(update=True,
    embed={
        "title": "Image Search Results",
        "description": f"[{str(searchres['title'])}]({str(searchres['url'])})",
        "image": {"url": searchres['image']}
    },
    components=[
            ActionRow(components=[
                Button(
                    style=ButtonStyles.PRIMARY,
                    custom_id=[handle_back, query, num],
                    emoji={
                        "id": "848383585962819585",
                        "name": "Back"
                    }
                ),
                Button(
                    style=ButtonStyles.PRIMARY,
                    custom_id=[handle_fwd, query, num],
                    emoji={
                        "id": "848383585374830623",
                        "name": "Forward"
                    }
                ),
                Button(
                    style=ButtonStyles.PRIMARY,
                    custom_id=[handle_rand, query, num],
                    emoji={
                        "id": "848380144338993174",
                        "name": "Random"
                    }
                )
            ])
        ]
    )

@discord.custom_handler(custom_id='back-12d6-41f2-ade9-4970763bf595')
def handle_back(ctx, query, num: int):
    num = num-1
    if num < 0 or num > 100: num = 0
    searchres = quacksearch(query, num)
    if searchres == False:
            ctx.send(Response(embed={
                "title": "Error",
                "description": "Unable to Process Request, Please Try Again Later (Rate Limited)"
            }))
            return
    return Response(update=True,
    embed={
        "title": "Image Search Results",
        "description": f"[{str(searchres['title'])}]({str(searchres['url'])})",
        "image": {"url": searchres['image']}
    },
    components=[
            ActionRow(components=[
                Button(
                    style=ButtonStyles.PRIMARY,
                    custom_id=[handle_back, query, num],
                    emoji={
                        "id": "848383585962819585",
                        "name": "Back"
                    }
                ),
                Button(
                    style=ButtonStyles.PRIMARY,
                    custom_id=[handle_fwd, query, num],
                    emoji={
                        "id": "848383585374830623",
                        "name": "Forward"
                    }
                ),
                Button(
                    style=ButtonStyles.PRIMARY,
                    custom_id=[handle_rand, query, num],
                    emoji={
                        "id": "848380144338993174",
                        "name": "Random"
                    }
                )
            ])
        ]
    )

@discord.custom_handler(custom_id='rand-5ed9-465d-bd8a-87ce2c042836')
def handle_rand(ctx, query, num: int):
    import random
    num = num+random.randint(0, 10)
    if num > 100: num = 0
    searchres = quacksearch(query, num)
    if searchres == False:
            ctx.send(Response(embed={
                "title": "Error",
                "description": "Unable to Process Request, Please Try Again Later (Rate Limited)"
            }))
            return
    return Response(update=True,
    embed={
        "title": "Image Search Results",
        "description": f"[{str(searchres['title'])}]({str(searchres['url'])})",
        "image": {"url": searchres['image']}
    },
    components=[
            ActionRow(components=[
                Button(
                    style=ButtonStyles.PRIMARY,
                    custom_id=[handle_back, query, num],
                    emoji={
                        "id": "848383585962819585",
                        "name": "Back"
                    }
                ),
                Button(
                    style=ButtonStyles.PRIMARY,
                    custom_id=[handle_fwd, query, num],
                    emoji={
                        "id": "848383585374830623",
                        "name": "Forward"
                    }
                ),
                Button(
                    style=ButtonStyles.PRIMARY,
                    custom_id=[handle_rand, query, num],
                    emoji={
                        "id": "848380144338993174",
                        "name": "Random"
                    }
                )
            ])
        ]
    )