from abc import ABC, abstractmethod
from src.Logger.Logger import Logger

class RoutingStrategy(ABC):

    timestamp = -1

    def __init__(self, riders, route):
        self.logger = Logger('RoutingStrategy')
        self.riders = riders
        self.route = route

    @abstractmethod
    def planRoute(self):
        pass