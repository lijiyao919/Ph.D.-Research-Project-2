from collections import defaultdict

class Group:
    def __init__(self, id):
        self.__gid = id
        self.__riders = defaultdict(lambda:None)
        self.__destination = 0

    def __str__(self):
        res = "{" + str(self.__gid) + ": ["
        for rider in self.__riders.values():
            res = res + str(rider.getID())
        res = res + "]}"
        return res

    def addRider(self, rider):
        self.__riders[rider.getID()] = rider
        self.__destination = rider.getDestZone()

    def isInGroup(self, rider):
        if rider.getID() in self.__riders.keys():
            return True
        else:
            return False

    def getID(self):
        return self.__gid

    def getGroupSize(self):
        return len(self.__riders)

    def getDestination(self):
        return self.__destination

    def getRiders(self):
        return self.__riders


a= Group(1)