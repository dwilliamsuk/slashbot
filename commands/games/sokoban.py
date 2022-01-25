## Discord Slash Command Required Imports
from main import logger
from main import discord
from flask_discord_interactions import (Message,
                                        CommandOptionType,
                                        ActionRow,
                                        Button,
                                        ButtonStyles)
from .games import games
import threading

import json
from random import randrange

## Define Player Emoji
playerEmoji = '🤠'

## Define Playable Maps
baseMap = [
      ['⬜', '⬜', '⬜', '⬜', '⬜', '⬜', '⬜'],
      ['⬜', '⬛', '⬛', '⭐', '⬛', '⬛', '⬜'],
      ['⬜', '⬛', playerEmoji, '⬛', '⬛', '⬛', '⬜'],
      ['⬜', '⬛', '⬛', '📦', '⬛', '⬛', '⬜'],
      ['⬜', '⬛', '⬛', '⬛', '📦', '⬛', '⬜'],
      ['⬜', '⬛', '⬛', '⬛', '⬛', '⭐', '⬜'],
      ['⬜', '⬜', '⬜', '⬜', '⬜', '⬜', '⬜']
    ],[
      ['⬜', '⬜', '⬜', '⬜', '⬜', '⬜', '⬜'],
      ['⬜', '⭐', '⬛', '⬛', '⬛', '⬛', '⬜'],
      ['⬜', '⭐', '⬛', '⬛', '⬛', '⬛', '⬜'],
      ['⬜', '⬜', '⬜', '⬛', '⬛', '⬛', '⬜'],
      ['⬜', '⬛', '📦', '📦', '⬛', '⬛', '⬜'],
      ['⬜', playerEmoji, '⬛', '⬛', '⬛', '⬛', '⬜'],
      ['⬜', '⬜', '⬜', '⬜', '⬜', '⬜', '⬜']
    ],[
      ['⬜', '⬜', '⬜', '⬜', '⬜', '⬜', '⬜'],
      ['⬜', '⬜', '⬜', playerEmoji, '⬛', '⭐', '⬜'],
      ['⬜', '⬜', '⬜', '⬛', '⬛', '⬜', '⬜'],
      ['⬜', '⬜', '⬛', '⬛', '📦', '⭐', '⬜'],
      ['⬜', '⬛', '⬛', '📦', '⬛', '⬛', '⬜'],
      ['⬜', '⬛', '⬛', '⬛', '📦', '⭐', '⬜'],
      ['⬜', '⬜', '⬜', '⬜', '⬜', '⬜', '⬜']
    ],[
      ['⬜', '⬜', '⬜', '⬜', '⬜', '⬜', '⬜'],
      ['⬜', '⬛', '⬛', '⬛', '⬛', playerEmoji, '⬜'],
      ['⬜', '⬛', '⬛', '⬛', '⬛', '⬜', '⬜'],
      ['⬜', '⬛', '⭐', '⬜', '📦', '⬜', '⬜'],
      ['⬜', '⬛', '📦', '⬛', '⬛', '⭐', '⬜'],
      ['⬜', '⬛', '⬛', '⬛', '📦', '⭐', '⬜'],
      ['⬜', '⬜', '⬜', '⬜', '⬜', '⬜', '⬜']
    ],[
      ['⬜', '⬜', '⬜', '⬜', '⬜', '⬜', '⬜'],
      ['⬜', playerEmoji, '⬛', '⬛', '⬛', '⭐', '⬜'],
      ['⬜', '⬛', '⬜', '⬜', '⬛', '⬛', '⬜'],
      ['⬜', '⬛', '⬛', '⬜', '⬛', '⬜', '⬜'],
      ['⬜', '⬛', '📦', '⬛', '⬛', '⬛', '⬜'],
      ['⬜', '⬛', '⬛', '⬛', '⬛', '⬛', '⬜'],
      ['⬜', '⬜', '⬜', '⬜', '⬜', '⬜', '⬜']
    ]


## Searches for and returns player location as x, y
def playerLocator(map):
    for lineNum, line in enumerate(map):
        for pixelNum, pixel in enumerate(line):
            if pixel == playerEmoji:
                x = pixelNum
                y = lineNum
    return x, y

