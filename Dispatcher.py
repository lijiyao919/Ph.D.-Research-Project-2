from collections import defaultdict
from Driver import Driver
from Rider import Rider
from Config import *
from Graph import Graph
from Map import AdjList_Chicago
from Logger import Logger
import logging

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

        #Drivers' Performance
        self.__average_profit = 0.0
        self.__average_idle_time = 0.0

        #Riders' Performance
        self.__average_waiting_time = 0.0
        self.__average_travel_time = 0.0
        self.__average_fare = 0.0
        self.__average_sat = 0.0

        self.logger = Logger('Dispatcher')
        self.logger.setLevel(logging.DEBUG)
        self.logger.info(Dispatcher.timestamp, "__INIT__", None, None, "Create Dispatcher Object")

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
                self.logger.error(Dispatcher.timestamp, "handleDriverRequest", driver.getID(), None, "Driver has been in the Pool")
        else:
            self.logger.error(Dispatcher.timestamp, "handleDriverRequest", None, None, "Driver's type is wrong.")

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
                self.logger.error(Dispatcher.timestamp, "handleRiderRequest", None, rider.getID(), "Rider has been in the Pool" )

            # check how many riders in the zone&direction&group_num to determine group id
            rider_num = len(self.__rider_waiting_dict[zone_id][dir_id][group_id])
            #When the number of rider in group up to VEHICLE_CAPACITY
            if rider_num == VEHICLE_CAPACITY:
                self.__assign_gid_dict[zone_id][dir_id] += 1
        else:
            self.logger.error(Dispatcher.timestamp, "handleRiderRequest", None, None, "Rider's type is wrong.")

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
                                self.logger.debug(Dispatcher.timestamp, "checkRiderPatience", None, rider.getID(), "Cancel Time Should be: ", str(rider.getStartTime()+rider.getPatience()))
                        else:
                            self.logger.error(Dispatcher.timestamp, "checkRiderPatience", None, rider.getID(), "Rider not in the waiting list")

                    #Remove rider from waiting dict
                    for id in cancel_id:
                        if id in self.__rider_waiting_dict[zone_id][dir][group_id].keys():
                            del self.__rider_waiting_dict[zone_id][dir][group_id][id]
                        else:
                            self.logger.error(Dispatcher.timestamp, "checkRiderPatience", None, id, "Fail to remove rider from waiting list")

    def matchRidertoDriver(self):
        for zone_id in self.__rider_waiting_dict.keys():
            for dir_id in self.__rider_waiting_dict[zone_id].keys():
                if len(self.__rider_waiting_dict[zone_id][dir_id]) != 0:
                    group_id_delete_list = []
                    for group_id in self.__rider_waiting_dict[zone_id][dir_id].keys():
                        driver_zone, driver_number = self.__selectDriverZoneWithLen(zone_id)
                        if driver_zone is not None:
                            for driver_id in self.__driver_dict[driver_zone].keys():
                                driver = self.__driver_dict[driver_zone][driver_id]
                                if driver.getStatus() == IDLE:
                                    self.logger.info(Dispatcher.timestamp, "matchRidertoDriver", driver.getID(), None, "Driver be Chosen to Serve Riders.")
                                    route, total_effort = self.planRoute(self.__rider_waiting_dict[zone_id][dir_id][group_id], driver)
                                    driver.setStatus(INSERVICE)
                                    driver.setAcceptTime(Dispatcher.timestamp)
                                    driver.setRoute(route)
                                    driver.setTripEffort(total_effort)
                                    driver.calcProfit()
                                    self.logger.debug(Dispatcher.timestamp, "matchRidertoDriver", driver.getID(), None, str(driver))
                                    break
                            for rider_id in self.__rider_waiting_dict[zone_id][dir_id][group_id].keys():
                                rider = self.__rider_waiting_dict[zone_id][dir_id][group_id][rider_id]
                                rider.calcPrice(len(self.__rider_waiting_dict[zone_id][dir_id][group_id]))
                                rider.calcSat()
                                rider.setStatus(SERVING)
                                self.__rider_serving_dict[rider_id] = rider
                                self.logger.info(Dispatcher.timestamp, "matchRidertoDriver", driver.getID(), rider.getID(), str(rider))
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
                    self.logger.info(Dispatcher.timestamp, "updateDriverStatus", driver.getID(), None, "Update Driver Who is INSERVICE.")
                    self.logger.debug(Dispatcher.timestamp, "updateDriverStatus", driver.getID(), None, str(driver))
                    start_trip_time = driver.getAcceptTime()
                    next_dest_time=(driver.getRoute())[0][1].getTravelTime()
                    if start_trip_time + next_dest_time <= Dispatcher.timestamp:
                        rider = driver.popRoute()
                        driver.setPos(rider[1].getDestZone())
                        self.__rider_finished_dict[rider[0]]=rider[1]
                        del self.__rider_serving_dict[rider[0]]
                        rider[1].setStatus(FINISHED)
                        self.logger.info(Dispatcher.timestamp, "updateDriverStatus", driver.getID(), rider[1].getID(), "Dropoff One Rider.")
                    if len(driver.getRoute()) == 0:
                        driver.setStatus(IDLE)
                        self.logger.info(Dispatcher.timestamp, "updateDriverStatus", driver.getID(), None, "Finish One Trip.")
                    self.logger.debug(Dispatcher.timestamp, "updateDriverStatus", driver.getID(), None, str(driver))
                elif driver.getStatus() == IDLE:
                    self.logger.info(Dispatcher.timestamp, "updateDriverStatus", driver.getID(), None, "Update Driver Who is IDLE.")
                    driver.tickIdleTime()
                else:
                    self.logger.error(Dispatcher.timestamp, "updateDriverStatus", driver.getID(), None, "Driver Status is Wrong.")


    def updateRiderStatus(self):
        for zone_id in self.__rider_waiting_dict.keys():
            for dir_id in self.__rider_waiting_dict[zone_id].keys():
                for group_id in self.__rider_waiting_dict[zone_id][dir_id].keys():
                    for rider_id in self.__rider_waiting_dict[zone_id][dir_id][group_id].keys():
                        if self.__rider_waiting_dict[zone_id][dir_id][group_id][rider_id].getStatus() == WAITING:
                            self.__rider_waiting_dict[zone_id][dir_id][group_id][rider_id].tickWaitTime()

    def getDriverDictLen(self):
        total_len = 0
        for zone_id in self.__driver_dict.keys():
            total_len = total_len + len(self.__driver_dict[zone_id])
        return total_len

    def getRiderWaitDictLen(self):
        total_len = 0
        for zone_id in self.__rider_waiting_dict.keys():
            for dir_id in self.__rider_waiting_dict[zone_id].keys():
                for group_id in self.__rider_waiting_dict[zone_id][dir_id].keys():
                    total_len = total_len + len(self.__rider_waiting_dict[zone_id][dir_id][group_id])
        return total_len

    def getRiderServeDictLen(self):
        return len(self.__rider_serving_dict)

    def getRiderFinishDictLen(self):
        return len(self.__rider_finished_dict)

    def getRiderCancelDictLen(self):
        return len(self.__rider_canceled_dict)

    def getCurrentTotalNumberOfRider(self):
        return self.getRiderWaitDictLen()+self.getRiderServeDictLen()+self.getRiderFinishDictLen()+self.getRiderCancelDictLen()

    def calcAverageProfitOfDrivers(self):
        totalProfit = 0
        for zone_id in self.__driver_dict.keys():
            for driver in self.__driver_dict[zone_id].values():
                totalProfit += driver.getProfit()
        return totalProfit / self.getDriverDictLen()

    def calcAverageIdleTimeOfDrivers(self):
        totalIdleTime = 0
        for zone_id in self.__driver_dict.keys():
            for driver in self.__driver_dict[zone_id].values():
                totalIdleTime += driver.getIdleTime()
        return totalIdleTime / self.getDriverDictLen()

    def calcAverageWaitTimeOfRiders(self):
        totalWaitTime = 0
        for rider in self.__rider_finished_dict.values():
            totalWaitTime +=rider.getWaitTime()
        return totalWaitTime/self.getRiderFinishDictLen()

    def calcAverageDetourTimeOfRiders(self):
        totalDetourTime = 0
        for rider in self.__rider_finished_dict.values():
            totalDetourTime += rider.getDetourTime()
        return totalDetourTime/self.getRiderFinishDictLen()

    def calcAverageFareOfRiders(self):
        totalFare = 0
        for rider in self.__rider_finished_dict.values():
            totalFare += rider.getPrice()
        return totalFare/self.getRiderFinishDictLen()

    def calcAverageDefaultFareRiders(self):
        totalDefaultFare = 0
        for rider in self.__rider_finished_dict.values():
            totalDefaultFare += rider.getDefaultPrice()
        return totalDefaultFare/self.getRiderFinishDictLen()

    def calcAverageSatOfRiders(self):
        totalSat = 0
        for rider in self.__rider_finished_dict.values():
            totalSat += rider.getSat()
        return totalSat/self.getRiderFinishDictLen()

















