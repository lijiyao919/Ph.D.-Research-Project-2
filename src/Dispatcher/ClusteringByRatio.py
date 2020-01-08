from src.Dispatcher.ClusteringStrategy import ClusteringStrategy
from src.Import.ImportDemandEvaluation import ImportDemandEvaluation
from src.Configure.Config import *
import logging

class ClusteringByRatio(ClusteringStrategy):
    def __init__(self, rider_waiting_dict, driver_dict):
        super().__init__(rider_waiting_dict)
        #self.logger.setLevel(logging.DEBUG)
        self.logger.info(ClusteringStrategy.timestamp, "__INIT__", None, None, "Create ClusteringByRatio Object")

        self.__demand_evaluation = ImportDemandEvaluation.getInstance()
        self.__driver_dict = driver_dict

    def cluster(self, rider):
        zone_id = rider.getDestZone()
        demand = self.__demand_evaluation.getRatioOfSupplyDemand(zone_id)
        supply = len(self.__driver_dict[zone_id])
        ratio =None

        if demand !=0:
            ratio = supply/demand

        if ratio != None and ratio < 1:
            rider.setDirID(-1)
            self.groupRiderByDir(rider, 1)
        else:
            self.groupRiderByDir(rider, VEHICLE_CAPACITY)



