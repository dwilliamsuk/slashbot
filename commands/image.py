## Discord Slash Command Required Imports
from main import discord
from flask_discord_interactions import (Response,
                                        CommandOptionType,
                                        ActionRow,
                                        Button,
                                        ButtonStyles)
from main import logger
import threading

## Image search function
def quacksearch(query, num=0):
    from commands.modules import duckimgsearch as quack
    query = str(query)
    searchres = quack.search(query)
    if searchres == 'Err' or not searchres:
        return False
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
        ## If all is good send the image search result
        ctx.send(Response(embed={
            "title": "Image Search Results",
            "description": f"[{searchres['title']}]({searchres['url']})",
            "image": {"url": searchres['thumbnail']}
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

    thread = threading.Thread(target=command, args=[query])
    thread.start()

    return Response(deferred=True)

@discord.custom_handler()
def handle_fwd(ctx, query, num: int):
    num = num+1
    if num > 100: num = 0
    searchres = quacksearch(query, num)
    return Response(update=True,
    embed={
        "title": "Image Search Results",
        "description": f"[{searchres['title']}]({searchres['url']})",
        "image": {"url": searchres['thumbnail']}
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

@discord.custom_handler()
def handle_back(ctx, query, num: int):
    num = num-1
    if num < 0 or num > 100: num = 0
    a = quacksearch(query, num)
    searchres = quacksearch(query, num)
    return Response(update=True,
    embed={
        "title": "Image Search Results",
        "description": f"[{searchres['title']}]({searchres['url']})",
        "image": {"url": searchres['thumbnail']}
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

@discord.custom_handler()
def handle_rand(ctx, query, num: int):
    import random
    num = num+random.randint(0, 10)
    if num > 100: num = 0
    searchres = quacksearch(query, num)
    return Response(update=True,
    embed={
        "title": "Image Search Results",
        "description": f"[{searchres['title']}]({searchres['url']})",
        "image": {"url": searchres['thumbnail']}
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