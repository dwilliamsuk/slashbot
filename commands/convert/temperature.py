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
    Celsius = "degree_Celsius"
    Fahrenheit = "degree_Fahrenheit"
    Kelvin = "kelvin"
    Rankine = "degree_Rankine"
    Reaumur = "degree_Reaumur"
    Planck = "planck_temperature"


@convert.command(annotations={"amount": "Amount to convert", "input": "Input Temperature", "output": "Output Temperature"})
def temperature(ctx, amount: float,  input: Units, output: Units):
    convoutput = Q(amount, input).to(output).magnitude

    return Response(embed={
            "title": f"Unit Conversion",
            "description": f"{amount} {Units(input).name} --> {convoutput} {Units(output).name}"
            })