import unittest
from src.Rider import Rider


class RiderTest(unittest.TestCase):
    def testInvalidConstruction(self):
        r1 = Rider("R1", 0, 7, 6, 10, 20, 1, 1, 2, 1)
        self.assertEqual("R1", r1.getID())
        self.assertEqual(0, r1.getRequestTimeStamp())
        self.assertEqual(7, r1.getSrcZone())
        self.assertEqual(6, r1.getDestZone())
        self.assertEqual(20, r1.getPatience())
        self.assertEqual(1, r1.getShortestTime())
        self.assertEqual("waiting", r1.getStatus())
        self.assertEqual(0, r1.getWaitTime())
        self.assertEqual(0, r1.getTravelTime())
        self.assertEqual(10, r1.getPrice())
        self.assertEqual(0, r1.getSat())
        print(r1)

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


    def testTickWaitTimeSuccess(self):
        r0 = Rider("R0", 0, 8, 24, 7.75, 20, -87.6333, 41.8996, -87.6764, 41.9012)
        r0.tickWaitTime()
        self.assertEqual(1, r0.getWaitTime())

    def testTravelTimeSuccess(self):
        r0 = Rider("R0", 0, 8, 24, 7.75, 20, -87.6333, 41.8996, -87.6764, 41.9012)
        r0.setTravelTime(5)
        self.assertEqual(5, r0.getTravelTime())
        self.assertEqual(4, r0.getDetourTime())

    def testCalcPriceSuccess(self):
        r0 = Rider("R0", 0, 8, 24, 7.75, 20, -87.6333, 41.8996, -87.6764, 41.9012)
        r0.setTravelTime(5)
        r0.calcPrice(1)
        self.assertAlmostEqual(6.0914, r0.getPrice(), delta=0.01)

        r0 = Rider("R0", 0, 8, 24, 7.75, 20, -87.6333, 41.8996, -87.6764, 41.9012)
        r0.setTravelTime(5)
        r0.calcPrice(2)
        self.assertAlmostEqual(5.901, r0.getPrice(), delta=0.01)

        r0 = Rider("R0", 0, 8, 24, 7.75, 20, -87.6333, 41.8996, -87.6764, 41.9012)
        r0.setTravelTime(5)
        r0.calcPrice(3)
        self.assertAlmostEqual(5.7107, r0.getPrice(), delta=0.01)

        r0 = Rider("R0", 0, 8, 24, 7.75, 20, -87.6333, 41.8996, -87.6764, 41.9012)
        r0.setTravelTime(5)
        r0.calcPrice(4)
        self.assertAlmostEqual(5.52, r0.getPrice(), delta=0.01)

    def testCalcSat(self):
        r0 = Rider("R0", 0, 8, 24, 7.75, 20, -87.6333, 41.8996, -87.6764, 41.9012)
        r0.setTravelTime(5)
        r0.calcPrice(1)
        r0.calcSat()
        self.assertAlmostEqual(-11.496, r0.getSat(), delta=0.01)

        r0.calcPrice(2)
        r0.calcSat()
        self.assertAlmostEqual(-7.52, r0.getSat(), delta=0.01)

        r0.calcPrice(3)
        r0.calcSat()
        self.assertAlmostEqual(-2.23, r0.getSat(), delta=0.01)

        r0.calcPrice(4)
        r0.calcSat()
        self.assertAlmostEqual(4.82, r0.getSat(), delta=0.01)




if __name__ == '__main__':
    unittest.main()