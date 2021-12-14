## Discord Slash Command Required Imports
from main import discord
from flask_discord_interactions import (Response,
                                        CommandOptionType)
from main import logger

## Define the command and parameter(s) it requires
@discord.command(options=[{
    "name": "postcode",
    "description": "A Valid UK Postcode",
    "type": CommandOptionType.STRING,
    "required": True
}])
def coverage(ctx, postcode):
    "Get Mobile Coverage of a postcode via Ofcom"
    logger.info(f"/coverage ran by user '{ctx.author.id}' in guild '{ctx.guild_id}' with parameter(s) '{postcode}'")
    def do_coverage(postcode):
        ## Command Specific Imports
        import requests
        import json
        import re
        postcode = postcode.replace(' ', '')
        ## UK Postcode match regex
        UK_REGEX = '(GIR 0A{2})|[A-PR-UWYZ](([A-HK-Y]?\d\d?)|(\d[A-HJKPSTUW])|' \
                '([A-HK-Y]\d[ABEHMNPRV-Y]))[ ]?\d[ABD-HJLNP-UW-Z]{2}'
        VALID_CODE = re.compile('^{}$'.format(UK_REGEX), re.I)
        ## Check if postcode matches regex
        if bool(VALID_CODE.match(postcode)) == False:
            ctx.edit(Response(embed={
                "title": "Error",
                "description": "Invalid Postcode"
            }))
            return
        postcode = postcode.upper()
        ## Get info from ofcom about postcode
        url = "https://ofcomapi.samknows.com/mobile-coverage-pc-enhanced"
        querystring = {"postcode": postcode}
        response = requests.request("GET", url, data='', params=querystring)
        ## Check if response is valid
        if response.status_code != 200:
            ctx.edit(Response(embed={
                "title": "Error",
                "description": "Unable to process request, please try again later"
            }))
            return
        responsejson = response.json()
        ## If response invalid throw error
        if responsejson['code'] != 'OK':
            ctx.edit(Response(embed={
                "title": "Error",
                "description": responsejson['message']
                }))
            return
        responsejson = responsejson['data']
        ## Replace the letters that the API provides with word that can then be used in command
        responsejson_str = json.dumps(responsejson).replace('G', 'Excellent') \
            .replace('A', 'Good') \
            .replace('R', 'Poor') \
            .replace('C', 'None')
        responsejson = json.loads(responsejson_str)
        ## Setup for the emoji's to correspond with coverage amount
        emojijson = json.loads('{"Excellent":":green_circle:","Good":":orange_circle:",'
                            '"Poor":":red_circle:","None":":black_circle:"}')
        ## Get the two parts of the postcode for nice formatting
        out_code = postcode[:-3].strip()
        inw_code = postcode[-3:].strip()
        ctx.edit(Response(embed={
            "title": "Mobile Coverage",
            "description": out_code + ' ' + inw_code,
            
            "image": {
                "url": "https://maps.googleapis.com/maps/api/staticmap?center=" + postcode + ",uk&zoom=15&size=250x150&key=AIzaSyD_32GA260kPpBtRrfEzUHcF8mNL-ZV7hw"
            },
            "fields": [
                {
                    "name": responsejson[0]['provider'],
                    "value": emojijson[responsejson[0]['data_indoor']] + ' ' + responsejson[0]['data_indoor'] + " Indoors\n"
                            + emojijson[responsejson[0]['data_outdoor']] + ' ' + responsejson[0][
                                'data_outdoor'] + " Outdoors"
                },
                {
                    "name": responsejson[1]['provider'],
                    "value": emojijson[responsejson[1]['data_indoor']] + ' ' + responsejson[1]['data_indoor'] + " Indoors\n"
                            + emojijson[responsejson[1]['data_outdoor']] + ' ' + responsejson[1][
                                'data_outdoor'] + " Outdoors"
                },
                {
                    "name": responsejson[2]['provider'],
                    "value": emojijson[responsejson[2]['data_indoor']] + ' ' + responsejson[2]['data_indoor'] + " Indoors\n"
                            + emojijson[responsejson[2]['data_outdoor']] + ' ' + responsejson[2][
                                'data_outdoor'] + " Outdoors"
                },
                {
                    "name": responsejson[3]['provider'],
                    "value": emojijson[responsejson[3]['data_indoor']] + ' ' + responsejson[3]['data_indoor'] + " Indoors\n"
                            + emojijson[responsejson[3]['data_outdoor']] + ' ' + responsejson[3][
                                'data_outdoor'] + " Outdoors"
                }
            ],
        }))
        return


    ## This threading allows more time for the bot to respond to discord
    import threading
    thread = threading.Thread(target=do_coverage, args=(postcode,))
    thread.start()


    ## This is the initial response sent to discord and prevents the command from timing out
    return Response(deferred=True)