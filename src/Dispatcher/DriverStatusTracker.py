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

    def updateDriverStatusWhenIdle(self, driver, no_work_dict):
        if driver.getStatus() == IDLE:
            if driver.getFinishTripTime() != DriverStatusTracker.timestamp:
                driver.tickIdleTime()
                no_work_dict[DriverStatusTracker.timestamp][driver.getPos()] += 1
                theZoneRatio = self.getSmoothRatio(driver.getPos())
                for adjacent_zone in AdjList_Chicago[driver.getPos()]:
                    adjRatio = self.getSmoothRatio(adjacent_zone)
                    if theZoneRatio - adjRatio > IDLE_MOVE_THRE:
                        del self.__driver_dict[driver.getPos()][driver.getID()]
                        self.__driver_dict[adjacent_zone][driver.getID()] = driver
                        driver.setPos(adjacent_zone)
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











