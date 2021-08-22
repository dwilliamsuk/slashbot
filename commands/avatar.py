## Discord Slash Command Required Imports
from main import discord
from main import logger
from flask_discord_interactions import (Response,
                                        CommandOptionType,
                                        Member)

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
    return Response(
        embed={
        "title": f"{user.username}'s Avatar",
        "image": {"url": f"{user.avatar_url}?size=512"}
    })
