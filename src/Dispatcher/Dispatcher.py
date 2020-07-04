from collections import defaultdict, OrderedDict
from src.Driver.Driver import Driver
from src.Rider.Rider import Rider
from src.Configure.Config import *
from src.Logger.Logger import Logger
from src.Dispatcher.ClusteringByDir import ClusteringByDir
from src.Dispatcher.MatchingInQueue import MatchingInQueue
from src.Dispatcher.DriverStatusTracker import DriverStatusTracker
from src.Dispatcher.RiderStatusTracker import RiderStatusTracker
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

        #Performance of driver and rider
        self.wait_rider={}
        self.no_work_driver={}
        self.idle_driver_before_match={}

        self.grp_in_4=0
        self.grp_in_3=0
        self.grp_in_2=0
        self.grp_in_1=0

        #Learning reward
        self.driver_num_serve = 0
        self.driver_num_move = 0

        #Cluser Strategy
        self.__cluster_strategy = ClusteringByDir(self.__rider_wait_dict)

        #Matching Strategy
        self.__match_strategy = MatchingInQueue(self.__driver_dict, self.__rider_wait_dict, self.__rider_serve_dict)

        #Driver Status Tracker
        self.__driver_tracker = DriverStatusTracker(self.__driver_dict)

        #Rider Status tracker
        self.__rider_tracker = RiderStatusTracker(self.__rider_wait_dict, self.__rider_serve_dict, self.__rider_finish_dict, self.__rider_cancel_dict)

        #Driver Dict
        for zone_id in range(1,78):
            self.__driver_dict[zone_id] = {}

        #Rider Dict
        for zone_id in range(1,78):
            self.__rider_wait_dict[zone_id] = {}
            for dir_id in range(-1, 360//DIR_THRESHOLD):
                self.__rider_wait_dict[zone_id][dir_id] = defaultdict(dict)

        #
        for cycle in range(SIMULATION_CYCLE_START, SIMULATION_CYCLE_END):
            self.wait_rider[cycle] = []
            self.no_work_driver[cycle] = []
            for zone_id in range(0,78):
                self.wait_rider[cycle].append(0)
                self.no_work_driver[cycle].append(0)

    def showDriverDict(self, zone_id):
        ret = str(zone_id) + ": {"
        for driver_id in OrderedDict(sorted(self.__driver_dict[zone_id].items(), key=lambda t: t[0])).keys():
            ret = ret + driver_id + ", "
        ret = ret + "}"
        return ret

    def getDriverFromDriverDict(self, zone_id, driver_id):
        for id, driver in self.__driver_dict[zone_id].items():
            if id == driver_id:
                return driver
        return None

    def getDriverNumberOfZone(self, zone_id):
        return len(self.__driver_dict[zone_id])


    def showRiderWaitDict(self, zone_id):
        ret = str(zone_id) + ": {"
        for dir_id in self.__rider_wait_dict[zone_id].keys():
            ret = ret + str(dir_id) + ": {"
            for group_id in self.__rider_wait_dict[zone_id][dir_id].keys():
                ret = ret + str(group_id) + ": ["
                for rider_id in OrderedDict(sorted(self.__rider_wait_dict[zone_id][dir_id][group_id].items(), key=lambda t: t[0])).keys():
                    ret = ret + str(rider_id) + ", "
                ret = ret + "], "
            ret = ret + "}, "
        ret = ret + "}"
        return ret

    def getRiderFromWaitDict(self, zone_id, dir_id, group_id, rider_id):
        for id, rider in self.__rider_wait_dict[zone_id][dir_id][group_id].items():
            if id == rider_id:
                return rider
        return None

    def getGroupFromWaitDict(self, zone_id, dir_id, group_id):
        for id, group in self.__rider_wait_dict[zone_id][dir_id].items():
            if id == group_id:
                return group
        return None

    def getRequestNumberOfZone(self, zone_id):
        total_num = 0
        for dir_id in self.__rider_wait_dict[zone_id].keys():
            for group_id in self.__rider_wait_dict[zone_id][dir_id].keys():
                total_num += len(self.__rider_wait_dict[zone_id][dir_id][group_id])
        return total_num


    def showRiderServedDict(self):
        ret = "{"
        for rider_id in OrderedDict(sorted(self.__rider_serve_dict.items(), key=lambda t: t[0])).keys():
            ret=ret+str(rider_id)+", "
        ret=ret+"}"
        return ret

    def getRiderFromServedDict(self, rider_id):
        for id, rider in self.__rider_serve_dict.items():
            if id == rider_id:
                return rider
        return None

    def showRiderFinishedDict(self):
        ret = "{"
        for rider_id in OrderedDict(sorted(self.__rider_finish_dict.items(), key=lambda t: t[0])).keys():
            ret = ret + str(rider_id) + ", "
        ret = ret + "}"
        return ret

    def getRiderFromFinishedDict(self, rider_id):
        for id, rider in self.__rider_finish_dict.items():
            if id == rider_id:
                return rider
        return None

    def showRiderCanceledDict(self):
        ret = "{"
        for rider_id in OrderedDict(sorted(self.__rider_cancel_dict.items(), key=lambda t: t[0])).keys():
            ret = ret + str(rider_id) + ", "
        ret = ret + "}"
        return ret

    def getRiderFromCanceledDict(self, rider_id):
        for id, rider in self.__rider_cancel_dict.items():
            if id == rider_id:
                return rider
        return None

    #put driver into Driver Dict at start
    def handleDriverIntoDict(self, driver):
        if isinstance(driver, Driver):
            if driver.getID() not in self.__driver_dict[driver.getPos()].keys():
                self.__driver_dict[driver.getPos()][driver.getID()] = driver
            else:
                self.__logger.error(Dispatcher.timestamp, "handleDriverRequest", driver.getID(), None, "Driver has been in the Pool.")
                raise Exception("Driver has been in the Pool.")
        else:
            self.__logger.error(Dispatcher.timestamp, "handleDriverRequest", None, None, "Driver's type is wrong.")
            raise Exception("Driver's type is wrong.")

    def handleRiderIntoDict(self, rider):
        if isinstance(rider, Rider):
            self.__cluster_strategy.cluster(rider)
        else:
            self.__logger.error(Dispatcher.timestamp, "handleRiderRequest", None, None, "Rider's type is wrong.")
            raise Exception("Rider's type is wrong.")

    def matchRidertoDriver(self):
        self.driver_num_serve = 0
        for zone_id in self.__rider_wait_dict.keys():
            for dir_id in self.__rider_wait_dict[zone_id].keys():
                for group_id in self.__rider_wait_dict[zone_id][dir_id].copy().keys():
                    driver = self.__match_strategy.match(zone_id)
                    if driver is not None:
                        self.driver_num_serve += 1
                        self.__logger.info(Dispatcher.timestamp, "matchRidertoDriver", driver.getID(), None, "Driver be Chosen to Serve Riders.")
                        self.__logger.debug(Dispatcher.timestamp, "matchRidertoDriver", None, None, "Driver Zone ===> Rider Zone: ", str(driver.getPos()) + "===>" + str(zone_id))
                        # update driver status
                        driver.setRiders(self.__rider_wait_dict[zone_id][dir_id][group_id])
                        self.__driver_tracker.updateDriverStatusAfterMatching(driver)
                        self.__logger.debug(Dispatcher.timestamp, "matchRidertoDriver", driver.getID(), None, str(driver))

                        #update rider status
                        if len(self.__rider_wait_dict[zone_id][dir_id][group_id]) == 4:
                            self.grp_in_4 += 1
                        elif len(self.__rider_wait_dict[zone_id][dir_id][group_id]) == 3:
                            self.grp_in_3 += 1
                        elif len(self.__rider_wait_dict[zone_id][dir_id][group_id]) == 2:
                            self.grp_in_2 += 1
                        elif len(self.__rider_wait_dict[zone_id][dir_id][group_id]) == 1:
                            self.grp_in_1 += 1
                        else:
                            self.__logger.warning(Dispatcher.timestamp, "calcPoolingPerformanceInWaitDict", None, None, "Grp len is 0.")

                        for rider in self.__rider_wait_dict[zone_id][dir_id][group_id].values():
                            self.__rider_tracker.updateRiderStatusAfterMatching(rider)
                            self.__logger.debug(Dispatcher.timestamp, "matchRidertoDriver", driver.getID(), rider.getID(), str(rider))
                        del self.__rider_wait_dict[zone_id][dir_id][group_id]
                    else:
                        self.__logger.info(Dispatcher.timestamp, "matchRidertoDriver", None, None, "No Driver is available.")
                        break


    def updateDriverInDict(self):
        #print("32: " + str(self.__driver_tracker.getSmoothRatio(32)))
        #print("33: " + str(self.__driver_tracker.getSmoothRatio(33)))
        #print("35: " + str(self.__driver_tracker.getSmoothRatio(35)))
        #print("36: " + str(self.__driver_tracker.getSmoothRatio(36)))
        #print("39: " + str(self.__driver_tracker.getSmoothRatio(39)))
        #print("41: " + str(self.__driver_tracker.getSmoothRatio(41)))
        self.driver_num_move = 0
        for zone_id in self.__driver_dict.keys():
            for driver in self.__driver_dict[zone_id].copy().values():
                if driver.getStatus() == IDLE:
                    self.__logger.info(Dispatcher.timestamp, "updateDriverStatus", driver.getID(), None, "Update Driver when IDLE.")
                    preEffort = driver.getTripEffort()
                    self.__driver_tracker.updateDriverStatusWhenIdle(driver, self.no_work_driver)
                    if driver.getTripEffort() > preEffort:
                        self.driver_num_move += 1
                elif driver.getStatus() == INSERVICE:
                    self.__logger.info(Dispatcher.timestamp, "updateDriverStatus", driver.getID(), None, "Update Driver Who is INSERVICE.")
                    self.__driver_tracker.updateDriverStatusWhenInService(driver, self.__rider_tracker)
                    self.__logger.debug(Dispatcher.timestamp, "updateDriverStatus", driver.getID(), None, str(driver))
                else:
                    self.__logger.error(Dispatcher.timestamp, "updateDriverStatus", driver.getID(), None, "Driver Status is Wrong.")
                    raise Exception("Driver Status is Wrong.")


    def updateRidersInWaitDict(self):
        for zone_id in self.__rider_wait_dict.keys():
            for dir_id in self.__rider_wait_dict[zone_id].keys():
                for group_id in self.__rider_wait_dict[zone_id][dir_id].copy().keys():
                    for rider in self.__rider_wait_dict[zone_id][dir_id][group_id].copy().values():
                        if rider.getStatus() == WAITING:
                            self.__rider_tracker.updateRiderStatusWhenWait(rider, self.wait_rider)
                            self.__rider_tracker.checkRiderStatusIfTimeOut(rider)

    def countTotalDriverNumber(self):
        total_len = 0
        for zone_id in self.__driver_dict.keys():
            total_len = total_len + len(self.__driver_dict[zone_id])
        return total_len

    def countDriverNumberEachZone(self):
        self.idle_driver_before_match[Dispatcher.timestamp] = [0]
        for zone_id in self.__driver_dict.keys():
            cnt=0
            for driver in self.__driver_dict[zone_id].values():
                if driver.getStatus() == IDLE:
                    cnt+=1
            self.idle_driver_before_match[Dispatcher.timestamp].append(cnt)

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
                totalProfit += driver.getTripProfit()
        return totalProfit / self.countTotalDriverNumber()

    def calcAverageIdleTimeOfDrivers(self):
        totalIdleTime = 0
        for zone_id in self.__driver_dict.keys():
            for driver in self.__driver_dict[zone_id].values():
                totalIdleTime += driver.getIdleTime()
        return totalIdleTime / self.countTotalDriverNumber()

    def calcAverageTripEffortOfDrivers(self):
        totalTripEffort = 0
        for zone_id in self.__driver_dict.keys():
            for driver in self.__driver_dict[zone_id].values():
                totalTripEffort += driver.getTripEffort()
        return totalTripEffort / self.countTotalDriverNumber()

    def calcAverageWaitTimeOfRiders(self):
        totalWaitTime = 0
        riders = {**self.__rider_serve_dict, **self.__rider_finish_dict}
        for rider in riders.values():
            totalWaitTime +=rider.getWaitTime()
        return totalWaitTime/(self.countRiderNumberInFinishDict()+self.countRiderNumberInServeDict())

    def calcAverageDetourTimeOfRiders(self):
        totalDetourTime = 0
        riders = {**self.__rider_serve_dict, **self.__rider_finish_dict}
        for rider in riders.values():
            totalDetourTime += rider.getDetourTime()
        return totalDetourTime/(self.countRiderNumberInFinishDict()+self.countRiderNumberInServeDict())

    def calcAverageFareOfRiders(self):
        totalFare = 0
        riders = {**self.__rider_serve_dict, **self.__rider_finish_dict}
        for rider in riders.values():
            totalFare += rider.getPrice()
        return totalFare/(self.countRiderNumberInFinishDict()+self.countRiderNumberInServeDict())

    def calcAverageDefaultFareRiders(self):
        totalDefaultFare = 0
        riders = {**self.__rider_serve_dict, **self.__rider_finish_dict}
        for rider in riders.values():
            totalDefaultFare += rider.getDefaultPrice()
        return totalDefaultFare/(self.countRiderNumberInFinishDict()+self.countRiderNumberInServeDict())

    def calcAverageSatOfRiders(self):
        totalSat = 0
        riders = {**self.__rider_serve_dict, **self.__rider_finish_dict, **self.__rider_cancel_dict}
        for rider in riders.values():
            totalSat += rider.getSat()
        return totalSat/(self.countRiderNumberInFinishDict()+self.countRiderNumberInServeDict()+self.countRiderNumberInCancelDict())
























