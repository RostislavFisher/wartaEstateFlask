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




import sys

from deep_translator import GoogleTranslator
translator = GoogleTranslator(source='auto', target='en')

if getattr(sys, 'frozen', False):
    application_path = os.path.dirname(sys.executable)
elif __file__:
    application_path = os.path.dirname(__file__) + "\\..\\..\\"

config = Config(f"{application_path}\config.json")
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
            channel = await client.get_entity('realitka_chat')
            messages = await client.get_messages(channel, limit=40)

            listOfProcessedMessages = []
            for x in messages:
                if x.text is not None:
                    if x.text not in listOfProcessedMessages:
                        listOfProcessedMessages.append(x.text)
                        publication = Publication()
                        publication.text.fullTextOriginal = translator.translate(x.text)
                        listOfPublications.append(publication)

        loop = asyncio.get_event_loop()
        loop.run_until_complete(main())
        client.disconnect()
        return listOfPublications