## Moves player location with box movement and bounding rules
def playerMove(map, direction):
    playerLocation = playerLocator(map)
    x = playerLocation[0]
    y = playerLocation[1]
    if direction == 1:
        lastSpace = map[y][x]
        leftSpace = map[y][x-1]
        
        if leftSpace in ('⬜', '⭐', '🌟'):
            return map
        elif leftSpace == '📦':
            if map[y][x-2] in ('⬜', '📦', '🌟'):
                return map
            elif map[y][x-2] == '⭐':
                map[y][x-2] = '🌟'
                map[y][x-1] = '⬛'
                for line in map:
                    for pixel in line:
                        if pixel == '⭐':
                            return map
                return True
            map[y][x-2] = leftSpace
            map[y][x-1] = lastSpace
            map[y][x] = '⬛'
        else:
            map[y][x-1] = lastSpace
            map[y][x] = leftSpace
        return map
    elif direction == 2:
        lastSpace = map[y][x]
        rightSpace = map[y][x+1]
        
        if rightSpace in ('⬜', '⭐', '🌟'):
            return map
        elif rightSpace == '📦':
            if map[y][x+2] in ('⬜', '📦', '🌟'):
                return map
            elif map[y][x+2] == '⭐':
                map[y][x+2] = '🌟'
                map[y][x+1] = '⬛'
                for line in map:
                    for pixel in line:
                        if pixel == '⭐':
                            return map
                return True
            map[y][x+2] = rightSpace
            map[y][x+1] = lastSpace
            map[y][x] = '⬛'
        else:
            map[y][x+1] = lastSpace
            map[y][x] = rightSpace
        return map
    elif direction == 3:
        lastSpace = map[y][x]
        upSpace = map[y-1][x]
        
        if upSpace in ('⬜', '⭐', '🌟'):
            return map
        elif upSpace == '📦':
            if map[y-2][x] in ('⬜', '📦', '🌟'):
                return map
            elif map[y-2][x] == '⭐':
                map[y-2][x] = '🌟'
                map[y-1][x] = '⬛'
                for line in map:
                    for pixel in line:
                        if pixel == '⭐':
                            return map
                return True
            map[y-2][x] = upSpace
            map[y-1][x] = lastSpace
            map[y][x] = '⬛'
        else:
            map[y-1][x] = lastSpace
            map[y][x] = upSpace
        return map
    elif direction == 4:
        lastSpace = map[y][x]
        downSpace = map[y+1][x]
        
        if downSpace in ('⬜', '⭐', '🌟'):
            return map
        elif downSpace == '📦':
            if map[y+2][x] in ('⬜', '📦', '🌟'):
                return map
            elif map[y+2][x] == '⭐':
                map[y+2][x] = '🌟'
                map[y+1][x] = '⬛'
                for line in map:
                    for pixel in line:
                        if pixel == '⭐':
                            return map
                return True
            map[y+2][x] = downSpace
            map[y+1][x] = lastSpace
            map[y][x] = '⬛'
        else:
            map[y+1][x] = lastSpace
            map[y][x] = downSpace
        return map

## Convert map from map storage format to discord compatible message
def mapToMessage(map):
    msgMap = ""
    for line in map:
        for pixel in line:
            msgMap = msgMap + pixel
        msgMap = msgMap + "\n"
    return msgMap

## The algorithm used to convert a map to state (described below)
def mapToStateAlgo(item):
    for char in item:
        if char == '⬜':
            return 1
        elif char == '⬛':
            return 2
        elif char == playerEmoji:
            return 3
        elif char == '⭐':
            return 4
        elif char == '📦':
            return 5
        elif char == '🌟':
            return 6

## Convert map from map storage format (list) to trimmed down state so that it can fit
## in discord state limits (100 total chars)
def mapToState(inputMap):
    stateMap = []
    for line in inputMap:
        line = list(map(mapToStateAlgo, line))
        stateMap.append(line)
    stateMap = json.dumps(stateMap)
    stateMap = stateMap.replace(', ', '')
    return stateMap

## The algorithm used to convert a state to map (described below)
def stateToMapAlgo(item):
    if item == 1:
        return '⬜'
    elif item == 2:
        return '⬛'
    elif item == 3:
        return playerEmoji
    elif item == 4:
        return '⭐'
    elif item == 5:
        return '📦'
    elif item == 6:
        return '🌟'

## Convert back from a state to map storage format (list) so that it can be used internally
def stateToMap(inputState):
    sessionMap = []
    tempString = ''
    for char in inputState:
        if char in ('[', ']'):
            tempString += char
        elif char.isdigit() == True:
            tempString += char + ','
    tempString = tempString.replace(',]', '],')
    tempString = tempString.replace('],]', ']]')
    for line in json.loads(tempString):
        line = list(map(stateToMapAlgo, line))
        sessionMap.append(line)
    return sessionMap

