# __init__.py
## This file imports all the commands I'd like to be available for use. If a command isn't in here it means I've disabled it for slashbot for whatever reason.

## Slash Commands
from .random import random
from .image import image
from .bonk import bonk
from .weather import weather
from .info import info
from .invite import invite
from .avatar import avatar
from .qrcode import qrcode
from .cat import cat
from .dog import dog
from .fox import fox
from .w3w import w3w
from .ping import ping
from .bin import bin
from .fortune import fortune
from .coinflip import coinflip
from .search import search

## Slash Command Groups
import commands.convert
import commands.games

## Apps Commands
from .translate import Translate
from .avatar import Avatar
from .search import Search
