## Discord Slash Command Required Imports
from main import discord
from main import logger
from flask_discord_interactions import (Response,
                                        CommandOptionType)
import threading


## Define the command and parameter(s) it requires
@discord.command(options=[{
    "name": "user",
    "description": "The horny to B O N K",
    "type": CommandOptionType.USER,
    "required": True
}])
def bonk(ctx, user):
    "Horny B O N K"
    logger.info(f"/bonk ran by user '{ctx.author.id}' in guild '{ctx.guild_id}' with parameter(s) '{user.id}'")
    
    def command(user):
        ctx.send(Response(
            content=f'<@{user.id}>',
            embed={
            "title": "B O N K",
            "image": {"url": "https://media1.tenor.com/images/ae34b2d6cbac150bfddf05133a0d8337/tenor.gif?itemid=14889944"}
        }))

    thread = threading.Thread(target=command, args=[user])
    thread.start()

    return Response(deferred=True)
