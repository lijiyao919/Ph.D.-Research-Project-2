from src.Logger import Logger
from src.Config import *

class RiderStatusTracker:
    timestamp = -1

    def __init__(self, driver_dict, wait_dict, serve_dict, finish_dict, cancel_dict):
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
            del self.__wait_dict[zone_id][dir][group_id][rider.getID()]
            if len(self.__wait_dict[zone_id][dir][group_id]) == 0:
                del self.__wait_dict[zone_id][dir][group_id]
        else:
            self.__logger.debug(RiderStatusTracker.timestamp, "updateRiderStatusWhenTimeOut", None, rider.getID(), "Cancel Time Should be: ",
                                str(rider.getRequestTimeStamp() + rider.getPatience()))


    def updateRiderStatusAfterMatching(self, rider, group_num):
        rider.calcPrice(group_num)
        rider.calcSat()
        rider.setStatus(SERVING)
        self.__serve_dict[rider.getID()] = rider


    def updateRiderStatusWhenInService(self,rider):
        if rider.getStatus() == SERVING:
            if rider.getArrivalTimestamp() <= RiderStatusTracker.timestamp:
                self.__finish_dict[rider.getID()] = rider
                rider.setStatus(FINISHED)
                del self.__serve_dict[rider.getID()]
        else:
            self.__logger.error(RiderStatusTracker.timestamp, "updateRiderStatusWhenInService", None, rider.getID(), "The status and dict not match.")


    def updateRiderStatusWhenWait(self,rider):
        rider.tickWaitTime()

