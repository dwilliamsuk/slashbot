## Discord Slash Command Required Imports
from main import discord
from main import logger
from flask_discord_interactions import (Response,
                                        CommandOptionType)

from decimal import Decimal, ROUND_HALF_UP
import requests
import enum
from datetime import datetime

cents = Decimal('0.01')

class Currencies(enum.Enum):
    GBP = "GBP"
    EUR = "EUR"
    USD = "USD"
    CAD = "CAD"
    DKK = "DKK"
    AED = "AED"
    MAD = "MAD"
    BGN = "BGN"
    RSD = "RSD"
    INR = "INR"
    CNY = "CNY"
    JPY = "JPY"
    CHF = "CHF"

uri = "https://www.mastercard.co.uk"

@discord.command(annotations={"amount": "Amount to convert", "input": "Input Currency", "output": "Output Currency"})
def currency(ctx, amount: float,  input: Currencies, output: Currencies):
    "Currency Conversion"
    amount = Decimal(amount).quantize(cents, ROUND_HALF_UP)
    logger.info(f"/currency ran by user '{ctx.author.id}' in guild '{ctx.guild_id}' with parameter(s) '{amount}, {input}, {output}'")
    if amount < 0.01:
        return Response(f"Error! Cannot convert anything less than 0.01", ephemeral=True)
    if input == output:
        return Response(f"{input} = {output} surprisingly enough", ephemeral=True)
    def convertcurrency(amount: Decimal, input, output):
        req = f"{uri}/settlement/currencyrate/fxDate=0000-00-00;transCurr={input};crdhldBillCurr={output};bankFee=0;transAmt={amount}/conversion-rate"
        headers = {"referer": "https://www.mastercard.co.uk/en-gb/personal/get-support/convert-currency.html"}
        resp = requests.request("GET", req, headers=headers)
        if resp.status_code == 200:
            return resp.json()
        else:
            return False
    conversion = convertcurrency(amount, input, output)
    if conversion == False:
        return Response(f"Error! Unable to get conversion rate. Please try again later.", ephemeral=True)
    convamount = Decimal(conversion['data']['transAmt']).quantize(cents, ROUND_HALF_UP)
    outputamount = Decimal(conversion['data']['crdhldBillAmt']).quantize(cents, ROUND_HALF_UP)
    conversionrate = conversion['data']['conversionRate']
    lastupdate = datetime.strptime(conversion['date'], '%Y-%m-%d %H:%M:%S')
    lastupdate = lastupdate.isoformat()
    return Response(embed={
            "title": f"Currency Conversion",
            "description": f"{convamount} {input} --> {outputamount} {output}",
            "footer": {
                "text": f"With a conversion rate of {conversionrate}"
            },
            "timestamp": lastupdate
            })