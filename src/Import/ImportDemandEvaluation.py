import datetime
import json
from src.Configure.Config import *

class ImportDemandEvaluation:
    timestamp = -1
    __instance = None

    def __init__(self):
        """ Virtually private constructor. """
        if ImportDemandEvaluation.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            ImportDemandEvaluation.__instance = self
            with open(POPULARITY_SCORE_FILE) as json_file:
                self.__data = json.load(json_file)

    @staticmethod
    def getInstance():
        """ Static access method. """
        if ImportDemandEvaluation.__instance == None:
            ImportDemandEvaluation()
        return ImportDemandEvaluation.__instance



    def getRatioOfSupplyDemand(self, zone_id):
        curr_state_t = ImportDemandEvaluation.timestamp
        if curr_state_t <= 479:
            return self.__data[str(curr_state_t)][zone_id]
        else:
            return 0
