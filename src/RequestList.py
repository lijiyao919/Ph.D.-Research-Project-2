from src.Logger import Logger
import logging

class RequestList:

    timestamp = -1

    def __init__(self):
        self.log = Logger("RequestList")
        self.log.setLevel(logging.INFO)
        self.log.info(RequestList.timestamp, "__INIT__", None, None, "Create RequestList Object.")
        self.items = []


    def __str__(self):
        ret = "["
        # As long as there is another element in self._items,
        # append its string representation to ret
        for i in range(0, len(self.items)):
            ret = ret + str(self.items[i]) + ", "
        # Finishing touch on ret to close the brackets
        ret = ret[0:len(ret)-2] + "]"
        # If self._items was empty, modify ret
        if ret == "]":
            ret = "None"
        return ret

    def first_element(self):
        return self.items[0]


    def remove(self):
        return self.items.pop(0)


    def is_empty(self):
        return len(self.items) == 0


    def __len__(self):
        return len(self.items)


    def add(self, item):
        self.items.append(item)
