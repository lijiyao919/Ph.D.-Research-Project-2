from Config import *

class Driver:
    def __init__(self, id, pCurr):
        self.__id = id
        self.__pos = pCurr

        self.__status = IDLE
        self.__capacity = VEHICLE_CAPACITY
        self.__rider_serviced = []
        self.__route = []
        self.__profit = 0.0

    def __str__(self):
        ret = "{" + str(self.__id) + ", " + str(self.__pos) + ", " + str(self.__status) + ", " + str(self.__capacity) + ", "
        ret = ret + "Riders: " + self.__showRiders() + ", "
        ret = ret + "Route: " + self.__showRoute() + ", "
        ret = ret + str(self.__profit) + "}"
        return ret

    def __showRiders(self):
        ret = "["
        if len(self.__rider_serviced):
            for rider in self.__rider_serviced:
                ret = ret + rider.getRiderID() + ", "
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

    def setRoute(self, route):
        self.__route = route

    def setProfit(self, profit):
        self.__profit = profit

    def setStatus(self, status):
        self.__status = status

#TCs(Not Remove)
'''from Rider import Rider
d1 = Driver("V0", 23)
r0=Rider("R0", 0, 8, 24, 7.75, 20, -87.6333, 41.8996, -87.6764, 41.9012)
r1=Rider("R1", 0, 7, 6, 6, 20, -87.6495, 41.9227, -87.656, 41.9442)
d1.assignRiders([r0, r1])
d1.setRoute([23,24])
d1.setProfit(30)
d1.setStatus(INSERVICE)
print(d1)'''
