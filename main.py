## Imports
import os
import logging
import sys
import time

from flask import Flask
from flask_discord_interactions import (DiscordInteractions)

## Setup flask and flask discord interactions
app = Flask(__name__)
discord = DiscordInteractions(app)

## Logging Setup for Cloud Run --> stdout
logger = logging.getLogger("main-log")
out_hdlr = logging.StreamHandler(sys.stdout)
out_hdlr.setFormatter(logging.Formatter('%(message)s'))
out_hdlr.setLevel(logging.INFO)
logger.addHandler(out_hdlr)
logger.setLevel(logging.INFO)

## Get environment variables and setup for bot
app.config["DISCORD_CLIENT_ID"] = os.environ["DISCORD_CLIENT_ID"]
app.config["DISCORD_PUBLIC_KEY"] = os.environ["DISCORD_PUBLIC_KEY"]
app.config["DISCORD_CLIENT_SECRET"] = os.environ["DISCORD_CLIENT_SECRET"]

## Imports all commands in the commands folder
import commands

## Define the endpoint that discord should use for interactions
discord.set_route("/interactions")

## Used to monitor instance uptime
startTime = time.time()

## Check if in test mode for per guild command setup rather than global (saves command update time)
if os.environ["TEST_MODE"] == "1":
    print("TESTING MODE ACTIVE")
    print(discord.update_slash_commands(guild_id=os.environ["TESTING_GUILD"]))

## Command update endpoint
@app.route("/commandupdate")
def commandupdate():
    discord.update_slash_commands()
    return "Updated!"

@app.route("/")
def mainpage():
    return f"INSTANCE UP FOR {time.time() - startTime} SECONDS"

## Some flask setup stuffs if you're not using something like gunicorn
if __name__ == '__main__':
    app.run(host='0.0.0.0')
