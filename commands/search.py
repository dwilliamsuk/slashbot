## Discord Slash Command Required Imports
from main import discord
from main import logger
from flask_discord_interactions import (Message,
                                        CommandOptionType,
                                        ApplicationCommandType,
                                        SelectMenu,
                                        SelectMenuOption,
                                        ActionRow,
                                        Embed)
import threading

## Command Specific Imports
import requests
from urllib import parse

@discord.custom_handler(custom_id='lstSrch')
def handleListSearch(ctx):
    logger.info(f"/search ran by user '{ctx.author.id}' in guild '{ctx.guild_id}' with parameter(s) '{ctx.values[0]}'")

    safequery = parse.quote((ctx.values[0]).replace('_', ' '))
    uri = f"https://api.duckduckgo.com/?q={safequery}&format=json&pretty=0&skip_disambig=1"

    try:
        response = requests.request("GET", uri)
        ddgResp = response.json()
    except Exception as e:
        return Message(
            embed={
                "title": "Error",
                "description": "Unable to find any instant answers on that topic.",
            })
        return
    
    discordEmbed = {
        "title": f"{ddgResp['AbstractSource']}",
        "description": f"{ddgResp['AbstractText']}",
        "url": ddgResp['AbstractURL'],
        "footer": {
            "icon_url": "https://pbs.twimg.com/profile_images/1452668733533601802/uSn3mxSe_400x400.jpg",
            "text": "Results from DuckDuckGo"
        }
    }
    
    if ddgResp.get('Image'):
        discordEmbed['thumbnail'] = {"url": f"https://duckduckgo.com{ddgResp['Image']}"}

    options = []

    for option in ctx.message.components[0]['components'][0]['options']:
        if ctx.values[0] == option['value']:
            options.append(SelectMenuOption(label=option['label'], value=option['value'], default=True))
        else:
            options.append(SelectMenuOption(label=option['label'], value=option['value']))
    
    menu = SelectMenu(
                placeholder="Decisions, decisions. All of them wrong!",
                custom_id=[handleListSearch],
                options=options
            )
    
    return Message(update=True, embed=discordEmbed, components=[ActionRow(components=[menu])])

@discord.command(options=[{
    "name": "query",
    "description": "What you would like to search for",
    "type": CommandOptionType.STRING,
    "required": True
}])
def search(ctx, query):
    "Instant Answers using DuckDuckGo"
    logger.info(f"/search ran by user '{ctx.author.id}' in guild '{ctx.guild_id}' with parameter(s) '{query}'")

    def command(query):
        safequery = parse.quote(query)
        uri = f"https://api.duckduckgo.com/?q={safequery}&format=json&pretty=0"

        try:
            response = requests.request("GET", uri)
            ddgResp = response.json()
        except Exception as e:
            ctx.send(Message(
                embed={
                    "title": "Error",
                    "description": "Unable to find any instant answers on that topic.",
                }))
            return
        
        if ddgResp['Type'] == 'D':
            
            discordFields = []
            options = []
            for topic in ddgResp['RelatedTopics']:
                if not topic.get('Name'):
                    topicName = topic['FirstURL']
                    topicName = parse.unquote(topicName)
                    topicName = (topicName.split('/', 3))[-1]
                    topicName = topicName.replace('_', ' ')
                    topicText = topic['Result']
                    topicText = (topicText.split('</a>'))[-1]
                    discordFields.append({"name": f"{topicName}","value": f"[{topicName}]({topic['FirstURL']}), {topicText}"})
                    options.append(SelectMenuOption(label=topicName, value=(parse.unquote(((topic['FirstURL']).split('/', 3))[-1]))))
                pass
            
            menu = SelectMenu(
                placeholder="Decisions, decisions. All of them wrong!",
                custom_id=[handleListSearch],
                options=options
            )

            ctx.send(Message(
                embed={
                    "title": f"{ddgResp['AbstractSource']}",
                    "url": ddgResp['AbstractURL'],
                    "fields": discordFields,
                    "footer": {
                        "icon_url": "https://pbs.twimg.com/profile_images/1452668733533601802/uSn3mxSe_400x400.jpg",
                        "text": "Results from DuckDuckGo"
                    }
                },
                components=[ActionRow(components=[menu])]
                ))
            return

        elif ddgResp['Type'] == 'A':
            discordEmbed = {
                "title": f"{ddgResp['AbstractSource']}",
                "description": f"{ddgResp['AbstractText']}",
                "url": ddgResp['AbstractURL'],
                "footer": {
                    "icon_url": "https://pbs.twimg.com/profile_images/1452668733533601802/uSn3mxSe_400x400.jpg",
                    "text": "Results from DuckDuckGo"
                }
            }
            
            if ddgResp.get('Image'):
                discordEmbed['thumbnail'] = {"url": f"https://duckduckgo.com{ddgResp['Image']}"}

            ctx.send(Message(embed=discordEmbed))
            return

        else:
            ctx.send(Message(
                embed={
                    "title": "Error",
                    "description": "Unable to find any instant answers on that topic.",
                }))
            return
    
    thread = threading.Thread(target=command, args=[query])
    thread.start()

    return Message(deferred=True)

