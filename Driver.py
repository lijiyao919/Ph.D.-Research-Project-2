from Config import *

class Driver:
    def __init__(self, id, pCurr):
        self.__id = id
        self.__pos = pCurr

        self.__status = IDLE
        self.__trip_effort = 0
        self.__rider_serviced = []
        self.__route = []
        self.__profit = 0.0

    def __str__(self):
        ret = "{" + str(self.__id) + ", " + str(self.__pos) + ", " + str(self.__status) + ", " + str(self.__trip_effort) + ", "
        ret = ret + "Riders: " + self.__showRiders() + ", "
        ret = ret + "Route: " + self.__showRoute() + ", "
        ret = ret + str(self.__profit) + "}"
        return ret

    def __showRiders(self):
        ret = "["
        if len(self.__rider_serviced):
            for rider in self.__rider_serviced:
                ret = ret + rider.getID() + ", "
            ret = ret[0:len(ret) - 2] + "]"
        else:
            ret = ret + "]"
        return ret

    def __showRoute(self):
        ret = "["
        if len(self.__route):
            for zone in self.__route:
                ret = ret + str(zone) + ", "
            ret = ret[0:len(ret) - 2] + "]"
        else:
            ret = ret + "]"
        return ret

    def assignRiders(self, riders):
        self.__rider_serviced = riders

    def getRiders(self):
        return self.__rider_serviced

    def setRoute(self, route):
        self.__route = route

    def getRoute(self):
        return self.__route

    def calcProfit(self):
        trip_profit = 0
        for rider in self.__rider_serviced:
            trip_profit += rider.getPrice()
        if self.__trip_effort == 0:
            pass
            #log here
        trip_profit -= self.__trip_effort * COST_PER_MINUTE
        self.__profit += trip_profit

    def getProfit(self):
        return self.__profit

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

    def setTripEffort(self, time):
        self.__trip_effort = time

    def getTripEffort(self):
        return self.__trip_effort


