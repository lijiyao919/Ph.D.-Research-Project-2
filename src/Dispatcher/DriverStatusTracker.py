from src.Logger.Logger import Logger
from src.Configure.Config import *
from src.Dispatcher.RiderStatusTracker import RiderStatusTracker


class DriverStatusTracker:

    timestamp = -1

    def __init__(self, driver_dict):
        self.__logger = Logger("DriverStatusTracker")
        self.__driver_dict = driver_dict

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
        else:
            self.__logger.error(DriverStatusTracker.timestamp, "updateDriverStatusWhenIdle", driver.getID(), None, "Driver Status is Wrong.")
            raise Exception("The driver status and dict not match.")











