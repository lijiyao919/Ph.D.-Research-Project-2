from src.Dispatcher.ClusteringStrategy import ClusteringStrategy
import logging
from src.Configure.Config import *

class ClusteringInGroup(ClusteringStrategy):
    def __init__(self, rider_waiting_dict):
        super().__init__()
        self.logger.setLevel(logging.DEBUG)
        self.logger.info(ClusteringStrategy.timestamp, "__INIT__", None, None, "Create ClusteringInGroup Object")

        self.__assign_gid_dict = {}
        self.__rider_dict = rider_waiting_dict

        # Assign Group ID
        for zone_id in range(1, 78):
            self.__assign_gid_dict[zone_id] = {}
            for dir_id in range(0, 12):
                self.__assign_gid_dict[zone_id][dir_id] = 1

    def showAssignGidDict(self):
        ret = "{"
        for zone_id in self.__assign_gid_dict.keys():
            ret = ret + str(zone_id) + ": {"
            for dir_id in self.__assign_gid_dict[zone_id].keys():
                ret = ret + str(dir_id) + ": [" + str(self.__assign_gid_dict[zone_id][dir_id]) + "], "
            ret = ret + "}, \n"
        ret = ret + "}"
        return ret

    def getGroupID(self, zone_id, dir_id):
        return self.__assign_gid_dict[zone_id][dir_id]

    def cluster(self, rider):
        # Rider's zone ID and dir ID
        zone_id = rider.getSrcZone()
        dir_id = rider.getDirID()
        group_id = self.__assign_gid_dict[zone_id][dir_id]

        # self.__rider_waiting_dict[rider.getSrcZone()][rider.getDirID()] is defaultdict(dict)
        # group_num is the dict
        if rider.getID() not in self.__rider_dict[zone_id][dir_id][group_id].keys():
            self.__rider_dict[zone_id][dir_id][group_id][rider.getID()] = rider
            rider.setGroupID(group_id)
        else:
            self.logger.error(ClusteringInGroup.timestamp, "cluster", None, rider.getID(), "Rider has been in the Pool")

        # check how many riders in the zone&direction&group_num to determine group id
        rider_num = len(self.__rider_dict[zone_id][dir_id][group_id])
        # When the number of rider in group up to VEHICLE_CAPACITY
        if rider_num == VEHICLE_CAPACITY:
            self.__assign_gid_dict[zone_id][dir_id] += 1

