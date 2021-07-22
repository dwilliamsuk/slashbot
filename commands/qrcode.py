## Discord Slash Command Required Imports
from main import discord
from main import logger
from flask_discord_interactions import (Response,
                                        CommandOptionType)

@discord.command(options=[{
    "name": "input",
    "description": "Input for the generated QR code",
    "type": CommandOptionType.STRING,
    "required": True
    }
])
def qrcode(ctx, input):
    "Generate a QR code"
    loginput = input.replace('\n', ' ').replace('\r', '')
    logger.info(f"/qrgen ran by user '{ctx.author.id}' in guild '{ctx.guild_id}' with parameter(s) '{loginput}'")
    from urllib.parse import quote
    input_encoded = quote(input)
    return (Response(embed={
        "image": {
            "url": f"https://quickchart.io/qr?light=ffffffff&dark=000000&ecLevel=H&margin=1&size=512&text={input_encoded}"
        }
    }))
