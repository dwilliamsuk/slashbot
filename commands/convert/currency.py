## Discord Slash Command Required Imports
from main import logger
from flask_discord_interactions import (Response,
                                        CommandOptionType)
import threading
from .convert import convert

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
    IDR = "IDR"
    MYR = "MYR"
    CHF = "CHF"
    CNY = "CNY"
    JPY = "JPY"
    TRY = "TRY"
    RUB = "RUB"

uri = "https://www.mastercard.co.uk"

@convert.command(annotations={"amount": "Amount to convert", "input": "Input Currency", "output": "Output Currency"})
def currency(ctx, amount: float,  input: Currencies, output: Currencies):
    "Currency Conversion"

    def command(amount: float, input: Currencies, output: Currencies):
        amount = Decimal(amount).quantize(cents, ROUND_HALF_UP)
        logger.info(f"/currency ran by user '{ctx.author.id}' in guild '{ctx.guild_id}' with parameter(s) '{amount}, {input}, {output}'")
        if amount < 0.01:
            ctx.send(Response(f"Error! Cannot convert anything less than 0.01", ephemeral=True))
            return
        if input == output:
            ctx.send(Response(f"{input} = {output} surprisingly enough", ephemeral=True))
            return
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
            ctx.send(Response(f"Error! Unable to get conversion rate. Please try again later.", ephemeral=True))
            return
        convamount = Decimal(conversion['data']['transAmt']).quantize(cents, ROUND_HALF_UP)
        outputamount = Decimal(conversion['data']['crdhldBillAmt']).quantize(cents, ROUND_HALF_UP)
        conversionrate = conversion['data']['conversionRate']
        lastupdate = datetime.strptime(conversion['date'], '%Y-%m-%d %H:%M:%S')
        lastupdate = lastupdate.isoformat()
        ctx.send(Response(embed={
                "title": f"Currency Conversion",
                "description": f"{convamount} {input} --> {outputamount} {output}",
                "footer": {
                    "text": f"With a conversion rate of {conversionrate}"
                },
                "timestamp": lastupdate
                }))
        return

    thread = threading.Thread(target=command, args=[amount, input, output])
    thread.start()

    return Response(deferred=True)
