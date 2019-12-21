from src.Logger.Logger import Logger
import logging

class RequestList:

    timestamp = -1

    def __init__(self):
        self.__logger = Logger("RequestList")
        self.__logger.setLevel(logging.INFO)
        self.__logger.info(RequestList.timestamp, "__INIT__", None, None, "Create RequestList Object.")
        self.__items = []

    def __str__(self):
        ret = "["
        for i in range(0, len(self.__items)):
            ret = ret + str(self.__items[i]) + ", "
        ret = ret + "]"
        return ret

    def first_element(self):
        if self.is_empty():
            self.__logger.error(RequestList.timestamp, "__INIT__", None, None, "No First element exists.")
            raise Exception("No First element exists.")
        return self.__items[0]

    def remove(self):
        item = self.__items.pop(0)
        self.__logger.info(RequestList.timestamp, "remove", None, None, str(item))
        return item


    def is_empty(self):
        return len(self.__items) == 0


    def __len__(self):
        return len(self.__items)


    def add(self, item):
        self.__logger.info(RequestList.timestamp, "add", None, None, str(item))
        self.__items.append(item)
