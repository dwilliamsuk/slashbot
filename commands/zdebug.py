## Discord Slash Command Required Imports
from main import discord
from main import logger
from flask_discord_interactions import (Response,
                                        CommandOptionType)

zdebug = discord.command_group("zdebug")

import os
owner = os.environ["owner"]

@zdebug.command()
def serverinfo(ctx):
    if ctx.author.id != owner:
        return Response("You are not allowed to use this command", ephemeral=True)
    import platform
    import time
    import main
    uname = platform.uname()
    return Response(f"Instance Info: {uname}\n Uptime = {time.time() - main.startTime}", ephemeral=True)