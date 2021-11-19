## Discord Slash Command Required Imports
from main import logger
from flask_discord_interactions import (Response,
                                        CommandOptionType)
from .convert import convert

from pint import UnitRegistry
import enum

ureg = UnitRegistry()
Q = ureg.Quantity

class Units(enum.Enum):
    Metre = "meter"
    Centimetre = "centimeter"
    Millimetre = "millimetre"
    Inch = "inch"
    Foot = "foot"
    Yard = "yard"
    Mile = "mile"
    Kilometre = "kilometer"
    LightYear = "lightyear"

class Plurals(enum.Enum):
    Metre = "meters"
    Centimetre = "centimeters"
    Millimetre = "millimetres"
    Inch = "inches"
    Foot = "feet"
    Yard = "yards"
    Mile = "miles"
    Kilometre = "kilometers"
    LightYear = "lightyears"


@convert.command(annotations={"amount": "Amount to convert", "input": "Input Length", "output": "Output Length"})
def length(ctx, amount: float,  input: Units, output: Units):

    convoutput = Q(amount, input).to(output).magnitude

    inputname = Plurals[Units(input).name].value
    outputname = Plurals[Units(output).name].value

    if amount <= 1: inputname = inputname = input
    if convoutput <= 1: outputname = outputname = output

    return Response(embed={
            "title": f"Unit Conversion",
            "description": f"{amount} {inputname} --> {convoutput} {outputname}"
            })