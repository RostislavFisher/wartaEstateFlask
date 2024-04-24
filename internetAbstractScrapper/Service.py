from abc import ABCMeta
from typing import List

# from internetAbstractScrapper.Publication import Publication
# from importLocalClass import importLocalClass
#
# Publication = importLocalClass(
#     r"C:\Users\Rostyslav\Desktop\wartaSoft\wartaEstateFlask\internetAbstractScrapper\Publication.py",
#     "Publication")

from internetAbstractScrapper.Publication import Publication
class Service(metaclass=ABCMeta):
    def __init__(self):
        self.ListOfPublications: List[Publication] = []  # Problem array

    # @abstractmethod
    def getListOfPublications(self, **kwargs) -> List[Publication]:
        """Returns list of publications. Each publication is a raw publication"""
        ...
