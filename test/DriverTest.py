import unittest
from src.Driver import Driver
from src.Rider import Rider
from src.Config import *

class RiderTest(unittest.TestCase):
    def testValidConstruction(self):
        d1 = Driver("V0", 23)
        self.assertEqual("V0", d1.getID())
        self.assertEqual(23, d1.getPos())
        self.assertEqual("idle", d1.getStatus())
        self.assertEqual(0, d1.getTripEffort())
        self.assertEqual(0, len(d1.getRoute()))
        self.assertEqual(0, d1.getProfit())
        print(d1)

    def testSetRoute(self):
        d1 = Driver("V0", 23)
        r1 = Rider("R1", 0, 7, 1, 10, 20, 1, 1, 2, 1)  # 0
        r2 = Rider("R2", 0, 7, 3, 10, 20, 1, 1, 2, 1)
        r3 = Rider("R3", 0, 7, 77, 10, 20, 1, 1, 2, 1)
        r4 = Rider("R4", 0, 7, 6, 10, 20, 1, 1, 2, 1)

        route = [("R1", r1), ("R2", r2), ("R3", r3), ("R4", r4)]
        d1.setRoute(route)
        self.assertEqual(4, len(d1.getRoute()))
        print(d1)

    def testSetStatus(self):
        d1 = Driver("V0", 23)
        d1.setStatus(INSERVICE)
        self.assertEqual("inservice", d1.getStatus())

    def testSetTripEffort(self):
        d1 = Driver("V0", 23)
        d1.setTripEffort(5)
        self.assertEqual(5, d1.getTripEffort())

    def testCalcPrice(self):
        d1 = Driver("V0", 23)
        r0 = Rider("R0", 0, 8, 24, 7.75, 20, -87.6333, 41.8996, -87.6764, 41.9012)
        r1 = Rider("R1", 0, 8, 32, 6, 20, -87.6495, 41.9227, -87.656, 41.9442)
        r0.setTravelTime(2);
        r0.calcPrice(2)
        #print(r0.getPrice())
        r1.setTravelTime(1)
        r1.calcPrice(2)
        #print(r1.getPrice())
        d1.setRoute([("R0", r0), ("R1", r1)])
        d1.setTripEffort(2)
        d1.calcTripProfit()
        self.assertAlmostEqual(10.64, d1.getProfit(), delta=0.1)

    def testSetAcceptTime(self):
        d1=Driver("V1", 23)
        d1.setTripStartTime(10)
        self.assertEqual(10, d1.getTripStartTime())

    def testTickIdleTime(self):
        d1=Driver("V1", 23)
        d1.tickIdleTime()
        self.assertEqual(1,d1.getIdleTime())