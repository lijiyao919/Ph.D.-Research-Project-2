from src.Configure.Config import *
from src.Graph.Graph import Graph
import numpy as np
import math
from src.Logger.Logger import Logger
import logging

class Rider:
    timestamp = -1

    def __init__(self, uID, sT, sZ, dZ, dP, pat, srcX, srcY, destX, destY):
        # logger in Dispatcher
        self.__logger = Logger('Rider')
        #self.__logger.setLevel(logging.DEBUG)
        self.__logger.info(Rider.timestamp, "__INIT__", None, None, "Create A Rider Object")

        self.__id = uID
        self.__request_timestamp = sT
        self.__srcZone = sZ
        self.__destZone = dZ
        self.__default_price = dP
        self.__price = math.inf
        self.__patience = pat
        self.__dirID = self.__assignDirID(srcX, srcY, destX, destY)
        self.__shortest_time = Graph.queryTravelCost(sZ, dZ)
        self.__arrival_timestamp = None
        self.__groupID = None

        self.__status = WAITING
        self.__wait_time = 0
        self.__detour_time = -1
        self.__sat = 0

        if self.__default_price > 100:
            self.__logger.warning(Rider.timestamp, "__INIT__", None, self.getID(), str(self))

    def __str__(self):
        ret = "{" + str(self.__id) + ', ' + str(self.__request_timestamp) +  ", " + str(self.__srcZone) + ", " + str(self.__destZone) + ", " + \
              str(self.__default_price) + ", "  + str(self.__price) +  ", " + str(self.__patience) + ", " + str(self.__dirID) +", " + \
              str(self.__shortest_time) + ", " +  str(self.__arrival_timestamp) + ", " + str(self.__groupID) + ", " +\
              str(self.__status) + ", " + str(self.__wait_time) + ", " + str(self.__detour_time) +  ", " +  str(self.__sat) + "}"
        return ret

    #https://stackoverflow.com/questions/13226038/calculating-angle-between-two-vectors-in-python
    #The range is [-180, 180)
    def __calcDirection(self, srcX, srcY, destX, destY):
        p1 = [srcX, srcY]
        p0 = [destX, destY]
        p2 = p1 + np.array([1, 0])

        v0 = np.array(p0) - np.array(p1)
        v1 = np.array(p2) - np.array(p1)
        angle = np.math.atan2(np.linalg.det([v0, v1]), np.dot(v0, v1))
        return np.degrees(angle)*(-1)

    #Tansfer from [-180,180) to [0,360).
    #calculate DirID by dividing the DIR_THRESHOLD
    def __assignDirID(self, srcX, srcY, destX, destY):
        dir = self.__calcDirection(srcX, srcY, destX, destY)
        return int((dir+180)/DIR_THRESHOLD)

    def getDirID(self):
        return self.__dirID

    def setGroupID(self, grpID):
        self.__groupID = grpID

    def getGroupID(self):
        return self.__groupID

    def tickWaitTime(self):
        self.__wait_time += 1

    def getWaitTime(self):
        return self.__wait_time

    def getShortestTime(self):
        return self.__shortest_time

    def calcDetourTime(self, time):
        self.__detour_time = time - self.__shortest_time

    def getDetourTime(self):
        return self.__detour_time

    def setArrivalTimestamp(self, time):
        self.__arrival_timestamp = time

    def getArrivalTimestamp(self):
        return self.__arrival_timestamp

    #prerequest: calc detour time first
    def calcPrice(self, n_shared):
        if self.__detour_time < 0:
            self.__logger.error(Rider.timestamp, "calcPrice", None, self.getID(), "Detour time is unreasonable.")
            raise Exception("Detour time is unreasonable.")
        self.__price = self.__default_price * math.exp(DETOUR_WEIGH * -self.__detour_time)
        if n_shared == 1:
            self.__price = self.__price * DISCOUNT_1
        elif n_shared == 2:
            self.__price = self.__price * DISCOUNT_2
        elif n_shared == 3:
            self.__price = self.__price * DISCOUNT_3
        elif n_shared == 4:
            self.__price = self.__price * DISCOUNT_4
        else:
            self.__logger.error(Rider.timestamp, "calcPrice", None, self.getID(), "Shared number is incorret.")
            raise Exception("Shared number is incorret.")

    def getPrice(self):
        return self.__price

    def getDefaultPrice(self):
        return self.__default_price

    def calcSat(self):
        if self.__detour_time < 0:
            self.__logger.error(Rider.timestamp, "calcSat", None, self.getID(), "Detour time is unreasonable.")
            raise Exception("Detour time is unreasonable.")
        elif self.__price >= self.__default_price:
            self.__logger.error(Rider.timestamp, "calcSat", None, self.getID(), "Price is unreasonable.")
            raise Exception("Price is unreasonable.")
        else:
            self.__sat = (self.__default_price-self.__price)*SAT_PRICE - math.expm1(self.__detour_time)
            if self.__sat > 10000000:
                self.__logger.warning(Rider.timestamp, "calcPrice", None, self.getID(), "SAT is too large", str(self))


    def getSat(self):
        return self.__sat

    def getID(self):
        return self.__id

    def getRequestTimeStamp(self):
        return self.__request_timestamp

    def getSrcZone(self):
        return self.__srcZone

    def getDestZone(self):
        return self.__destZone

    def getPatience(self):
        return self.__patience

    def setStatus(self, status):
        self.__status = status

    def getStatus(self):
        return self.__status



