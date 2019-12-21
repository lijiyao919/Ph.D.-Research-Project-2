import unittest
from src.Import.RequestList import RequestList
from src.Driver.Driver import Driver
from src.Rider.Rider import Rider

class RequestListTest(unittest.TestCase):
    def testCreateRequestList(self):
        rl = RequestList()
        self.assertEqual("[]", str(rl))
        self.assertEqual(0, len(rl))
        self.assertEqual(True, rl.is_empty())

    def testAddDriver(self):
        d1 = Driver("D1", 2)
        d2 = Driver("D2", 2)
        rl = RequestList()
        rl.add(d1)
        rl.add(d2)
        self.assertEqual("[{D1, 2, idle, 0, 0, Riders: [], Route: []}, {D2, 2, idle, 0, 0, Riders: [], Route: []}, ]", str(rl))
        self.assertEqual(2, len(rl))
        self.assertEqual(False, rl.is_empty())
        self.assertEqual("{D1, 2, idle, 0, 0, Riders: [], Route: []}", str(rl.first_element()))

    def testRemoveDriver(self):
        d1 = Driver("D1", 2)
        d2 = Driver("D2", 2)
        rl = RequestList()
        rl.add(d1)
        rl.add(d2)

        rl.remove()
        self.assertEqual("[{D2, 2, idle, 0, 0, Riders: [], Route: []}, ]", str(rl))
        self.assertEqual(1, len(rl))
        self.assertEqual(False, rl.is_empty())
        self.assertEqual("{D2, 2, idle, 0, 0, Riders: [], Route: []}", str(rl.first_element()))

        rl.remove()
        self.assertEqual("[]", str(rl))
        self.assertEqual(0, len(rl))
        self.assertEqual(True, rl.is_empty())
        try:
           rl.first_element()
           self.fail("Expected exception here.")
        except:
           pass

    def testAddRider(self):
        r1 = Rider("R1", 0, 1, 6, 10, 20, 1, 1, 2, 1)  # 0
        r2 = Rider("R2", 0, 1, 6, 10, 20, 1, 1, 2, 1)
        rl = RequestList()
        rl.add(r1)
        rl.add(r2)

        self.assertEqual("[{R1, 0, 1, 6, 10, inf, 20, 6, 3, None, None, waiting, 0, -1, 0}, {R2, 0, 1, 6, 10, inf, 20, 6, 3, None, None, waiting, 0, -1, 0}, ]", str(rl))
        self.assertEqual(2, len(rl))
        self.assertEqual(False, rl.is_empty())
        self.assertEqual("{R1, 0, 1, 6, 10, inf, 20, 6, 3, None, None, waiting, 0, -1, 0}", str(rl.first_element()))

    def testRemoveRider(self):
        r1 = Rider("R1", 0, 1, 6, 10, 20, 1, 1, 2, 1)  # 0
        r2 = Rider("R2", 0, 1, 6, 10, 20, 1, 1, 2, 1)
        rl = RequestList()
        rl.add(r1)
        rl.add(r2)

        rl.remove()
        self.assertEqual("[{R2, 0, 1, 6, 10, inf, 20, 6, 3, None, None, waiting, 0, -1, 0}, ]", str(rl))
        self.assertEqual(1, len(rl))
        self.assertEqual(False, rl.is_empty())
        self.assertEqual("{R2, 0, 1, 6, 10, inf, 20, 6, 3, None, None, waiting, 0, -1, 0}", str(rl.first_element()))

        rl.remove()
        self.assertEqual("[]", str(rl))
        self.assertEqual(0, len(rl))
        self.assertEqual(True, rl.is_empty())
        try:
            rl.first_element()
            self.fail("Expected exception here.")
        except:
            pass







