import unittest
from src.Import.ImportData import ImportData
from src.Import.RequestList import RequestList

class ImportDataTest(unittest.TestCase):

    def testImportDriverData(self):
        FILENAME_D = "C:/Users/a02231961/PycharmProjects/Ph.D.-Research-Project-2/data/Chicago_driver_test.csv"
        rl=RequestList()
        ImportData.importDriverData(FILENAME_D, rl)

        self.assertEqual(11, len(rl))
        self.assertEqual("{D0, 50, idle, 0, 0, Riders: [], Route: []}", str(rl.first_element()))

        rl.remove()
        self.assertEqual(10, len(rl))
        self.assertEqual("{D1, 50, idle, 0, 0, Riders: [], Route: []}", str(rl.first_element()))

    def testImportRiderData(self):
        FILENAME_R = "C:/Users/a02231961/PycharmProjects/Ph.D.-Research-Project-2/data/Chicago_rider_test.csv"
        rl = RequestList()
        ImportData.importRiderData(FILENAME_R, rl)

        self.assertEqual(29, len(rl))
        self.assertEqual("{R0, 0.0, 50, 55, 5.0, inf, 7, 4, 2, None, None, waiting, 0, -1, 0}", str(rl.first_element()))

        rl.remove()
        self.assertEqual(28, len(rl))
        self.assertEqual("{R1, 0.0, 50, 55, 5.0, inf, 7, 4, 2, None, None, waiting, 0, -1, 0}", str(rl.first_element()))