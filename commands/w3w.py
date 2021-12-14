## Discord Slash Command Required Imports
from main import discord
from flask_discord_interactions import (Response,
                                        CommandOptionType)
from main import logger
import threading

## Define the command and parameter(s) it requires
@discord.command(options=[{
    "name": "latitude",
    "description": "Latitude",
    "type": CommandOptionType.STRING,
    "required": True
    },
    {
    "name": "longitude",
    "description": "Longitude",
    "type": CommandOptionType.STRING,
    "required": True
    }
])
def w3w(ctx, latitude, longitude):
    "Convert Coordinates to What3Words"
    logger.info(f"/w3w ran by user '{ctx.author.id}' in guild '{ctx.guild_id}' with parameter(s) '{latitude}, {longitude}'")

    def command(latitude, longitude):
        import re
        if re.search('[a-zA-Z]', latitude) or re.search('[a-zA-Z]', longitude): return Response(embed={"title": "Error","description": "Invalid Latitude or Longitude"})
        latitude = str(round(float(latitude), 6))
        longitude = str(round(float(longitude), 6))
        import requests
        regexlat = re.search('^(\+|-)?(?:90(?:(?:\.0{1,6})?)|(?:[0-9]|[1-8][0-9])(?:(?:\.[0-9]{1,6})?))$', latitude)
        regexlng = re.search('^(\+|-)?(?:180(?:(?:\.0{1,6})?)|(?:[0-9]|[1-9][0-9]|1[0-7][0-9])(?:(?:\.[0-9]{1,6})?))$', longitude)
        if not regexlat or not regexlng: ctx.send(Response(embed={"title": "Error","description": "Invalid Latitude or Longitude"}))
        BASEURL = "https://mapapi.what3words.com/api"
        ENDPOINT = f"{BASEURL}/convert-to-3wa?coordinates={latitude},{longitude}&language=en&format=json"
        resp = requests.request("GET", ENDPOINT)
        if resp.status_code == 400:
            jresp = resp.json()
            ctx.send(Response(embed={"title": "Error","description": f"{jresp['error']['message'].capitalize()}","footer": {"text": f"Code: {jresp['error']['code']}"}}))
        if resp.status_code != 200:
            ctx.send(Response(embed={"title": "Error","description": "Try again later"}))
        jresp = resp.json()
        ctx.send(Response(embed={
            "title": f"{jresp['words']}",
            "url": f"{jresp['map']}",
            "image": {"url": f"https://mapapi.what3words.com/map/minimap?lat={jresp['coordinates']['lat']}&lng={jresp['coordinates']['lng']}"},
            "footer": {"text": f"{jresp['coordinates']['lat']}, {jresp['coordinates']['lng']}"}
        }))

    thread = threading.Thread(target=command, args=[latitude, longitude])
    thread.start()

    return Response(deferred=True)