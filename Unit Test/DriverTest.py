import unittest
from Driver import Driver
from Rider import Rider
from Config import *

class RiderTest(unittest.TestCase):
    def testValidConstruction(self):
        d1 = Driver("V0", 23)

        self.assertEqual("V0", d1.getID())
        self.assertEqual(23, d1.getPos())
        self.assertEqual("idle", d1.getStatus())
        self.assertEqual(0, d1.getTripEffort())
        self.assertEqual(0, len(d1.getRiders()))
        self.assertEqual(0, len(d1.getRoute()))
        self.assertEqual(0, d1.getProfit())
        print(d1)

    def testAssignRiders(self):
        d1 = Driver("V0", 23)
        r0 = Rider("R0", 0, 8, 24, 7.75, 20, -87.6333, 41.8996, -87.6764, 41.9012)
        r1 = Rider("R1", 0, 7, 6, 6, 20, -87.6495, 41.9227, -87.656, 41.9442)
        d1.assignRiders([r0, r1])
        self.assertEqual(2, len(d1.getRiders()))
        print(d1)

    def testSetRoute(self):
        d1 = Driver("V0", 23)
        d1.setRoute([7,8])
        self.assertEqual(2, len(d1.getRoute()))
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
        d1.assignRiders([r0, r1])
        d1.setTripEffort(2)
        d1.calcProfit()
        self.assertAlmostEqual(10.64, d1.getProfit(), delta=0.1)