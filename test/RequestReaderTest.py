import unittest
from src.Import.RequestList import RequestList
from src.Import.ImportData import *

class RequestReaderTest(unittest.TestCase):
    def testCreateRiderRequest(self):
        r1 = Rider("R1", 0, 7, 6, 10, 20, 1, 1, 2, 1)
        reuqest = RiderRequest(0, "RiderRequest", r1)
        print(reuqest)

    def testCreateDriverRequest(self):
        d1 = Driver("V0", 23)
        reuqest = DriverRequest(0, "DriverRequest", d1)
        print(reuqest)

    def testReadRequestFromCsv(self):
        rider_list = RequestList()
        driver_list = RequestList()

        readRequestFromCsv(driver_list, rider_list)

        print(driver_list)
        print(rider_list)

