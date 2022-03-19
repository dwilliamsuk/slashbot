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

baseMap = [
      ['🔳', '🔳', '🔳', '🔳', '🔳', '🔳'],
      ['🔳', '🔳', '🔳', '🔳', '🔳', '🔳'],
      ['🔳', '🔳', '🔳', '🔳', '🔳', '🔳'],
      ['🔳', '🔳', '🔳', '🔳', '🔳', '🔳'],
      ['🔳', '🔳', '🔳', '🔳', '🔳', '🔳']
    ]

def winCheck(map):

    def diagonalCheck(map):
        def topLeftToRight(map):
            horizontalMap = []
            horizontalMap.append([map[0][0], map[1][1], map[2][2], map[3][3], map[4][4]])
            horizontalMap.append([map[0][1], map[1][2], map[2][3], map[3][4], map[4][5]])
            horizontalMap.append([map[0][2], map[1][3], map[2][4], map[3][5]])
            return horizontalCheck(horizontalMap)
        
        def topRightToLeft(map):
            horizontalMap = []
            horizontalMap.append([map[0][5], map[1][4], map[2][3], map[3][2], map[4][1]])
            horizontalMap.append([map[0][4], map[1][3], map[2][2], map[3][1], map[4][0]])
            horizontalMap.append([map[0][3], map[1][2], map[2][1], map[3][0]])
            return horizontalCheck(horizontalMap)
        
        def bottomLeftToRight(map):
            horizontalMap = []
            horizontalMap.append([map[4][0], map[3][1], map[2][2], map[1][3], map[0][4]])
            horizontalMap.append([map[4][1], map[3][2], map[2][3], map[1][4], map[0][5]])
            horizontalMap.append([map[4][2], map[3][3], map[2][4], map[1][5]])
            return horizontalCheck(horizontalMap)
        
        def bottomRightToLeft(map):
            horizontalMap = []
            horizontalMap.append([map[4][5], map[3][4], map[2][3], map[1][2], map[0][1]])
            horizontalMap.append([map[4][4], map[3][3], map[2][2], map[1][1], map[0][0]])
            horizontalMap.append([map[4][3], map[3][2], map[2][1], map[1][0]])
            return horizontalCheck(horizontalMap)
        
        if topLeftToRight(map) == True or topRightToLeft(map) == True or bottomLeftToRight(map) == True or bottomRightToLeft(map) == True:
            return True
        return False

    def verticalCheck(map):
        horizontalMap = []
        for spaceIndex, _ in enumerate(map[0]):
            tempList = []
            for index in range(5): tempList.append(map[index][spaceIndex])
            horizontalMap.append(tempList)
        return horizontalCheck(horizontalMap)

    def horizontalCheck(map):
        for row in map:
            lineSquareCount = 0
            prevSpace = ''
            for space in row:
                if space == prevSpace and space != '🔳':
                    lineSquareCount += 1
                    if lineSquareCount >= 3: return True
                    prevSpace = space
                else:
                    lineSquareCount = 0
                    prevSpace = space 
        return False
        
    
    if diagonalCheck(map) or verticalCheck(map) or horizontalCheck(map) == True:
        return True
    return False

def gameMove(map, move: int, currPlayer: int):
    mapNum = 4
    playerTypes = ['🟩', '🟥']
    moveLocation = map[mapNum][move]
    if moveLocation == '🔳': 
        map[mapNum][move] = playerTypes[currPlayer]
    else:
        while moveLocation in ('🟥', '🟩') and mapNum >= 0:
            mapNum += -1
            moveLocation = map[mapNum][move]
            if moveLocation == '🔳':
                map[mapNum][move] = playerTypes[currPlayer]
                break
    return map, winCheck(map)


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
        if char == '🔳':
            return 1
        elif char == '🟩':
            return 2
        elif char == '🟥':
            return 3

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
        return '🔳'
    elif item == 2:
        return '🟩'
    elif item == 3:
        return '🟥'


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

def gameToEmbed(map, playerOne: int, playerTwo: int, currPlayer: int, update=1, win=False):
    if win == True:
        style = ButtonStyles.DANGER
        if currPlayer == 0: style = ButtonStyles.SUCCESS

        colour = 15548997
        if currPlayer == 0: colour = 5763719

        winner = playerTwo
        if currPlayer == 1: winner = playerOne

        msg = Message(
            content=f"🎉 <@{winner}> WON!",
            embed={"color": colour,
            "fields": [
                {
                    "name": "Game",
                    "value": mapToMessage(map)
                }
            ]},
        allowed_mentions={"parse": []},
        update=update,
        components=[ActionRow(components=[]), ActionRow(components=[])])
        for num in range(6):
            actionrow = 0
            if num > 2: actionrow = 1
            (msg.components[actionrow].components).append(Button(
                            style=style,
                            custom_id=[move_handler, mapToState(map), num, playerOne, playerTwo, currPlayer],
                            label=f"{num+1}",
                            disabled=True
                        ))
        return msg

    style = ButtonStyles.SUCCESS
    if currPlayer == 0: style = ButtonStyles.DANGER

    colour = 5763719
    if currPlayer == 0: colour = 15548997

    content = f"🟥 <@{playerOne}> VS <@{playerTwo}> 🟩"
    if playerTwo == 0: content = f"<@{playerOne}> VS ?"

    msg = Message(
        content=content,
        embed={"color": colour,
        "fields": [
            {
                "name": "Game",
                "value": mapToMessage(map)
            }
        ]},
    allowed_mentions={"parse": []},
    update=update,
    components=[ActionRow(components=[]), ActionRow(components=[])])
    for num in range(6):
        actionrow = 0
        if num > 2: actionrow = 1
        (msg.components[actionrow].components).append(Button(
                        style=style,
                        custom_id=[move_handler, mapToState(map), num, playerOne, playerTwo, currPlayer],
                        label=f"{num+1}",
                    ))
    return msg

## Define the command and parameter(s) it requires
@games.command()
def fourinarow(ctx):
    "Four in a Row is a two-player connection board game."
    logger.info(f"/fourinarow ran by user '{ctx.author.id}' in guild '{ctx.guild_id}' with parameter(s) ''")

    def command():
        ctx.send(gameToEmbed(baseMap, ctx.author.id, 0, 0, 0))
        return
    
    thread = threading.Thread(target=command)
    thread.start()

    return Message(deferred=True)


@discord.custom_handler(custom_id='move')
def move_handler(ctx, map, move: int, playerOne: int, playerTwo: int, currPlayer: int):
    map = stateToMap(map)
    author = int(ctx.author.id)
    
    ## Set second player if not already set and check if player is current game player
    if playerTwo == 0 and author != playerOne: playerTwo = author
    if author != playerOne and author != playerTwo: return
    
    ## Current player swap and check current player
    if currPlayer == 0 and playerOne == author:
        currPlayer = 1 
    elif currPlayer == 1 and playerTwo == author:
        currPlayer = 0
    else:
        return
    
    currGameMove = gameMove(map, move, currPlayer)
    map = currGameMove[0]
    win = currGameMove[1]

    if win == True:
        return(gameToEmbed(map, playerOne, playerTwo, currPlayer, win=True))

    return(gameToEmbed(map, playerOne, playerTwo, currPlayer))
