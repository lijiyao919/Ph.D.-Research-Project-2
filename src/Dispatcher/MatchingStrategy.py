from abc import ABC, abstractmethod
from src.Logger.Logger import Logger

class MatchingStrategy(ABC):

    timestamp = -1

    def __init__(self):
        self.logger = Logger('MatchingStrategy')

    @abstractmethod
    def match(self, rider_zone_id):
        pass