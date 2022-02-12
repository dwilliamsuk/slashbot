## Discord Slash Command Required Imports
from main import logger
from main import discord
from flask_discord_interactions import (Message,
                                        CommandOptionType,
                                        ActionRow,
                                        Button,
                                        ButtonStyles,
                                        ApplicationCommandType)
import threading

## Command Specific Imports
from duckduckgo_search import ddg_translate

translateLanguageNames = {'af': 'Afrikaans', 'am': 'Amharic', 'ar': 'Arabic', 'as': 'Assamese', 'az': 'Azerbaijani',
 'bg': 'Bulgarian', 'bn': 'Bangla', 'bs': 'Bosnian', 'ca': 'Catalan', 'cs': 'Czech', 'cy': 'Welsh', 'da': 'Danish',
  'de': 'German', 'el': 'Greek', 'en': 'English', 'es': 'Spanish', 'et': 'Estonian', 'fa': 'Persian', 'fi': 'Finnish',
   'fil': 'Filipino', 'fj': 'Fijian', 'fr': 'French', 'fr-CA': 'French (Canada)', 'ga': 'Irish', 'gu': 'Gujarati',
    'he': 'Hebrew', 'hi': 'Hindi', 'hr': 'Croatian', 'ht': 'Haitian Creole', 'hu': 'Hungarian', 'hy': 'Armenian',
     'id': 'Indonesian', 'is': 'Icelandic', 'it': 'Italian', 'iu': 'Inuktitut', 'ja': 'Japanese', 'kk': 'Kazakh',
      'km': 'Khmer', 'kmr': 'Kurdish (Northern)', 'kn': 'Kannada', 'ko': 'Korean', 'ku': 'Kurdish (Central)',
       'lo': 'Lao', 'lt': 'Lithuanian', 'lv': 'Latvian', 'mg': 'Malagasy', 'mi': 'Maori', 'ml': 'Malayalam',
        'mr': 'Marathi', 'ms': 'Malay', 'mt': 'Maltese', 'mww': 'Hmong Daw', 'my': 'Myanmar (Burmese)',
         'nb': 'Norwegian', 'ne': 'Nepali', 'nl': 'Dutch', 'or': 'Odia', 'otq': 'Querétaro Otomi', 'pa': 'Punjabi',
          'pl': 'Polish', 'prs': 'Dari', 'ps': 'Pashto', 'pt': 'Portuguese (Brazil)', 'pt-PT': 'Portuguese (Portugal)',
           'ro': 'Romanian', 'ru': 'Russian', 'sk': 'Slovak', 'sl': 'Slovenian', 'sm': 'Samoan', 'sq': 'Albanian',
            'sr-Cyrl': 'Serbian (Cyrillic)', 'sr-Latn': 'Serbian (Latin)', 'sv': 'Swedish', 'sw': 'Swahili',
             'ta': 'Tamil', 'te': 'Telugu', 'th': 'Thai', 'ti': 'Tigrinya', 'tlh-Latn': 'Klingon', 'to': 'Tongan',
              'tr': 'Turkish', 'ty': 'Tahitian', 'uk': 'Ukrainian', 'ur': 'Urdu', 'vi': 'Vietnamese', 'yua': 'Yucatec Maya',
               'yue': 'Cantonese (Traditional)', 'zh-Hans': 'Chinese Simplified', 'zh-Hant': 'Chinese Traditional'}


@discord.command(type=ApplicationCommandType.MESSAGE)
def Translate(ctx, msg):
    logger.info(f"/translate ran by user '{ctx.author.id}' in guild '{ctx.guild_id}' with parameter(s) '{msg.content}'")
    
    def command(ctx, msg):
        convertTo = 'en'
        inputText = msg.content
        translation = ddg_translate(keywords=inputText, to=convertTo)
        
        if len(translation) == 0:
            ctx.send(Message(
            embed={
                "title": "Error",
                "description": "Unable to Process Request, Please Try Again Later."
            }))
            return
        
        detectedLanguage = translateLanguageNames[translation[0]['detected_language']]
        convertedTo = translateLanguageNames[convertTo]

        ctx.send(Message(
        embed={
            "title": f"Translation from {detectedLanguage} --> {convertedTo}",
            "fields": [
                {
                    "name": f"{detectedLanguage}",
                    "value": f"```{translation[0]['original']}```"
                },
                {
                    "name": f"{convertedTo}",
                    "value": f"```{translation[0]['translated']}```"
                }
            ]
        }))
        return
        

    thread = threading.Thread(target=command, args=[ctx, msg])
    thread.start()

    return Message(deferred=True)
