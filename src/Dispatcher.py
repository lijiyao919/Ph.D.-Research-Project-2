from collections import defaultdict
from src.Driver import Driver
from src.Rider import Rider
from src.Config import *
from src.Logger import Logger
from src.ClusteringInGroup import ClusteringInGroup
from src.MatchingInQueue import MatchingInQueue
from src.DriverStatusTracker import DriverStatusTracker
from src.RiderStatusTracker import RiderStatusTracker
import logging

class Dispatcher:
    # Sync timestamp for logging
    timestamp = -1

    def __init__(self):
        #logger in Dispatcher
        self.__logger = Logger('Dispatcher')
        self.__logger.setLevel(logging.DEBUG)
        self.__logger.info(Dispatcher.timestamp, "__INIT__", None, None, "Create A Dispatcher Object")

        #Storage for drivers and riders
        self.__driver_dict = {}
        self.__rider_wait_dict = {}
        self.__rider_serve_dict = {}
        self.__rider_finish_dict = {}
        self.__rider_cancel_dict = {}

        #Cluser Strategy
        self.__cluster_strategy = ClusteringInGroup(self.__rider_wait_dict)

        #Matching Strategy
        self.__match_strategy = MatchingInQueue(self.__driver_dict, self.__rider_wait_dict, self.__rider_serve_dict)

        #Driver Status Tracker
        self.__driver_tracker = DriverStatusTracker(self.__driver_dict)

        #Rider Status tracker
        self.__rider_tracker = RiderStatusTracker(self.__rider_wait_dict, self.__rider_serve_dict, self.__rider_finish_dict, self.__rider_cancel_dict)

        #Drivers' Performance
        self.__average_profit = 0.0
        self.__average_idle_time = 0.0

        #Riders' Performance
        self.__average_waiting_time = 0.0
        self.__average_travel_time = 0.0
        self.__average_fare = 0.0
        self.__average_sat = 0.0

        #Driver Dict
        for zone_id in range(1,78):
            self.__driver_dict[zone_id] = {}

        #Rider Dict
        for zone_id in range(1,78):
            self.__rider_wait_dict[zone_id] = {}
            for dir_id in range(0, 12):
                self.__rider_wait_dict[zone_id][dir_id] = defaultdict(dict)

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
        for zone_id in self.__rider_wait_dict.keys():
            ret = ret + str(zone_id) + ": {"
            for dir_id in self.__rider_wait_dict[zone_id].keys():
                ret = ret + str(dir_id) + ": {"
                for group_id in self.__rider_wait_dict[zone_id][dir_id].keys():
                    ret = ret + str(group_id) + ": ["
                    for rider_id in self.__rider_wait_dict[zone_id][dir_id][group_id].keys():
                        ret = ret + str(rider_id) + ", "
                    ret = ret[0:len(ret) - 2] + "], "
                ret = ret + "}, "
            ret = ret + "},\n"
        return ret

    def showRiderServedDict(self):
        ret = "Rider Served DICT: {rider_id}\n"
        ret = ret + "{"
        for rider_id in self.__rider_serve_dict.keys():
            ret=ret+str(rider_id)+", "
        ret=ret+"}\n"
        return ret

    def showRiderFinishedDict(self):
        ret = "Rider Finished DICT: {rider_id}\n"
        ret = ret + "{"
        for rider_id in self.__rider_finish_dict.keys():
            ret = ret + str(rider_id) + ", "
        ret = ret + "}\n"
        return ret

    def showRiderCanceledDict(self):
        ret = "Rider Canceled DICT: {rider_id}\n"
        ret = ret + "{"
        for rider_id in self.__rider_cancel_dict.keys():
            ret = ret + str(rider_id) + ", "
        ret = ret + "}\n"
        return ret

    def showDriverNumberOfEachZone(self):
        numZone = []
        for zone_id in self.__driver_dict.keys():
            total = len(self.__driver_dict[zone_id])
            numZone.append(total)
        return numZone

    def showRiderNumberOfEachZone(self):
        numZone = []
        for zone_id in self.__rider_wait_dict.keys():
            total_num = 0
            for dir_id in self.__rider_wait_dict[zone_id].keys():
                for group_id in self.__rider_wait_dict[zone_id][dir_id].keys():
                    total_num += len(self.__rider_wait_dict[zone_id][dir_id][group_id])
            numZone.append(total_num)
        return numZone

    #put driver into Driver Dict at start
    def handleDriverIntoDict(self, driver):
        if isinstance(driver, Driver):
            if driver.getID() not in self.__driver_dict[driver.getPos()].keys():
                self.__driver_dict[driver.getPos()][driver.getID()] = driver
            else:
                self.__logger.error(Dispatcher.timestamp, "handleDriverRequest", driver.getID(), None, "Driver has been in the Pool")
        else:
            self.__logger.error(Dispatcher.timestamp, "handleDriverRequest", None, None, "Driver's type is wrong.")

    def handleRiderIntoDict(self, rider):
        if isinstance(rider, Rider):
            self.__cluster_strategy.cluster(rider)
        else:
            self.__logger.error(Dispatcher.timestamp, "handleRiderRequest", None, None, "Rider's type is wrong.")

    def matchRidertoDriver(self):
        for zone_id in self.__rider_wait_dict.keys():
            for dir_id in self.__rider_wait_dict[zone_id].keys():
                for group_id in self.__rider_wait_dict[zone_id][dir_id].copy().keys():
                    driver = self.__match_strategy.match(zone_id)
                    if driver is not None:
                        self.__logger.info(Dispatcher.timestamp, "matchRidertoDriver", driver.getID(), None, "Driver be Chosen to Serve Riders.")
                        self.__logger.debug(Dispatcher.timestamp, "matchRidertoDriver", None, None, "Driver Zone ===> Rider Zone: ", str(driver.getPos()) + "===>" + str(zone_id))
                        driver.setRiders(self.__rider_wait_dict[zone_id][dir_id][group_id].copy)
                        self.__driver_tracker.updateDriverStatusAfterMatching(driver)
                        self.__logger.debug(Dispatcher.timestamp, "matchRidertoDriver", driver.getID(), None, str(driver))

                        for rider in self.__rider_wait_dict[zone_id][dir_id][group_id].values():
                            self.__rider_tracker.updateRiderStatusAfterMatching(rider, len(self.__rider_wait_dict[zone_id][dir_id][group_id]))
                            self.__logger.debug(Dispatcher.timestamp, "matchRidertoDriver", driver.getID(), rider.getID(), str(rider))
                        del self.__rider_wait_dict[zone_id][dir_id][group_id]
                    else:
                        self.__logger.info(Dispatcher.timestamp, "matchRidertoDriver", None, None, "No Driver is available.")
                        break


    def updateDriverInDriverDict(self):
        for zone_id in self.__driver_dict.keys():
            for driver in self.__driver_dict[zone_id].copy().values():
                if driver.getStatus() == IDLE:
                    self.__logger.info(Dispatcher.timestamp, "updateDriverStatus", driver.getID(), None, "Update Driver when IDLE.")
                    self.__driver_tracker.updateDriverStatusWhenIdle(driver)
                elif driver.getStatus() == INSERVICE:
                    self.__logger.info(Dispatcher.timestamp, "updateDriverStatus", driver.getID(), None, "Update Driver Who is INSERVICE.")
                    self.__driver_tracker.updateDriverStatusWhenInService(driver)
                    self.__logger.debug(Dispatcher.timestamp, "updateDriverStatus", driver.getID(), None, str(driver))
                else:
                    self.__logger.error(Dispatcher.timestamp, "updateDriverStatus", driver.getID(), None, "Driver Status is Wrong.")


    def updateRidersInWaitDict(self):
        for zone_id in self.__rider_wait_dict.keys():
            for dir_id in self.__rider_wait_dict[zone_id].keys():
                for group_id in self.__rider_wait_dict[zone_id][dir_id].keys():
                    for rider in self.__rider_wait_dict[zone_id][dir_id][group_id].values():
                        if rider.getStatus() == WAITING:
                            self.__rider_tracker.checkRiderStatusIfTimeOut(rider)
                            self.__rider_tracker.updateRiderStatusWhenWait(rider)


    def updateRidersInServeDict(self):
        for rider in self.__rider_serve_dict.values():
            self.__rider_tracker.updateRiderStatusWhenInService()


    def countTotalDriverNumber(self):
        total_len = 0
        for zone_id in self.__driver_dict.keys():
            total_len = total_len + len(self.__driver_dict[zone_id])
        return total_len

    def countRiderNumberInWaitDict(self):
        total_len = 0
        for zone_id in self.__rider_wait_dict.keys():
            for dir_id in self.__rider_wait_dict[zone_id].keys():
                for group_id in self.__rider_wait_dict[zone_id][dir_id].keys():
                    total_len = total_len + len(self.__rider_wait_dict[zone_id][dir_id][group_id])
        return total_len

    def countRiderNumberInServeDict(self):
        return len(self.__rider_serve_dict)

    def countRiderNumberInFinishDict(self):
        return len(self.__rider_finish_dict)

    def countRiderNumberInCancelDict(self):
        return len(self.__rider_cancel_dict)

    def countCurrentTotalRiderNumber(self):
        return self.countRiderNumberInWaitDict() + self.countRiderNumberInServeDict() + self.countRiderNumberInFinishDict() + self.countRiderNumberInCancelDict()

    def calcAverageProfitOfDrivers(self):
        totalProfit = 0
        for zone_id in self.__driver_dict.keys():
            for driver in self.__driver_dict[zone_id].values():
                totalProfit += driver.getProfit()
        return totalProfit / self.countTotalDriverNumber()

    def calcAverageIdleTimeOfDrivers(self):
        totalIdleTime = 0
        for zone_id in self.__driver_dict.keys():
            for driver in self.__driver_dict[zone_id].values():
                totalIdleTime += driver.getIdleTime()
        return totalIdleTime / self.countTotalDriverNumber()

    def calcAverageWaitTimeOfRiders(self):
        totalWaitTime = 0
        for rider in self.__rider_finish_dict.values():
            totalWaitTime +=rider.getWaitTime()
        return totalWaitTime/self.countRiderNumberInFinishDict()

    def calcAverageDetourTimeOfRiders(self):
        totalDetourTime = 0
        for rider in self.__rider_finish_dict.values():
            totalDetourTime += rider.getDetourTime()
        return totalDetourTime/self.countRiderNumberInFinishDict()

    def calcAverageFareOfRiders(self):
        totalFare = 0
        for rider in self.__rider_finish_dict.values():
            totalFare += rider.getPrice()
        return totalFare/self.countRiderNumberInFinishDict()

    def calcAverageDefaultFareRiders(self):
        totalDefaultFare = 0
        for rider in self.__rider_finish_dict.values():
            totalDefaultFare += rider.getDefaultPrice()
        return totalDefaultFare/self.countRiderNumberInFinishDict()

    def calcAverageSatOfRiders(self):
        totalSat = 0
        for rider in self.__rider_finish_dict.values():
            totalSat += rider.getSat()
        return totalSat/self.countRiderNumberInFinishDict()





















