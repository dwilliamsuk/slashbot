## Discord Slash Command Required Imports
from main import logger
from flask_discord_interactions import (Response,
                                        CommandOptionType)
from .convert import convert
import threading

from pint import UnitRegistry
import enum

ureg = UnitRegistry()
Q = ureg.Quantity

class Units(enum.Enum):
    Minute = "minute"
    Hour = "hour"
    Day = "day"
    Week = "week"
    Fortnight = "fortnight"
    Month = "month"
    Year = "year"
    Decade = "decade"
    Century = "century"
    Millennium = "millennium"
    Eon = "eon"

class Plurals(enum.Enum):
    Minute = "minutes"
    Hour = "hours"
    Day = "days"
    Week = "weeks"
    Fortnight = "fortnights"
    Month = "months"
    Year = "years"
    Decade = "decades"
    Century = "centuries"
    Millennium = "millennia"
    Eon = "eons"


@convert.command(annotations={"amount": "Amount to convert", "input": "Input Time", "output": "Output Time"})
def time(ctx, amount: float,  input: Units, output: Units):

    def command(amount: float, input: Units, output: Units):
        convoutput = Q(amount, input).to(output).magnitude

        inputname = Plurals[Units(input).name].value
        outputname = Plurals[Units(output).name].value

        if amount <= 1: inputname = inputname = input
        if convoutput <= 1: outputname = outputname = output

        ctx.send(Response(embed={
                "title": f"Unit Conversion",
                "description": f"{amount} {inputname} --> {convoutput} {outputname}"
                }))
    
    thread = threading.Thread(target=command, args=[amount, input, output])
    thread.start()

    return Response(deferred=True)