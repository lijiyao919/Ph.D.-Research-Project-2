from Config import *
from Graph import Graph
import numpy as np
import math
import random

class Rider:
    def __init__(self, uID, sT, sZ, dZ, dP, pat, srcX, srcY, destX, destY):
        self.__id = uID
        self.__startTime = sT
        self.__srcZone = sZ
        self.__destZone = dZ
        self.__patience = pat
        self.__direction = self.__calcDirection(srcX, srcY, destX, destY)
        self.__shortest_time = Graph.queryTravelCost(str(sZ), str(dZ))
        self.__default_price = dP

        self.__status = WAITING
        self.__wait_time = 0.0
        self.__travel_time = 0.0
        self.__price = dP
        self.__sat = 0.0

    def __str__(self):
        ret = "{" + str(self.__id) + ', ' + str(self.__startTime) + ", " +  str(self.__srcZone) + ", " + str(self.__destZone) + ", " + \
                  str(self.__patience) + ", " + str(self.__direction) +", "+ str(self.__shortest_time) + ", " + str(self.__default_price) + ", " + \
                  str(self.__status) + ", " + str(self.__wait_time) + ", " + str(self.__travel_time) +  ", " + str(self.__price) +  ", " + str(self.__sat) + "}"
        return ret

    #https://stackoverflow.com/questions/13226038/calculating-angle-between-two-vectors-in-python
    def __calcDirection(self, srcX, srcY, destX, destY):
        p1 = [srcX, srcY]
        p0 = [destX, destY]
        p2 = p1 + np.array([1, 0])

        v0 = np.array(p0) - np.array(p1)
        v1 = np.array(p2) - np.array(p1)
        angle = np.math.atan2(np.linalg.det([v0, v1]), np.dot(v0, v1))
        return np.degrees(angle)*(-1)

    def tickWaitTime(self):
        self.__wait_time += 1

    def getWaitTime(self):
        return self.__wait_time

    def setTravelTime(self, time):
        self.__travel_time = time

    def getTravelTime(self):
        return self.__travel_time

    def getShortestTime(self):
        return self.__shortest_time

    def getDetourTime(self):
        return self.__travel_time - self.__shortest_time

    def calcPrice(self, n_shared):
        if self.getDetourTime() < 0:
            return math.inf
            #log here
        self.__price = self.__default_price * math.exp(DETOUR_WEIGH * -self.getDetourTime())
        if n_shared == 1:
            self.__price = self.__price * DISCOUNT_1
        elif n_shared == 2:
            self.__price = self.__price * DISCOUNT_2
        elif n_shared == 3:
            self.__price = self.__price * DISCOUNT_3
        elif n_shared == 4:
            self.__price = self.__price * DISCOUNT_4
        else:
            pass
            #log here

    def getPrice(self):
        return self.__price

    def calcSat(self):
        self.__sat = math.exp((self.__default_price-self.__price)*SAT_PRICE) - \
                     math.exp(self.getDetourTime()*SAT_TIME) + 1
        #print(math.exp((self.__default_price-self.__price)*SAT_PRICE))
        #print(math.exp(self.getDetourTime()*SAT_TIME) - 1)

    def getSat(self):
        return self.__sat

    def getID(self):
        return self.__id

    def getStartTime(self):
        return self.__startTime

    def getSrcZone(self):
        return self.__srcZone

    def getDestZone(self):
        return self.__destZone

    def getPatience(self):
        return self.__patience

    def getDirection(self):
        return self.__direction

    def getStatus(self):
        return self.__status


