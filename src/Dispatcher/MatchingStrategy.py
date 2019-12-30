from abc import ABC, abstractmethod
from src.Logger.Logger import Logger
import datetime
import json

class MatchingStrategy(ABC):

    timestamp = -1
    time = datetime.datetime(2016, 4, 11, hour=11, minute=45)

    def __init__(self):
        self.logger = Logger('MatchingStrategy')
        with open('C:/Users/a02231961/PycharmProjects/Ph.D.-Research-Project-2/data/data.json') as json_file:
            self.__data = json.load(json_file)

    def getRatioOfSupplyDemand(self, zone_id):
        curr_state_t = MatchingStrategy.time.strftime('%m/%d/%Y %H:%M').split(' ')[1]
        return self.__data[curr_state_t][zone_id]

    @abstractmethod
    def match(self, rider_zone_id):
        pass