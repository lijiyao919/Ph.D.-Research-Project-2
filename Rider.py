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
        self.__direction = self.__calcDirection(srcX, srcY, destX, destY)
        self.__defaultPrice = dP
        self.__patience = pat

        self.__status = WAITING
        self.__price = 0.0
        self.__wait_time = 0.0
        self.__detour_time = 0.0
        self.__sat = 0.0

    def __str__(self):
        ret = "{" + str(self.__id) + ', ' + str(self.__startTime) + ", " +  str(self.__srcZone) + ", " + str(self.__destZone) + ", " + \
                  str(self.__direction) + ", " + str(self.__defaultPrice) +", "+ str(self.__patience) + ", " + str(self.__status) + ", " + \
                  str(self.__price) + ", " +str(self.__wait_time) + ", " + str(self.__detour_time) +  ", " + str(self.__sat) + "}"
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

    def calcDetourTime(self, curr_travel_time):
        self.__detour_time = curr_travel_time - Graph.queryTravelCost(str(self.__srcZone), str(self.__destZone))


    def calcPrice(self, n_shared):
        self.__price = self.__defaultPrice * 0.9 * math.exp(-0.05*self.__detour_time)
        if n_shared == 1:
            self.__price = self.__price * 0.96
        elif n_shared == 2:
            self.__price = self.__price * 0.93
        elif n_shared == 3:
            self.__price = self.__price * 0.90
        elif n_shared == 4:
            self.__price = self.__price * 0.87
        else:
            pass

    def calcSatisfaction(self):
        Wp = random.uniform(1, 1.5)
        Wt = random.uniform(0.5, 1)
        self.__sat = math.exp((self.__defaultPrice-self.__price)*Wp) - math.exp(self.__detour_time*Wt) + 1

    def getRiderID(self):
        return self.__id

    def getDetourTime(self):
        return self.__detour_time

    def getPrice(self):
        return self.__price

#TCs(not remove)
#uID, sT, sZ, dZ, dP, pat, srcX, srcY, destX, destY
'''r0=Rider("R0", 0, 8, 24, 7.75, 20, -87.6333, 41.8996, -87.6764, 41.9012)
r1=Rider("R1", 0, 7, 6, 6, 20, -87.6495, 41.9227, -87.656, 41.9442)
r2=Rider("R1", 0, 7, 6, 6, 20, 0, 0, -1, 0)
r0.calcDetourTime(3)
r0.calcPrice(4)
r0.calcSatisfaction()
print(r0)'''