@discord.command(type=ApplicationCommandType.MESSAGE)
def Search(ctx, msg):
    logger.info(f"/search ran by user '{ctx.author.id}' in guild '{ctx.guild_id}' with parameter(s) '{msg.content}'")

    def command(query):
        safequery = parse.quote(query)
        uri = f"https://api.duckduckgo.com/?q={safequery}&format=json&pretty=0"

        try:
            response = requests.request("GET", uri)
            ddgResp = response.json()
        except Exception as e:
            ctx.send(Message(
                embed={
                    "title": "Error",
                    "description": "Unable to find any instant answers on that topic.",
                }))
            return
        
        if ddgResp['Type'] == 'D':
            
            discordFields = []
            options = []
            for topic in ddgResp['RelatedTopics']:
                if not topic.get('Name'):
                    topicName = topic['FirstURL']
                    topicName = parse.unquote(topicName)
                    topicName = (topicName.split('/', 3))[-1]
                    topicName = topicName.replace('_', ' ')
                    topicText = topic['Result']
                    topicText = (topicText.split('</a>'))[-1]
                    discordFields.append({"name": f"{topicName}","value": f"[{topicName}]({topic['FirstURL']}), {topicText}"})
                    options.append(SelectMenuOption(label=topicName, value=(parse.unquote(((topic['FirstURL']).split('/', 3))[-1]))))
                pass
            
            menu = SelectMenu(
                placeholder="Decisions, decisions. All of them wrong!",
                custom_id=[handleListSearch],
                options=options
            )

            ctx.send(Message(
                embed={
                    "title": f"{ddgResp['AbstractSource']}",
                    "url": ddgResp['AbstractURL'],
                    "fields": discordFields,
                    "footer": {
                        "icon_url": "https://pbs.twimg.com/profile_images/1452668733533601802/uSn3mxSe_400x400.jpg",
                        "text": "Results from DuckDuckGo"
                    }
                },
                components=[ActionRow(components=[menu])]
                ))
            return

        elif ddgResp['Type'] == 'A':
            discordEmbed = {
                "title": f"{ddgResp['AbstractSource']}",
                "description": f"{ddgResp['AbstractText']}",
                "url": ddgResp['AbstractURL'],
                "footer": {
                    "icon_url": "https://pbs.twimg.com/profile_images/1452668733533601802/uSn3mxSe_400x400.jpg",
                    "text": "Results from DuckDuckGo"
                }
            }
            
            if ddgResp.get('Image'):
                discordEmbed['thumbnail'] = {"url": f"https://duckduckgo.com{ddgResp['Image']}"}

            ctx.send(Message(embed=discordEmbed))
            return

        else:
            ctx.send(Message(
                embed={
                    "title": "Error",
                    "description": "Unable to find any instant answers on that topic.",
                }))
            return
    
    thread = threading.Thread(target=command, args=[msg.content])
    thread.start()

    return Message(deferred=True)
