from collections import OrderedDict
from src.Configure.Config import *
from src.Graph.Graph import Graph
from src.Driver.RoutingInDistance import RoutingInDistance
from src.Logger.Logger import Logger
import logging
import math


class Driver:

    timestamp = -1

    def __init__(self, id, pCurr):
        # logger in Dispatcher
        self.__logger = Logger('Driver')
        #self.__logger.setLevel(logging.DEBUG)
        self.__logger.info(Driver.timestamp, "__INIT__", None, None, "Create A Driver Object")

        self.__id = id
        self.__pos = pCurr

        self.__status = IDLE
        self.__riders = {}
        self.__trip_route = []
        self.__trip_effort = 0
        self.__trip_profit = 0
        self.__idle_time = 0
        self.__finish_trip_time = -1

    def __str__(self):
        ret = "{" + str(self.__id) + ", " + str(self.__pos) + ", " + str(self.__status) + ", " + str(self.__trip_effort) + ", "
        ret = ret + str(self.__trip_profit) + ", "
        ret = ret + "Riders: " + self.showRidersOnBoard() + ", "
        ret = ret + "Route: " + self.showTripRoute() + "}"
        return ret

    def showRidersOnBoard(self):
        ret = "["
        if len(self.__riders):
            for rider_id in OrderedDict(sorted(self.__riders.items(), key=lambda t: t[0])).keys():
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

    def getID(self):
        return self.__id

    def setRiders(self, riders):
        for rider_id, rider in riders.items():
            self.__riders[rider_id] = rider

    def getRider(self, id):
        if id in self.__riders.keys():
            return self.__riders[id]
        else:
            self.__logger.error(Driver.timestamp, "getRider", self.getID(), id, "Rider not in vehicle.")
            raise Exception("Rider not in vehicle.")

    def removeRider(self, id):
        if id in self.__riders.keys():
            del self.__riders[id]
        else:
            self.__logger.error(Driver.timestamp, "removeRider", self.getID(), id, "Rider not in vehicle.")
            raise Exception("Rider not in vehicle.")

    def calcTripRoute(self):
        if len(self.__trip_route) == 0:
            route_strategy = RoutingInDistance(self.__riders, self.__trip_route)
            route_strategy.planRoute()
        else:
            self.__logger.error(Driver.timestamp, "calcTripRoute", self.getID(), None, "Trip route is empty.")
            raise Exception("Trip route is empty.")

    def popTripRoute(self):
        if len(self.__trip_route) > 0:
            return self.__trip_route.pop(0)
        else:
            self.__logger.error(Driver.timestamp, "popTripRoute", self.getID(), None, "Nothing to be poped.")
            raise Exception("Nothing to be poped.")

    def getTripRoute(self):
        return self.__trip_route

    #must calc route first
    def calcTripEffort(self):
        total_effort = 0
        pos = self.getPos()
        for elem in self.__trip_route:
            total_effort = total_effort + Graph.queryTravelCost(pos, elem.getZoneID())
            elem.setEventTime(Driver.timestamp + total_effort)
            if elem.getEvent() == DROPOFF:
                rider = self.__riders[elem.getRiderID()]
                rider.setArrivalTimestamp(Driver.timestamp + total_effort)
                rider.calcDetourTime(total_effort) #detour time is b/w the rerquest accepted and arrive at destination.
            pos = elem.getZoneID()

        if total_effort < 0:
            self.__logger.warning(Driver.timestamp, "calcTripEffort", self.getID(), None, "Trip effort value is unresonable ")
            raise Exception("Trip effort value is unresonable ")
        else:
            self.__trip_effort = total_effort

    def tickTripEffort(self):
        self.__trip_effort += 1

    def getTripEffort(self):
        return self.__trip_effort

    def notifyRiderPrice(self):
        shared_number = len(self.__riders)
        for rider in self.__riders.values():
            rider.calcPrice(shared_number)

    #must calc route effort and rider price first
    def calcTripProfit(self):
        trip_revenue = 0
        if len(self.__riders) > 0:
            for rider in self.__riders.values():
                if rider.getPrice() is not math.inf:
                    trip_revenue += rider.getPrice()
                else:
                    self.__logger.error(Driver.timestamp, "calcTripEffort", self.getID(), None, "Price value is unresonable ")
                    raise Exception("Price value is unresonable ")
            self.__trip_profit = trip_revenue - self.__trip_effort * COST_PER_CYCLE
        else:
            self.__logger.error(Driver.timestamp, "calcTripEffort", self.getID(), None, "No riders in vehicle.")
            raise Exception("No riders in vehicle.")

    def getTripProfit(self):
        return self.__trip_profit

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

    def setFinishTripTime(self, time):
        self.__finish_trip_time = time

    def getFinishTripTime(self):
        return self.__finish_trip_time


