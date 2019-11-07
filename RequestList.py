from Logger import Logger

class RequestList:

    timestamp = -1

    def __init__(self):
        self.log = Logger("RequestList")
        #self.log.setLevel(logging.DEBUG)
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
        self.log.info(RequestList.timestamp, "first_element", None, None, "The first item of the RequestList is: ", str(self.items[0]))
        return self.items[0]


    def remove(self):
        self.log.info(RequestList.timestamp, "remove", None, None,"Pop the first item in the RequestList is: ", str(self.items[0]))
        return self.items.pop(0)


    def is_empty(self):
        self.log.info(RequestList.timestamp, "is_empty", None, None, "Tell the RequestList is empty or not")
        return len(self.items) == 0


    def __len__(self):
        self.log.info(RequestList.timestamp, "__len__", None, None,"The length of the RequestList")
        return len(self.items)


    def add(self, item):
        self.log.info(RequestList.timestamp, "add", None, None, "Add request into RequestList")
        self.items.append(item)
