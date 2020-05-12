from src.Logger.Logger import Logger
from src.Configure.Config import *
from src.Graph.Map import AdjList_Chicago
from src.Import.ImportDemandEvaluation import ImportDemandEvaluation


class DriverStatusTracker:

    timestamp = -1

    def __init__(self, driver_dict):
        self.__logger = Logger("DriverStatusTracker")
        self.__driver_dict = driver_dict
        self.__demand_evaluation = ImportDemandEvaluation.getInstance()


    def updateDriverStatusAfterMatching(self, driver):
        driver.setStatus(INSERVICE)
        driver.calcTripRoute()
        driver.calcTripEffort()
        driver.notifyRiderPrice()
        driver.calcTripProfit()

    def updateDriverStatusWhenInService(self, driver, rider_tracker):
        for elem in driver.getTripRoute().copy():
            if  elem.getEventTime() <= DriverStatusTracker.timestamp:
                #handle rider on board
                curr_elem = driver.popTripRoute()
                if curr_elem.getEvent() == DROPOFF:
                    rider = driver.getRider(curr_elem.getRiderID())
                    rider_tracker.notifyRiderToFinishTrip(rider)
                    driver.removeRider(curr_elem.getRiderID())
                #handle driver
                del self.__driver_dict[driver.getPos()][driver.getID()]
                self.__driver_dict[curr_elem.getZoneID()][driver.getID()] = driver
                driver.setPos(curr_elem.getZoneID())

        if len(driver.getTripRoute()) == 0:
            driver.setStatus(IDLE)
            driver.setFinishTripTime(DriverStatusTracker.timestamp)

    def updateDriverStatusWhenIdle(self, driver, no_work_dict, R):
        if driver.getStatus() == IDLE:
            if driver.getFinishTripTime() != DriverStatusTracker.timestamp:
                driver.tickIdleTime()
                no_work_dict[DriverStatusTracker.timestamp][driver.getPos()] += 1
                min_ratio = 1000
                min_zone = None
                for adjacent_zone in AdjList_Chicago[driver.getPos()]:
                    adjRatio = self.getSmoothRatio(adjacent_zone)
                    if adjRatio < min_ratio:
                        min_ratio=adjRatio
                        min_zone=adjacent_zone
                theZoneRatio = self.getSmoothRatio(driver.getPos())
                #print(str((DriverStatusTracker.timestamp,driver.getPos()))+': '+str(self.__idle_move_threshold[driver.getPos()]))
                #print(R, DriverStatusTracker.timestamp, driver.getPos(), theZoneRatio - min_ratio)
                driver.learner.runQLearning(None, DriverStatusTracker.timestamp, driver.getPos(), theZoneRatio - min_ratio)
                A = driver.learner.selectAction((DriverStatusTracker.timestamp, driver.getPos(), theZoneRatio - min_ratio))

                #if theZoneRatio - min_ratio > idle_move_threshold:
                if A == 1:
                    del self.__driver_dict[driver.getPos()][driver.getID()]
                    self.__driver_dict[min_zone][driver.getID()] = driver
                    driver.setPos(min_zone)
                    driver.tickTripEffort()
        else:
            self.__logger.error(DriverStatusTracker.timestamp, "updateDriverStatusWhenIdle", driver.getID(), None, "Driver Status is Wrong.")
            raise Exception("The driver status and dict not match.")


    def getSmoothRatio(self, zone_id):
        total = 0
        for driver in self.__driver_dict[zone_id].values():
            if driver.getStatus() == IDLE and driver.getFinishTripTime() != DriverStatusTracker.timestamp:
                total += 1
        return total/(1+self.__demand_evaluation.getSmoothRatioOfSupplyDemand(zone_id))











