from src.Logger import Logger
from src.Config import *

class DriverStatusTracker:

    timestamp = -1

    def __init__(self, driver_dict):
        self.__logger = Logger("DriverStatusTracker")

        self.__driver_dict = driver_dict

    def updateDriverStatusAfterMatching(self, driver):
        driver.setStatus(INSERVICE)
        driver.setTripStartTime(DriverStatusTracker.timestamp)
        driver.calcTripRoute()
        driver.calcTripEffort()
        driver.calcTripProfit()

    def updateDriverStatusWhenInService(self, driver):
        next_event_time = driver.getTripRoute()[0].getArrivalTime()
        if  next_event_time <= DriverStatusTracker.timestamp:
            elem = driver.popTripRoute()
            del self.__driver_dict[driver.getPos()][driver.getID()]
            self.__driver_dict[elem.getZoneID()][driver.getID()] = driver
            driver.setPos(elem.getZoneID())
            if elem.task == DROPOFF:
                driver.removeRider(elem.getRiderID())

    def updateDriverStatusWhenIdle(self, driver):
        driver.tickIdleTime()