## This is the main function that is used to setup sokoban using all the previously defined functions
## when slashbot is invoked
def mainCommand(refresh=False, mapNumber=999, author=0):
    if mapNumber == 999:
        mapNumber = randrange(len(baseMap))
    sessionMap = baseMap[mapNumber]
    return(Message(
        update=refresh,
        content=mapToMessage(sessionMap),
        components=[
            ActionRow(components=[
                Button(
                    style=ButtonStyles.PRIMARY,
                    custom_id=[handle_left, mapToState(sessionMap), mapNumber, author],
                    emoji={
                        "id": "935275367701291058",
                        "name": "Left"
                        }),
                Button(
                    style=ButtonStyles.PRIMARY,
                    custom_id=[handle_right, mapToState(sessionMap), mapNumber, author],
                    emoji={
                        "id": "935275367902629968",
                        "name": "Right"
                        }),
                Button(
                    style=ButtonStyles.PRIMARY,
                    custom_id=[handle_up, mapToState(sessionMap), mapNumber, author],
                    emoji={
                        "id": "935275367692914708",
                        "name": "Up"
                        }),
                Button(
                    style=ButtonStyles.PRIMARY,
                    custom_id=[handle_down, mapToState(sessionMap), mapNumber, author],
                    emoji={
                        "id": "935275367583850568",
                        "name": "Down"
                        }),
                Button(
                    style=ButtonStyles.DANGER,
                    custom_id=[handle_restart, mapNumber, author],
                    emoji={
                        "id": "935275979629289492",
                        "name": "Restart"
                        })
            ]
            )
        ])
    )

## Define the command and parameter(s) it requires
@games.command()
def sokoban(ctx):
    "sokoban"
    logger.info(f"/sokoban ran by user '{ctx.author.id}' in guild '{ctx.guild_id}' with parameter(s) ''")

    def command():
        ctx.send(mainCommand(mapNumber=randrange(len(baseMap)), author=ctx.author.id))
        return
    
    thread = threading.Thread(target=command)
    thread.start()

    return Message(deferred=True)

## This is the algorithm used to convert a map in map format (list) to a win map
def winMapAlgo(item):
    for char in item:
        if char == '⬜':
            return '🟩'
        elif char == playerEmoji:
            return '🥳'
        else:
            return char
          
## This handler is used when a move results in a win
def handle_win(sessionMap, mapNumber, author):
    mapNumber=999
    winMap = []
    for line in sessionMap:
        winMap.append(list(map(winMapAlgo, line)))
    return Message(
            update=True,
            content=mapToMessage(winMap),
            components=[
                ActionRow(components=[
                    Button(
                        style=ButtonStyles.SUCCESS,
                        custom_id=[handle_restart, mapNumber, author],
                        emoji={
                            "id": "935275979629289492",
                            "name": "Restart"
                            }
                    )
                ]
                )
            ]
    )

## This handler is used to reset the current game
@discord.custom_handler(custom_id='sres')
def handle_restart(ctx, mapNumber=999, author=0):
    if ctx.author.id != author:
        return
    mapNumber = int(mapNumber)
    return(mainCommand(True, mapNumber, author))

## This handler is used to move player left
@discord.custom_handler(custom_id='sleft')
def handle_left(ctx, sessionMap, mapNumber, author):
    if ctx.author.id != author:
        return
    sessionMap = stateToMap(sessionMap)
    sessionMapMove = playerMove(sessionMap, 1)
    if sessionMapMove == True: return(handle_win(sessionMap, mapNumber, author))
    return(Message(
            update=True,
            content=mapToMessage(sessionMapMove),
            components=[
                ActionRow(components=[
                    Button(
                        style=ButtonStyles.PRIMARY,
                        custom_id=[handle_left, mapToState(sessionMapMove), mapNumber, author],
                        emoji={
                            "id": "935275367701291058",
                            "name": "Left"
                            }),
                    Button(
                        style=ButtonStyles.PRIMARY,
                        custom_id=[handle_right, mapToState(sessionMapMove), mapNumber, author],
                        emoji={
                            "id": "935275367902629968",
                            "name": "Right"
                            }),
                    Button(
                        style=ButtonStyles.PRIMARY,
                        custom_id=[handle_up, mapToState(sessionMapMove), mapNumber, author],
                        emoji={
                            "id": "935275367692914708",
                            "name": "Up"
                            }),
                    Button(
                        style=ButtonStyles.PRIMARY,
                        custom_id=[handle_down, mapToState(sessionMapMove), mapNumber, author],
                        emoji={
                            "id": "935275367583850568",
                            "name": "Down"
                            }),
                    Button(
                        style=ButtonStyles.DANGER,
                        custom_id=[handle_restart, mapNumber, author],
                        emoji={
                            "id": "935275979629289492",
                            "name": "Restart"
                            })
                ]
                )
            ])
        )
    
