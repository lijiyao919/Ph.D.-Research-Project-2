from src.Config import *
from src.Graph import Graph
from src.RoutingInDistance import RoutingInDistance
from src.Logger import Logger
import logging


class Driver:

    timestamp = -1

    def __init__(self, id, pCurr):
        # logger in Dispatcher
        self.__logger = Logger('Driver')
        self.__logger.setLevel(logging.DEBUG)
        self.__logger.info(Driver.timestamp, "__INIT__", None, None, "Create A Driver Object")

        self.__id = id
        self.__pos = pCurr

        self.__status = IDLE
        self.__riders = {}
        self.__trip_route = []
        self.__trip_effort = 0
        self.__trip_profit = 0
        self.__idle_time = 0

    def __str__(self):
        ret = "{" + str(self.__id) + ", " + str(self.__pos) + ", " + str(self.__status) + ", " + str(self.__trip_effort) + ", "
        ret = ret + str(self.__trip_profit) + ", "
        ret = ret + "Riders: " + self.showRidersOnBoard() + ", "
        ret = ret + "Route: " + self.showTripRoute() + "}"
        return ret

    def showRidersOnBoard(self):
        ret = "["
        if len(self.__riders):
            for rider_id in self.__riders.keys():
                ret = ret + rider_id + ", "
            ret = ret[0:len(ret) - 2] + "]"
        else:
            ret = ret + "]"
        return ret

    def showTripRoute(self):
        ret = "["
        if len(self.__trip_route):
            for elem in self.__trip_route:
                ret = ret + str(elem.getZoneID()) + ", "
            ret = ret[0:len(ret) - 2] + "]"
        else:
            ret = ret + "]"
        return ret

    def setRiders(self, riders):
        self.__riders = riders

    def getRider(self, id):
        if id in self.__riders.keys():
            return self.__riders[id]
        else:
            self.__logger.error(Driver.timestamp, "getRider", self.getID(), id, "Rider not in vehicle.")

    def removeRider(self, id):
        if id in self.__riders.keys():
            del self.__riders[id]
        else:
            self.__logger.error(Driver.timestamp, "removeRider", self.getID(), id, "Rider not in vehicle.")

    def calcTripRoute(self):
        if len(self.__trip_route) == 0:
            route_strategy = RoutingInDistance(self.__riders, self.__trip_route)
            route_strategy.planRoute()
        else:
            self.__logger.error(Driver.timestamp, "calcTripRoute", self.getID(), None, "Trip route is empty.")

    def popRoute(self):
        return self.__trip_route.pop(0)

    def getRoute(self):
        return self.__trip_route

    def calcTripEffort(self):
        total_effort = 0
        pos = self.getPos()
        for elem in self.__trip_route:
            total_effort = total_effort + Graph.queryTravelCost(pos, elem.getZoneID())
            elem.setEventTime(Driver.timestamp + total_effort)
            if elem.getEvent() == DROPOFF:
                rider = self.__riders[elem.getRiderID()]
                rider.setArrivalTimestamp(Driver.timestamp + total_effort)
                rider.calcDetourTime(total_effort)
            pos = elem.zone_id

        if total_effort <= 0:
            self.__logger.warning(Driver.timestamp, "calcTripEffort", self.getID(), None, "Trip effort value is unresonable ")
        else:
            self.__trip_effort = total_effort

    def getTripEffort(self):
        return self.__trip_effort

    def calcTripProfit(self):
        trip_revenue = 0
        for elem in self.__trip_route:
            trip_revenue += self.__riders[elem.getRiderID()].getPrice()
        trip_profit = trip_revenue - self.__trip_effort * COST_PER_MINUTE

        if trip_profit <= 0:
            self.__logger.warning(Driver.timestamp, "calcTripEffort", self.getID(), None, "Trip profit value is unresonable ")
        else:
            self.__trip_profit = trip_profit

    def getProfit(self):
        return self.__trip_profit

    def getID(self):
        return self.__id

    def setPos(self, zid):
        self.__pos = zid

    def getPos(self):
        return self.__pos

    def setStatus(self, status):
        self.__status = status

    def getStatus(self):
        return self.__status

    def tickIdleTime(self):
        self.__idle_time += 1

    def getIdleTime(self):
        return self.__idle_time


