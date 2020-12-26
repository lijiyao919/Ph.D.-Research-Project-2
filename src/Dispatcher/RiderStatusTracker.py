from src.Logger.Logger import Logger
from src.Configure.Config import *

class RiderStatusTracker:
    timestamp = -1

    def __init__(self, wait_dict, serve_dict, finish_dict, cancel_dict):
        self.__logger = Logger("RiderStatusTracker")

        self.__wait_dict = wait_dict
        self.__serve_dict = serve_dict
        self.__finish_dict = finish_dict
        self.__cancel_dict = cancel_dict

    def checkRiderStatusIfTimeOut(self, rider):
        if RiderStatusTracker.timestamp - rider.getRequestTimeStamp() >= rider.getPatience():
            rider.setStatus(CANCEL)
            self.__cancel_dict[rider.getID()] = rider
            zone_id = rider.getSrcZone()
            dir = rider.getDirID()
            group_id = rider.getGroupID()
            del (self.__wait_dict[zone_id][dir][group_id].getRiders())[rider.getID()]
            if self.__wait_dict[zone_id][dir][group_id].getGroupSize() == 0:
                del self.__wait_dict[zone_id][dir][group_id]
            #cancel_dict[RiderStatusTracker.timestamp][rider.getSrcZone()] += 1
        else:
            self.__logger.debug(RiderStatusTracker.timestamp, "updateRiderStatusWhenTimeOut", None, rider.getID(), "Cancel Time Should be: ",
                                str(rider.getRequestTimeStamp() + rider.getPatience()))


    def updateRiderStatusAfterMatching(self, rider):
        rider.calcSat()
        rider.setStatus(SERVING)
        self.__serve_dict[rider.getID()] = rider


    def notifyRiderToFinishTrip(self, rider):
        if rider.getStatus() == SERVING:
            self.__finish_dict[rider.getID()] = rider
            rider.setStatus(FINISHED)
            del self.__serve_dict[rider.getID()]
        else:
            self.__logger.error(RiderStatusTracker.timestamp, "updateRiderStatusWhenInService", None, rider.getID(), "The status and dict not match.")
            raise Exception("The rider status and dict not match.")


    def updateRiderStatusWhenWait(self,rider,wait_rider_dict):
        if rider.getStatus() == WAITING:
            rider.tickWaitTime()
            wait_rider_dict[RiderStatusTracker.timestamp][rider.getSrcZone()] += 1
        else:
            self.__logger.error(RiderStatusTracker.timestamp, "updateDriverStatusWhenIdle", None, rider.getID(), "Rider Status is Wrong.")
            raise Exception("The rider status and dict not match.")


