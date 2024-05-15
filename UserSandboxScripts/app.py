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
from AI.Sandbox.SandboxFilterUnit import *
from AI.Sandbox.Item import Item
from AI.Sandbox.Response import Response
from AI.Sandbox.Sandbox import Sandbox
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
    def deleteEmpty(item, **kwargs):
        if item.item.data["publication"].text.fullTextOriginal != "":
            return Response(200, "Positive", item=item.item)
        return Response(400, "Negative", item=item.item)

    def deleteNotRealEstatePublications(item, **kwargs):
        prompt = TextPrompt(item.item.data["publication"].text.fullTextOriginal)
        response = processor.execute("IsRealEstatePublication", prompt=prompt)
        if response.data['result'] == "YES":
            return Response(200, "Positive", item=item.item)
        return Response(400, "Negative", item=item.item)

    def getLocation(item, **kwargs):
        prompt = TextPrompt(item.item.data["publication"].text.fullTextOriginal)
        response = processor.execute("Location", prompt=prompt)

        item.item.data["location"] = response.data
        return Response(200, "AdditionalInformation", item=item.item)

    def getPrice(item, **kwargs):
        prompt = TextPrompt(item.item.data["publication"].text.fullTextOriginal)
        response = processor.execute("RealEstatePrice", prompt=prompt)

        item.item.data["price"] = response.data
        return Response(200, "AdditionalInformation", item=item.item)

    def getTypeOfAccommodation(item, **kwargs):
        # ft:davinci-002:personal::9N6pociK
        prompt = TextPrompt(item.item.data["publication"].text.fullTextOriginal)
        response = processor.execute("TypeOfAccommodation", prompt=prompt)
        item.item.data["TypeOfAccommodation"] = response.data
        return Response(200, "AdditionalInformation", item=item.item)

    realitka = Realitka()
    context = Context()
    processor = AIProcessor(context=context)
    sandbox = Sandbox(context=context)
    filterUnit = SandboxFilterUnit()
    filterUnit.function = deleteEmpty
    sandbox.addUnit(filterUnit)
    filterUnitDeleteNotRealEstatePublications = SandboxFilterUnit()
    filterUnitDeleteNotRealEstatePublications.function = deleteNotRealEstatePublications
    sandbox.addUnit(filterUnitDeleteNotRealEstatePublications)
    additionalInformationUnit = SandboxFilterUnit()
    additionalInformationUnit.function = getLocation
    sandbox.addUnit(additionalInformationUnit)
    additionalInformationPrice = SandboxFilterUnit()
    additionalInformationPrice.function = getPrice
    sandbox.addUnit(additionalInformationPrice)
    additionalInformationTypeOfAccommodation = SandboxFilterUnit()
    additionalInformationTypeOfAccommodation.function = getTypeOfAccommodation
    sandbox.addUnit(additionalInformationTypeOfAccommodation)

    listOfServices = [realitka]
    listOfNews = []
    for service in listOfServices:
        news = service.getListOfPublications()
        listOfNews.extend(news)
    listOfItems = []
    for new in listOfNews:
        item = Item({"publication": new})
        listOfItems.append(item)

    sandbox.run(listOfItems)

    result = sandbox.getAllResultsWaiting()

    jsonResult = {"result": []}
    for item in result:
        jsonResult["result"].append({"publication": item.item.data["publication"].text.fullTextOriginal,
                                     "location": item.item.data["location"],
                                     "price": item.item.data["price"]
                                     })
    return str(jsonResult)


def start():
    app.run()