## This handler is used to move player right
@discord.custom_handler(custom_id='sright')
def handle_right(ctx, sessionMap, mapNumber, author):
    if ctx.author.id != author:
        return
    sessionMap = stateToMap(sessionMap)
    sessionMapMove = playerMove(sessionMap, 2)
    if sessionMapMove == True: return(handle_win(sessionMap, mapNumber, author))
    return(Message(
            update=True,
            content=mapToMessage(sessionMapMove),
            components=[
                ActionRow(components=[
                    Button(
                        style=ButtonStyles.PRIMARY,
                        custom_id=[handle_left, mapToState(sessionMapMove), mapNumber, author],
                        emoji={
                            "id": "935275367701291058",
                            "name": "Left"
                            }),
                    Button(
                        style=ButtonStyles.PRIMARY,
                        custom_id=[handle_right, mapToState(sessionMapMove), mapNumber, author],
                        emoji={
                            "id": "935275367902629968",
                            "name": "Right"
                            }),
                    Button(
                        style=ButtonStyles.PRIMARY,
                        custom_id=[handle_up, mapToState(sessionMapMove), mapNumber, author],
                        emoji={
                            "id": "935275367692914708",
                            "name": "Up"
                            }),
                    Button(
                        style=ButtonStyles.PRIMARY,
                        custom_id=[handle_down, mapToState(sessionMapMove), mapNumber, author],
                        emoji={
                            "id": "935275367583850568",
                            "name": "Down"
                            }),
                    Button(
                        style=ButtonStyles.DANGER,
                        custom_id=[handle_restart, mapNumber, author],
                        emoji={
                            "id": "935275979629289492",
                            "name": "Restart"
                            })
                ]
                )
            ])
        )

## This handler is used to move player up
@discord.custom_handler(custom_id='sup')
def handle_up(ctx, sessionMap, mapNumber, author):
    if ctx.author.id != author:
        return
    sessionMap = stateToMap(sessionMap)
    sessionMapMove = playerMove(sessionMap, 3)
    if sessionMapMove == True: return(handle_win(sessionMap, mapNumber, author))
    return(Message(
            update=True,
            content=mapToMessage(sessionMapMove),
            components=[
                ActionRow(components=[
                    Button(
                        style=ButtonStyles.PRIMARY,
                        custom_id=[handle_left, mapToState(sessionMapMove), mapNumber, author],
                        emoji={
                            "id": "935275367701291058",
                            "name": "Left"
                            }),
                    Button(
                        style=ButtonStyles.PRIMARY,
                        custom_id=[handle_right, mapToState(sessionMapMove), mapNumber, author],
                        emoji={
                            "id": "935275367902629968",
                            "name": "Right"
                            }),
                    Button(
                        style=ButtonStyles.PRIMARY,
                        custom_id=[handle_up, mapToState(sessionMapMove), mapNumber, author],
                        emoji={
                            "id": "935275367692914708",
                            "name": "Up"
                            }),
                    Button(
                        style=ButtonStyles.PRIMARY,
                        custom_id=[handle_down, mapToState(sessionMapMove), mapNumber, author],
                        emoji={
                            "id": "935275367583850568",
                            "name": "Down"
                            }),
                    Button(
                        style=ButtonStyles.DANGER,
                        custom_id=[handle_restart, mapNumber, author],
                        emoji={
                            "id": "935275979629289492",
                            "name": "Restart"
                            })
                ]
                )
            ])
        )

## This handler is used to move player down
@discord.custom_handler(custom_id='sdown')
def handle_down(ctx, sessionMap, mapNumber, author):
    if ctx.author.id != author:
        return
    sessionMap = stateToMap(sessionMap)
    sessionMapMove = playerMove(sessionMap, 4)
    if sessionMapMove == True: return(handle_win(sessionMap, mapNumber, author))
    return(Message(
            update=True,
            content=mapToMessage(sessionMapMove),
            components=[
                ActionRow(components=[
                    Button(
                        style=ButtonStyles.PRIMARY,
                        custom_id=[handle_left, mapToState(sessionMapMove), mapNumber, author],
                        emoji={
                            "id": "935275367701291058",
                            "name": "Left"
                            }),
                    Button(
                        style=ButtonStyles.PRIMARY,
                        custom_id=[handle_right, mapToState(sessionMapMove), mapNumber, author],
                        emoji={
                            "id": "935275367902629968",
                            "name": "Right"
                            }),
                    Button(
                        style=ButtonStyles.PRIMARY,
                        custom_id=[handle_up, mapToState(sessionMapMove), mapNumber, author],
                        emoji={
                            "id": "935275367692914708",
                            "name": "Up"
                            }),
                    Button(
                        style=ButtonStyles.PRIMARY,
                        custom_id=[handle_down, mapToState(sessionMapMove), mapNumber, author],
                        emoji={
                            "id": "935275367583850568",
                            "name": "Down"
                            }),
                    Button(
                        style=ButtonStyles.DANGER,
                        custom_id=[handle_restart, mapNumber, author],
                        emoji={
                            "id": "935275979629289492",
                            "name": "Restart"
                            })
                ]
                )
            ])
        )
