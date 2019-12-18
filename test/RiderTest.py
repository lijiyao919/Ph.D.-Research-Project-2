import unittest
import math
from src.Rider.Rider import Rider
from src.Configure.Config import *

class RiderTest(unittest.TestCase):
    def testConstructor(self):
        r1 = Rider("R1", 0, 7, 6, 10, 20, 1, 1, 2, 1)
        self.assertEqual("R1", r1.getID())
        self.assertEqual(0, r1.getRequestTimeStamp())
        self.assertEqual(7, r1.getSrcZone())
        self.assertEqual(6, r1.getDestZone())
        self.assertEqual(10, r1.getDefaultPrice())
        self.assertEqual(math.inf, r1.getPrice())
        self.assertEqual(20, r1.getPatience())
        self.assertEqual(1, r1.getShortestTime())
        self.assertEqual(None, r1.getArrivalTimestamp())
        self.assertEqual(None, r1.getGroupID())
        self.assertEqual("waiting", r1.getStatus())
        self.assertEqual(0, r1.getWaitTime())
        self.assertEqual(-1, r1.getDetourTime())
        self.assertEqual(0, r1.getSat())
        self.assertEqual("{R1, 0, 7, 6, 10, inf, 20, 6, 1, None, None, waiting, 0, -1, 0}", str(r1))


    def testDirID(self):
        r1 = Rider("R1", 0, 7, 6, 10, 20, 1, 1, 2, 1)  #0
        self.assertEqual(6, r1.getDirID())

        r1 = Rider("R1", 0, 7, 6, 10, 20, 1, 1, 2, 2)  #45
        self.assertEqual(7, r1.getDirID())

        r1 = Rider("R1", 0, 7, 6, 10, 20, 1, 1, 1, 2)  #90
        self.assertEqual(9, r1.getDirID())

        r1 = Rider("R1", 0, 7, 6, 10, 20, 1, 1, 0, 2)  #135
        self.assertEqual(10, r1.getDirID())

        r1 = Rider("R1", 0, 7, 6, 10, 20, 1, 1, 0, 1)  #-180
        self.assertEqual(0, r1.getDirID())

        r1 = Rider("R1", 0, 7, 6, 10, 20, 1, 1, 0, 0)  #-135
        self.assertEqual(1, r1.getDirID())

        r1 = Rider("R1", 0, 7, 6, 10, 20, 1, 1, 1, 0)  #-90
        self.assertEqual(3, r1.getDirID())

        r1 = Rider("R1", 0, 7, 6, 10, 20, 1, 1, 2, 0)  #-45
        self.assertEqual(4, r1.getDirID())


    def testTickWaitTime(self):
        r0 = Rider("R0", 0, 8, 24, 7.75, 20, -87.6333, 41.8996, -87.6764, 41.9012)
        r0.tickWaitTime()
        self.assertEqual(1, r0.getWaitTime())

    def testclacDetourTime(self):
        r0 = Rider("R0", 0, 8, 24, 7.75, 20, -87.6333, 41.8996, -87.6764, 41.9012)
        r0.calcDetourTime(5)
        self.assertEqual(4, r0.getDetourTime())

    def testCalcPriceSuccess(self):
        r0 = Rider("R0", 0, 8, 24, 7.75, 20, -87.6333, 41.8996, -87.6764, 41.9012)
        r0.calcDetourTime(5)
        r0.calcPrice(1)
        self.assertAlmostEqual(6.0914, r0.getPrice(), delta=0.01)

        r0 = Rider("R0", 0, 8, 24, 7.75, 20, -87.6333, 41.8996, -87.6764, 41.9012)
        r0.calcDetourTime(5)
        r0.calcPrice(2)
        self.assertAlmostEqual(5.901, r0.getPrice(), delta=0.01)

        r0 = Rider("R0", 0, 8, 24, 7.75, 20, -87.6333, 41.8996, -87.6764, 41.9012)
        r0.calcDetourTime(5)
        r0.calcPrice(3)
        self.assertAlmostEqual(5.7107, r0.getPrice(), delta=0.01)

        r0 = Rider("R0", 0, 8, 24, 7.75, 20, -87.6333, 41.8996, -87.6764, 41.9012)
        r0.calcDetourTime(5)
        r0.calcPrice(4)
        self.assertAlmostEqual(5.52, r0.getPrice(), delta=0.01)

    def testcalcPriceWithWrongDetourTime(self):
        try:
            r0 = Rider("R0", 0, 8, 24, 7.75, 20, -87.6333, 41.8996, -87.6764, 41.9012)
            r0.calcPrice(4)
            self.fail("Expected exception here.")
        except:
            pass

    def testcalcPriceWithWrongSharedNumber(self):
        try:
            r0 = Rider("R0", 0, 8, 24, 7.75, 20, -87.6333, 41.8996, -87.6764, 41.9012)
            r0.calcDetourTime(5)
            r0.calcPrice(5)
            self.fail("Expected exception here.")
        except:
            pass

    def testCalcSatSuccess(self):
        #without detour time
        r0 = Rider("R0", 0, 8, 24, 7.75, 20, -87.6333, 41.8996, -87.6764, 41.9012)
        r0.calcDetourTime(1)
        r0.calcPrice(1)
        r0.calcSat()
        self.assertAlmostEqual(1.592, r0.getSat(), delta=0.01)

        #with detour time
        r0 = Rider("R0", 0, 8, 24, 7.75, 20, -87.6333, 41.8996, -87.6764, 41.9012)
        r0.calcDetourTime(2)
        r0.calcPrice(1)
        r0.calcSat()
        self.assertAlmostEqual(1.518, r0.getSat(), delta=0.01)

    def testCalcSatWithWrongPrice(self):
        try:
            r0 = Rider("R0", 0, 8, 24, 7.75, 20, -87.6333, 41.8996, -87.6764, 41.9012)
            r0.calcSat()
            self.fail("Expected exception here.")
        except:
            pass

    def testCalcSatWithWrongDetourTime(self):
        try:
            r0 = Rider("R0", 0, 8, 24, 7.75, 20, -87.6333, 41.8996, -87.6764, 41.9012)
            r0.calcDetourTime(1)
            r0.calcSat()
            self.fail("Expected exception here.")
        except:
            pass

    def testSetGroupID(self):
        r0 = Rider("R0", 0, 8, 24, 7.75, 20, -87.6333, 41.8996, -87.6764, 41.9012)
        r0.setGroupID(1)
        self.assertEqual(1, r0.getGroupID())

    def testSetArrivalTimestamp(self):
        r0 = Rider("R0", 0, 8, 24, 7.75, 20, -87.6333, 41.8996, -87.6764, 41.9012)
        r0.setArrivalTimestamp(10)
        self.assertEqual(10, r0.getArrivalTimestamp())

    def testSetStatus(self):
        r0 = Rider("R0", 0, 8, 24, 7.75, 20, -87.6333, 41.8996, -87.6764, 41.9012)
        r0.setStatus(SERVING)
        self.assertEqual(SERVING, r0.getStatus())
