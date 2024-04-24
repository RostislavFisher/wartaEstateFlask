import importlib
import os
import sys

from flask import Flask, request
from AI.AIProcessor import AIProcessor
from AI.Model.AbstractModel import AbstractModel
from AI.Model.FineTunedModel import FineTunedModel
from AI.Model.PromptedModel import PromptedModel
from AI.Prompt.TextPrompt import TextPrompt
from AI.Sandbox.Context import Context

from wartaUtils.Config import Config

if getattr(sys, 'frozen', False):
    application_path = os.path.dirname(sys.executable)
elif __file__:
    application_path = os.path.dirname(__file__) + "\\..\\..\\"

config = Config(f"{application_path}\config.json")
listOfEnvironments = config.configJSON["listOfEnvironments"]
print(config.configJSON)
for environment in listOfEnvironments:
    sys.path.append(environment)

from internetAbstractScrapper.Publication import Publication
from internetAbstractScrapper.Service import Service
from internetAppliedScrapper.Realitka.Realitka import Realitka


app = Flask(__name__)

@app.route('/getAllPublicationsWithLocationsInOriginalLanguage')
def getAllPublicationsWithLocationsInOriginalLanguage():
    realitka = Realitka()
    context = Context()
    processor = AIProcessor(context=context)


    listOfServices = [realitka]
    listOfNews = []
    for service in listOfServices:
        news = service.getListOfPublications()
        listOfNews.extend(news)


    listOfPublicationsWithLocations = []
    for new in listOfNews:
        prompt = TextPrompt(new.text.fullTextOriginal)
        response = processor.execute("Location", prompt=prompt)
        publicationWithLocation = {"publication": {"text": new.text.fullTextOriginal}, "location": response.data}
        listOfPublicationsWithLocations.append(publicationWithLocation)

    return str(listOfPublicationsWithLocations)


def start():
    app.run()
