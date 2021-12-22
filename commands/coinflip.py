## Discord Slash Command Required Imports
from main import discord
from main import logger
from flask_discord_interactions import (Response,
                                        CommandOptionType)
import threading
import random

## Define the command and parameter(s) it requires
@discord.command()
def coinflip(ctx):
    "Coin Flip"
    logger.info(f"/coinflip ran by user '{ctx.author.id}' in guild '{ctx.guild_id}' with parameter(s) ''")

    def command():
        choices = ["https://www.royalmint.com/globalassets/the-royal-mint/images/pages/new-pound-coin/large_new_pound.png", "Heads"], ["https://www.royalmint.com/globalassets/the-royal-mint/images/pages/new-pound-coin/large_new_pound_rev.png", "Tails"]
        coin = random.choice(choices)
        ctx.send(Response(embed={
            "title": f"{coin[1]}",
            "image": {
                "url": coin[0]
            }
                }))
        return
    
    thread = threading.Thread(target=command)
    thread.start()

    return Response(deferred=True)
