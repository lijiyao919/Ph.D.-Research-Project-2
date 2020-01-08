from src.Dispatcher.ClusteringStrategy import ClusteringStrategy
import logging
from src.Configure.Config import *

class ClusteringByDir(ClusteringStrategy):
    def __init__(self, rider_waiting_dict):
        super().__init__(rider_waiting_dict)
        #self.logger.setLevel(logging.DEBUG)
        self.logger.info(ClusteringStrategy.timestamp, "__INIT__", None, None, "Create ClusteringInGroup Object")

    def cluster(self, rider):
        self.groupRiderByDir(rider, VEHICLE_CAPACITY)



