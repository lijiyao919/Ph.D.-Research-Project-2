from Config import *

class Driver:
    def __init__(self, id, pCurr):
        self.__id = id
        self.__pos = pCurr

        self.__status = IDLE
        self.__trip_effort = 0
        self.__route = []
        self.__accept_time = 0

        self.__profit = 0.0
        self.__idle_time = 0

    def __str__(self):
        ret = "{" + str(self.__id) + ", " + str(self.__pos) + ", " + str(self.__status) + ", " + str(self.__trip_effort) + ", "
        ret = ret + "Riders: " + self.__showRiders() + ", "
        ret = ret + "Route: " + self.__showRoute() + ", "
        ret = ret + str(self.__profit) + ", " + str(self.__accept_time) + "}"
        return ret

    def __showRiders(self):
        ret = "["
        if len(self.__route):
            for rider_id, _ in self.__route:
                ret = ret + rider_id + ", "
            ret = ret[0:len(ret) - 2] + "]"
        else:
            ret = ret + "]"
        return ret

    def __showRoute(self):
        if len(self.__route):
            ret = "[" + str(self.getPos()) + ", "
            ret = ret + str(self.__route[0][1].getSrcZone()) + ", "
            for _, rider in self.__route:
                ret = ret + str(rider.getDestZone()) + ", "
            ret = ret[0:len(ret) - 2] + "]"
        else:
            ret = "[]"
        return ret

    def setRoute(self, route):
        self.__route = route

    def popRoute(self):
        return self.__route.pop(0)

    def getRoute(self):
        return self.__route

    def calcProfit(self):
        trip_profit = 0
        for _, rider in self.__route:
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

    def setTripStartTime(self, time):
        self.__accept_time = time

    def getTripStartTime(self):
        return self.__accept_time

    def tickIdleTime(self):
        self.__idle_time += 1

    def getIdleTime(self):
        return self.__idle_time


