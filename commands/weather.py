## Discord Slash Command Required Imports
from main import discord
from flask_discord_interactions import (Response,
                                        CommandOptionType)
from main import logger
import threading

## Define the command and parameter(s) it requires
@discord.command(options=[{
    "name": "city",
    "description": "The city you'd like the weather for",
    "type": CommandOptionType.STRING,
    "required": True
    },
    {
    "name": "country",
    "description": "An optional country code",
    "type": CommandOptionType.STRING,
    "required": False
    }
])
def weather(ctx, city, country=''):
    "Get the Weather for a Location"
    logger.info(f"/weather ran by user '{ctx.author.id}' in guild '{ctx.guild_id}' with parameter(s) '{city}, {country}'")

    def command(city, country):
        ## Command Specific Imports
        import os
        import requests
        ## Command Specific Imports
        ## Grab openweathermap key environment variable and set base URL
        appid = os.environ["owmkey"]
        baseurl = f"https://api.openweathermap.org/data/2.5/weather?appid={appid}&units=metric&q="
        ## Ensure user hasn't used & in query to prevent arguments from being added to the request, if so throw error
        if '&' in city or '&' in country:
            ctx.send(Response(embed={
                "title": "Nice Try",
                "url": "https://cdn.discordapp.com/attachments/820398852992401468/822894568709947392/oi.mp4"
            }))
        url = f"{baseurl}{city},{country}"
        response = requests.request("GET", url)
        rjson = response.json()
        ## Ensure response is valid
        if response.status_code != 200:
            ctx.send(Response(embed={
                "title": "Error",
                "description": rjson['message'].capitalize()
            }))
        ## If all is good send response
        ctx.send(Response(embed={
                "title": f"{rjson['name']}, {rjson['sys']['country']}",
                "description": f"{rjson['weather'][0]['description'].title()}",
                "thumbnail": {"url": f"https://openweathermap.org/img/wn/{rjson['weather'][0]['icon']}@2x.png"},
                "image": {
                "url": f"https://maps.googleapis.com/maps/api/staticmap?center={rjson['coord']['lat']},{rjson['coord']['lon']}&zoom=10&size=250x150&key=AIzaSyD_32GA260kPpBtRrfEzUHcF8mNL-ZV7hw"},
                "fields": [
                    {
                        "name": "Temperature",
                        "value": f"Temp: {rjson['main']['temp']}°C\nFeels Like: {rjson['main']['feels_like']}°C\nMin: {rjson['main']['temp_min']}°C\nMax: {rjson['main']['temp_max']}°C",
                        "inline": False,
                    },
                    {
                        "name": "Humidity",
                        "value": f"{rjson['main']['humidity']}%",
                        "inline": False,
                    },
                    {
                        "name": "Wind Speed",
                        "value": f"{rjson['wind']['speed']}mph",
                        "inline": False,
                    },
                ]
            }))
        
    thread = threading.Thread(target=command, args=[city, country])
    thread.start()

    return Response(deferred=True)