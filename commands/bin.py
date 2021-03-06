## Discord Slash Command Required Imports
from main import discord
from main import logger
from flask_discord_interactions import (Response,
                                        CommandOptionType)
import threading


## Define the command and parameter(s) it requires
@discord.command()
def bin(ctx):
    "Random Bin"
    logger.info(f"/bin ran by user '{ctx.author.id}' in guild '{ctx.guild_id}' with parameter(s) ''")
    
    def command():
        from random import randint
        binnum = randint(0, 293)
        ctx.send(Response(
            embed={
            "image": {"url": f"https://cloudflare-ipfs.com/ipfs/QmPet28MXQbj32LPWc4EC3a8RybFp4568458sGA1fdyCed/binimages/{binnum}.jpg"}
        }))
        return

    thread = threading.Thread(target=command)
    thread.start()

    return Response(deferred=True)
