from collections import OrderedDict
from src.Graph.Map import AdjList_Chicago
from src.Dispatcher.MatchingStrategy import MatchingStrategy
from src.Configure.Config import *
import logging

class MatchingInQueue(MatchingStrategy):
    def __init__(self, driver_dict, rider_wait_dict, rider_serve_dict):
        super().__init__()
        #self.logger.setLevel(logging.DEBUG)
        self.logger.info(MatchingStrategy.timestamp, "__INIT__", None, None, "Create MatchingInQueue Object")

        self.__driver_dict = driver_dict
        self.__rider_wait_dict = rider_wait_dict
        self.__rider_serve_dict = rider_serve_dict

    def match(self, rider_zone_id):
        zones = AdjList_Chicago[rider_zone_id].copy()
        zones.append(rider_zone_id)
        zone_selected = None
        max = 0

        for zone in zones:
            supply_demand_ratio = self.__countIdleDriversWithinAZone(zone)/(1+self.getRatioOfSupplyDemand(zone))
            if supply_demand_ratio > max:
                zone_selected = zone
                max = supply_demand_ratio
            elif supply_demand_ratio == max and max != 0:
                if zone < zone_selected:
                    zone_selected = zone

        if zone_selected is not None:
            for driver in OrderedDict(sorted(self.__driver_dict[zone_selected].items(), key=lambda t: t[0])).values():
                if driver.getStatus() == IDLE:
                    return driver
        return None



    def __countIdleDriversWithinAZone(self, zone_id):
        total = 0
        for driver in self.__driver_dict[zone_id].values():
            if driver.getStatus() == IDLE:
                total += 1
        return total




