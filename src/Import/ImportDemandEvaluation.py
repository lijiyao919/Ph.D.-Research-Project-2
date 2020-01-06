import datetime
import json

class ImportDemandEvaluation:
    time = datetime.datetime(2016, 4, 11, hour=10, minute=45)
    __instance = None

    def __init__(self):
        """ Virtually private constructor. """
        if ImportDemandEvaluation.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            ImportDemandEvaluation.__instance = self
            with open('C:/Users/a02231961/PycharmProjects/Ph.D.-Research-Project-2/data/data.json') as json_file:
                self.__data = json.load(json_file)

    @staticmethod
    def getInstance():
        """ Static access method. """
        if ImportDemandEvaluation.__instance == None:
            ImportDemandEvaluation()
        return ImportDemandEvaluation.__instance



    def getRatioOfSupplyDemand(self, zone_id):
        curr_state_t = ImportDemandEvaluation.time.strftime('%m/%d/%Y %H:%M').split(' ')[1]
        return self.__data[curr_state_t][zone_id]
