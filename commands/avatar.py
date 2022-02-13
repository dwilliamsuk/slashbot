## Discord Slash Command Required Imports
from main import discord
from main import logger
from flask_discord_interactions import (Response,
                                        CommandOptionType,
                                        Member,
                                        ApplicationCommandType)
import threading
import requests

## Define the command and parameter(s) it requires
@discord.command(options=[{
    "name": "user",
    "description": "The User",
    "type": CommandOptionType.USER,
    "required": True
}])
def avatar(ctx, user: Member):
    "View a Users Avatar"
    logger.info(f"/avatar ran by user '{ctx.author.id}' in guild '{ctx.guild_id}' with parameter(s) '{user.id}'")

    def command(user: Member):
        avatarURL = f"https://cdn.discordapp.com/avatars/{user.id}/{user.avatar_hash}?size=512"

        hasAvatarCheck = requests.head(avatarURL)
        if hasAvatarCheck.status_code != 200:
            avatarURL = f"https://cdn.discordapp.com/embed/avatars/{int(user.discriminator)%5}.png?size=512"
        
        ctx.send(Response(
            embed={
            "title": f"{user.username}'s Avatar",
            "image": {"url": avatarURL}
        }))
        return
    
    thread = threading.Thread(target=command, args=[user])
    thread.start()

    return Response(deferred=True)

@discord.command(type=ApplicationCommandType.USER)
def Avatar(ctx, user):
    logger.info(f"/avatar ran by user '{ctx.author.id}' in guild '{ctx.guild_id}' with parameter(s) '{user.id}'")

    def command(user: Member):
        avatarURL = f"https://cdn.discordapp.com/avatars/{user.id}/{user.avatar_hash}?size=512"

        hasAvatarCheck = requests.head(avatarURL)
        if hasAvatarCheck.status_code != 200:
            avatarURL = f"https://cdn.discordapp.com/embed/avatars/{int(user.discriminator)%5}.png?size=512"

        ctx.send(Response(
            embed={
            "title": f"{user.username}'s Avatar",
            "image": {"url": avatarURL}
        }))
        return
    
    thread = threading.Thread(target=command, args=[user])
    thread.start()

    return Response(deferred=True)

