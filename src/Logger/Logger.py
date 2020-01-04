import logging

class Logger:

    def __init__(self, module):
        # Create the Logger
        logging.basicConfig(filename='./Carpool.log', filemode='w', level=logging.WARNING, format='%(levelname)s - %(name)s - %(message)s')
        #logging.basicConfig(format='%(levelname)s - %(name)s - %(message)s', handlers=[logging.StreamHandler()])
        self.__logger = logging.getLogger(module)
        self.__cycle_obs = []
        self.__func_obs = []
        self.__drid_obs = []
        self.__rdid_obs = []

    def setLevel(self, level=logging.DEBUG):
        self.__logger.setLevel(level)

    def setCycle(self, time):
        self.__cycle_obs = time

    def setFunc(self, func):
        self.__func_obs = func

    def setDrId(self, id):
        self.__drid_obs = id

    def setRdId(self, id):
        self.__rdid_obs = id

    def isCycleEnable(self, timestamp):
        if len(self.__cycle_obs) == 0:
            return True
        elif timestamp in self.__cycle_obs:
            return True
        else:
            return  False

    def isFuncEnable(self, func):
        if len(self.__func_obs) == 0:
            return True
        elif func in self.__func_obs:
            return True
        else:
            return  False

    def isDridEnable(self, id):
        if len(self.__drid_obs) == 0:
            return True
        elif id in self.__drid_obs:
            return True
        else:
            return  False

    def isRdidEnable(self, id):
        if len(self.__rdid_obs) == 0:
            return True
        elif id in self.__rdid_obs:
            return True
        else:
            return  False

    def debug(self, timestamp, func, drid, rdid, msg1, msg2=""):
        if self.isCycleEnable(timestamp) and self.isFuncEnable(func) and self.isDridEnable(drid) and self.isRdidEnable(rdid):
            if drid is not None:
                if rdid is not None:
                    self.__logger.debug("%s - Cycle: %d - %s - %s - %s %s", func, timestamp, drid, rdid, msg1, msg2)
                else:
                    self.__logger.debug("%s - Cycle: %d - %s - %s %s", func, timestamp, drid, msg1, msg2)
            else:
                if rdid is not None:
                    self.__logger.debug("%s - Cycle: %d - %s - %s %s", func, timestamp, rdid, msg1, msg2)
                else:
                    self.__logger.debug("%s - Cycle: %d - %s %s", func, timestamp, msg1, msg2)


    def info(self, timestamp, func, drid, rdid, msg1, msg2=""):
        if self.isCycleEnable(timestamp) and self.isFuncEnable(func) and self.isDridEnable(drid) and self.isRdidEnable(rdid):
            if drid is not None:
                if rdid is not None:
                    self.__logger.info("%s - Cycle: %d - %s - %s - %s %s", func, timestamp, drid, rdid, msg1, msg2)
                else:
                    self.__logger.info("%s - Cycle: %d - %s - %s %s", func, timestamp, drid, msg1, msg2)
            else:
                if rdid is not None:
                    self.__logger.info("%s - Cycle: %d - %s - %s %s", func, timestamp, rdid, msg1, msg2)
                else:
                    self.__logger.info("%s - Cycle: %d - %s %s", func, timestamp, msg1, msg2)


    def warning(self, timestamp, func, drid, rdid, msg1, msg2=""):
        if self.isCycleEnable(timestamp) and self.isFuncEnable(func) and self.isDridEnable(drid) and self.isRdidEnable(rdid):
            if drid is not None:
                if rdid is not None:
                    self.__logger.warning("%s - Cycle: %d - %s - %s - %s %s", func, timestamp, drid, rdid, msg1, msg2)
                else:
                    self.__logger.warning("%s - Cycle: %d - %s - %s %s", func, timestamp, drid, msg1, msg2)
            else:
                if rdid is not None:
                    self.__logger.warning("%s - Cycle: %d - %s - %s %s", func, timestamp, rdid, msg1, msg2)
                else:
                    self.__logger.warning("%s - Cycle: %d - %s %s", func, timestamp, msg1, msg2)


    def error(self, timestamp, func, drid, rdid, msg1, msg2=""):
        if self.isCycleEnable(timestamp) and self.isFuncEnable(func) and self.isDridEnable(drid) and self.isRdidEnable(rdid):
            if drid is not None:
                if rdid is not None:
                    self.__logger.error("%s - Cycle: %d - %s - %s - %s %s", func, timestamp, drid, rdid, msg1, msg2)
                else:
                    self.__logger.error("%s - Cycle: %d - %s - %s %s", func, timestamp, drid, msg1, msg2)
            else:
                if rdid is not None:
                    self.__logger.error("%s - Cycle: %d - %s - %s %s", func, timestamp, rdid, msg1, msg2)
                else:
                    self.__logger.error("%s - Cycle: %d - %s %s", func, timestamp, msg1, msg2)


    def critical(self, timestamp, func, drid, rdid, msg1, msg2=""):
        if self.isCycleEnable(timestamp) and self.isFuncEnable(func) and self.isDridEnable(drid) and self.isRdidEnable(rdid):
            if drid is not None:
                if rdid is not None:
                    self.__logger.critical("%s - Cycle: %d - %s - %s - %s %s", func, timestamp, drid, rdid, msg1, msg2)
                else:
                    self.__logger.critical("%s - Cycle: %d - %s - %s %s", func, timestamp, drid, msg1, msg2)
            else:
                if rdid is not None:
                    self.__logger.critical("%s - Cycle: %d - %s - %s %s", func, timestamp, rdid, msg1, msg2)
                else:
                    self.__logger.critical("%s - Cycle: %d - %s %s", func, timestamp, msg1, msg2)


