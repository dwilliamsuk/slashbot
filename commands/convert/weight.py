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
    Gram = "gram"
    Kilogram = "kilogram"
    Milligram = "milligram"
    Ounce = "ounce"
    Pound = "pound"
    Tonne = "metric_ton"


class Plurals(enum.Enum):
    Gram = "grams"
    Kilogram = "kilograms"
    Milligram = "milligrams"
    Ounce = "ounces"
    Pound = "pounds"
    Tonne = "tonnes"


@convert.command(annotations={"amount": "Amount to convert", "input": "Input Weight", "output": "Output Weight"})
def weight(ctx, amount: float,  input: Units, output: Units):

    convoutput = Q(amount, input).to(output).magnitude

    inputname = Plurals[Units(input).name].value
    outputname = Plurals[Units(output).name].value

    if amount <= 1: inputname = inputname = input
    if convoutput <= 1: outputname = outputname = output

    return Response(embed={
            "title": f"Unit Conversion",
            "description": f"{amount} {inputname} --> {convoutput} {outputname}"
            })