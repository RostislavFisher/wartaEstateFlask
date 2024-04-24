import datetime
from abc import ABCMeta

from internetAbstractScrapper.TextClass import TextClass
class Publication(metaclass=ABCMeta):
    def __init__(self, **kwargs):
        self.description = kwargs.get("description", "")
        self.link = kwargs.get("link", "")
        self.source = kwargs.get("source", "")
        self.text = kwargs.get("text", TextClass())
        self.publishedOn = kwargs.get("publishedOn", datetime.datetime.now())
        self.imgPreview = kwargs.get("imgPreview", "")

    def setData(self, **kwargs):
        self.link = kwargs.get("link", "")
        self.source = kwargs.get("source", "")
        self.text = kwargs.get("text", TextClass())
        self.publishedOn = kwargs.get("publishedOn", datetime.datetime.now())
        self.imgPreview = kwargs.get("imgPreview", "")
