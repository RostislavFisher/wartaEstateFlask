import asyncio
import importlib
import os
import sys
from typing import List
import asyncio
from wartaUtils.Config import Config
from telethon import TelegramClient
from internetAbstractScrapper.Publication import Publication
from internetAbstractScrapper.Service import Service

# from importLocalClass import importLocalClass

# Publication = importLocalClass(
#     r"C:\Users\Rostyslav\Desktop\wartaSoft\wartaEstateFlask\internetAbstractScrapper\Publication.py",
#     "Publication")
#
# Service = importLocalClass(
#     r"C:\Users\Rostyslav\Desktop\wartaSoft\wartaEstateFlask\internetAbstractScrapper\Service.py",
#     "Service")



import sys

from deep_translator import GoogleTranslator
translator = GoogleTranslator(source='auto', target='en')

if getattr(sys, 'frozen', False):
    application_path = os.path.dirname(sys.executable)
elif __file__:
    application_path = os.path.dirname(__file__) + "\\..\\..\\"

config = Config(f"{application_path}\config.json")
# print(config.configJSON)
telegram_api_id = config.configJSON["telegram_api_id"]
telegram_api_hash = config.configJSON["telegram_api_hash"]

class Realitka(Service):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def getListOfPublications(self, **kwargs):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        client = TelegramClient('anon', telegram_api_id, telegram_api_hash, loop=loop)
        client.start()
        # client.connect()
        listOfPublications = []

        async def main():
            channel = await client.get_entity('the_cesko')
            messages = await client.get_messages(channel, limit=2)
            for x in messages:
                publication = Publication()
                # publication.text.fullTextOriginal = x.raw_text
                publication.text.fullTextOriginal = translator.translate(x.raw_text)
                print(publication.text.fullTextOriginal)
                listOfPublications.append(publication)

        loop = asyncio.get_event_loop()
        loop.run_until_complete(main())
        client.disconnect()
        return listOfPublications

# Realitka = Realitka()
# print(Realitka.getListOfPublications())
