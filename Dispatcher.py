from collections import defaultdict
from Driver import Driver
from Rider import Rider
from Config import *
from Graph import Graph
from Data.Map import AdjList_Chicago

class Dispatcher:
    # Sync timestamp for logging
    timestamp = -1

    def __init__(self):
        self.__driver_dict = {}
        self.__rider_waiting_dict = {}
        self.__rider_serving_dict = {}
        self.__rider_finished_dict = {}
        self.__rider_canceled_dict = {}
        self.__assign_gid_dict = {}

        #Driver Dict
        for zone_id in range(1,78):
            self.__driver_dict[zone_id] = {}

        #Rider Dict
        for zone_id in range(1,78):
            self.__rider_waiting_dict[zone_id] = {}
            for dir_id in range(0, 12):
                self.__rider_waiting_dict[zone_id][dir_id] = defaultdict(dict)

        #Assign Group ID
        for zone_id in range(1, 78):
            self.__assign_gid_dict[zone_id] = {}
            for dir_id in range(0, 12):
                self.__assign_gid_dict[zone_id][dir_id] = 1

    def showDriverDict(self):
        ret = "Driver DICT: zone_id:{rider_id}\n"
        for zone_id in self.__driver_dict.keys():
            ret = ret + str(zone_id) + ": {"
            for driver_id in self.__driver_dict[zone_id].keys():
                ret = ret + str(driver_id) + ", "
            ret = ret + "},\n"
        return ret

    def showRiderWaitDict(self):
        ret = "Rider Wait DICT: zone_id:{dir_id:{group_id:{rider_id}}}\n"
        for zone_id in self.__rider_waiting_dict.keys():
            ret = ret + str(zone_id) + ": {"
            for dir_id in self.__rider_waiting_dict[zone_id].keys():
                ret = ret + str(dir_id) + ": {"
                for group_id in self.__rider_waiting_dict[zone_id][dir_id].keys():
                    ret = ret + str(group_id) + ": ["
                    for rider_id in self.__rider_waiting_dict[zone_id][dir_id][group_id].keys():
                        ret = ret + str(rider_id) + ", "
                    ret = ret[0:len(ret) - 2] + "], "
                ret = ret + "}, "
            ret = ret + "},\n"
        return ret

    def showRiderServedDict(self):
        ret = "Rider Served DICT: {rider_id}\n"
        ret = ret + "{"
        for rider_id in self.__rider_serving_dict.keys():
            ret=ret+str(rider_id)+", "
        ret=ret+"}\n"
        return ret

    def showRiderFinishedDict(self):
        ret = "Rider Finished DICT: {rider_id}\n"
        ret = ret + "{"
        for rider_id in self.__rider_finished_dict.keys():
            ret = ret + str(rider_id) + ", "
        ret = ret + "}\n"
        return ret

    def showRiderCanceledDict(self):
        ret = "Rider Canceled DICT: {rider_id}\n"
        ret = ret + "{"
        for rider_id in self.__rider_canceled_dict.keys():
            ret = ret + str(rider_id) + ", "
        ret = ret + "}\n"
        return ret

    def showAssignGidDict(self):
        ret = "GID DICT: zone_id:{dir_id: #GID}\n"
        for zone_id in self.__assign_gid_dict.keys():
            ret = ret + str(zone_id) + ": {"
            for dir_id in self.__assign_gid_dict[zone_id].keys():
                ret = ret + str(dir_id) + ": [" + str(self.__assign_gid_dict[zone_id][dir_id]) + "], "
            ret = ret + "}, \n"
        return ret

    #put driver into Driver Dict at start
    def handleDriverRequest(self, driver):
        if isinstance(driver, Driver):
            if driver.getID() not in self.__driver_dict[driver.getPos()].keys():
                self.__driver_dict[driver.getPos()][driver.getID()] = driver
            else:
                pass
                #log error
        else:
            pass
            #log error

    def handleRiderRequest(self, rider):
        if isinstance(rider, Rider):
            #Rider's zone ID and dir ID
            zone_id = rider.getSrcZone()
            dir_id = rider.getDirID()
            group_id = self.__assign_gid_dict[zone_id][dir_id]

            #self.__rider_waiting_dict[rider.getSrcZone()][rider.getDirID()] is defaultdict(dict)
            #group_num is the dict
            if rider.getID() not in self.__rider_waiting_dict[zone_id][dir_id][group_id]:
                self.__rider_waiting_dict[zone_id][dir_id][group_id][rider.getID()] = rider
            else:
                pass
                #log error

            # check how many riders in the zone&direction&group_num to determine group id
            rider_num = len(self.__rider_waiting_dict[zone_id][dir_id][group_id])
            #When the number of rider in group up to VEHICLE_CAPACITY
            if rider_num == VEHICLE_CAPACITY:
                self.__assign_gid_dict[zone_id][dir_id] += 1
        else:
            pass
            #log error

    def checkRiderPatience(self):
        cancel_id = []
        for zone_id in self.__rider_waiting_dict.keys():
            for dir in self.__rider_waiting_dict[zone_id].keys():
                for group_id in self.__rider_waiting_dict[zone_id][dir].keys():
                    for rider in self.__rider_waiting_dict[zone_id][dir][group_id].values():
                        if rider.getStatus() == WAITING:
                            if Dispatcher.timestamp - rider.getStartTime() >= rider.getPatience():
                                rider.setStatus(CANCEL)
                                self.__rider_canceled_dict[rider.getID()] = rider
                                cancel_id.append(rider.getID())
                            else:
                                pass
                                #log debug
                        else:
                            pass
                            #log error

                    #Remove rider from waiting dict
                    for id in cancel_id:
                        if id in self.__rider_waiting_dict[zone_id][dir][group_id].keys():
                            del self.__rider_waiting_dict[zone_id][dir][group_id][id]
                        else:
                            pass
                            #log error

    def matchRidertoDriver(self):
        for zone_id in self.__rider_waiting_dict.keys():
            for dir_id in self.__rider_waiting_dict[zone_id].keys():
                if len(self.__rider_waiting_dict[zone_id][dir_id]) != 0:
                    group_id_delete_list = []
                    for group_id in self.__rider_waiting_dict[zone_id][dir_id].keys():
                        driver_zone, driver_number = self.__selectDriverZoneWithLen(zone_id)
                        if driver_zone is not None:
                            for driver_id in self.__driver_dict[driver_zone].keys():
                                if self.__driver_dict[driver_zone][driver_id].getStatus() == IDLE:
                                    route, total_effort = self.planRoute(self.__rider_waiting_dict[zone_id][dir_id][group_id], self.__driver_dict[driver_zone][driver_id])
                                    self.__driver_dict[driver_zone][driver_id].setStatus(INSERVICE)
                                    self.__driver_dict[driver_zone][driver_id].setAcceptTime(Dispatcher.timestamp)
                                    self.__driver_dict[driver_zone][driver_id].setRoute(route)
                                    self.__driver_dict[driver_zone][driver_id].setTripEffort(total_effort)
                                    self.__driver_dict[driver_zone][driver_id].calcProfit()
                                    break
                            for rider_id in self.__rider_waiting_dict[zone_id][dir_id][group_id].keys():
                                self.__rider_waiting_dict[zone_id][dir_id][group_id][rider_id].calcPrice(len(self.__rider_waiting_dict[zone_id][dir_id][group_id]))
                                self.__rider_waiting_dict[zone_id][dir_id][group_id][rider_id].calcSat()
                                self.__rider_waiting_dict[zone_id][dir_id][group_id][rider_id].setStatus(SERVING)
                                self.__rider_serving_dict[rider_id] = self.__rider_waiting_dict[zone_id][dir_id][group_id][rider_id]
                            group_id_delete_list.append(group_id)
                    for group_id in group_id_delete_list:
                        del self.__rider_waiting_dict[zone_id][dir_id][group_id]


    def __selectDriverZoneWithLen(self, zone_id):
        zones = AdjList_Chicago[zone_id].copy()
        zones.append(zone_id)
        zone_selected = None
        max=0
        #print(zones)
        #select zone
        for zone in zones:
            if len(self.__driver_dict[zone]) > max:
                zone_selected = zone
                max = len(self.__driver_dict[zone])

        return zone_selected, max


    def planRoute(self, riders, driver):
        route_tuple =sorted(riders.items(), key=lambda x: x[1].getShortestTime())
        src = route_tuple[0][1].getSrcZone()
        total_effort = Graph.queryTravelCost(driver.getPos(), src)
        for rider_id, rider in route_tuple:
            total_effort = total_effort + Graph.queryTravelCost(src, rider.getDestZone())
            rider.setTravelTime(total_effort)
            src = rider.getDestZone()
        #print(route_tuple)
        return route_tuple, total_effort

    def updateDriverStatus(self):
        for zone_id in self.__driver_dict.keys():
            for driver in self.__driver_dict[zone_id].values():
                if driver.getStatus() == INSERVICE:
                    start_trip_time = driver.getAcceptTime()
                    next_dest_time=(driver.getRoute())[0][1].getTravelTime()
                    if start_trip_time + next_dest_time <= Dispatcher.timestamp:
                        rider = driver.popRoute()
                        driver.setPos(rider[1].getDestZone())
                        self.__rider_finished_dict[rider[0]]=rider[1]
                        del self.__rider_serving_dict[rider[0]]
                elif driver.getStatus() == IDLE:
                    driver.tickIdleTime()
                else:
                    pass
                    #log error

    def updateRiderStatus(self):
        for zone_id in self.__rider_waiting_dict.keys():
            for dir_id in self.__rider_waiting_dict[zone_id].keys():
                for group_id in self.__rider_waiting_dict[zone_id][dir_id].keys():
                    for rider_id in self.__rider_waiting_dict[zone_id][dir_id][group_id].keys():
                        if self.__rider_waiting_dict[zone_id][dir_id][group_id][rider_id].getStatus() == WAITING:
                            self.__rider_waiting_dict[zone_id][dir_id][group_id][rider_id].tickWaitTime()















