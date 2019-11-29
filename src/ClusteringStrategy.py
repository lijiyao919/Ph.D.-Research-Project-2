from abc import ABC, abstractmethod
from src.Logger import Logger

class ClusteringStrategy(ABC):

    timestamp = -1

    def __init__(self):
        self.logger = Logger('ClusteringStrategy')

    @abstractmethod
    def cluster(self, rider):
        pass