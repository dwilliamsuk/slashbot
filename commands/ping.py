## Discord Slash Command Required Imports
from main import discord
from main import logger
from flask_discord_interactions import (Response,
                                        CommandOptionType)

@discord.command()
def ping(ctx):
    "Ping Command"
    logger.info(f"/ping ran by user '{ctx.author.id}' in guild '{ctx.guild_id}' with parameter(s) ''")
    import time
    rectime = (int(ctx.id) / 4194304 + 1420070400000)
    delayms = round((time.time_ns() // 1_000_000)  - rectime)
    if delayms > 0:
        return Response(embed={
            "title": "Pong!",
            "description": f"Took {delayms}ms"
        })
    else:
        return Response(embed={
            "title": "Po- HOLY SHIT!",
            "description": f"You went through fucking time, took {delayms}ms"
        })
