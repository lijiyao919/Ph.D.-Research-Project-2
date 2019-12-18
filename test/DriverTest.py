import unittest
from src.Driver.Driver import Driver
from src.Rider.Rider import Rider
from src.Configure.Config import *

class DriverTest(unittest.TestCase):

    def testConstructor(self):
        d1 = Driver("V0", 23)
        self.assertEqual("V0", d1.getID())
        self.assertEqual(23, d1.getPos())
        self.assertEqual(IDLE, d1.getStatus())
        self.assertEqual(0, d1.getTripEffort())
        self.assertEqual(0, d1.getTripProfit())
        self.assertEqual(0, d1.getIdleTime())
        self.assertEqual("{V0, 23, idle, 0, 0, Riders: [], Route: []}", str(d1))

    def testAddRidersIntoVehicle(self):
        try:
            d1 = Driver("V0", 23)
            r1 = Rider("R1", 0, 7, 1, 10, 20, 1, 1, 2, 1)  # 0
            r2 = Rider("R2", 0, 7, 3, 10, 20, 1, 1, 2, 1)
            r3 = Rider("R3", 0, 7, 77, 10, 20, 1, 1, 2, 1)
            r4 = Rider("R4", 0, 7, 6, 10, 20, 1, 1, 2, 1)
            riders={"R1":r1, "R2":r2, "R3":r3, "R4":r4}
            d1.setRiders(riders)
            self.assertEqual(r1, d1.getRider("R1"))
            self.assertEqual(r2, d1.getRider("R2"))
            self.assertEqual(r3, d1.getRider("R3"))
            self.assertEqual(r4, d1.getRider("R4"))
            d1.getRider("R5")
            self.fail("Expected exception here.")
        except:
            pass

    def testRemoveRider(self):
        try:
            d1 = Driver("V0", 23)
            r1 = Rider("R1", 0, 7, 1, 10, 20, 1, 1, 2, 1)  # 0
            riders={"R1":r1}
            d1.setRiders(riders)

            d1.removeRider("R1")
            self.assertEqual("[]", d1.showRidersOnBoard())
            d1.removeRider("R2")
            self.fail("Expected exception here.")
        except:
            pass

    def testCalcTripRouteSuccess(self):
        d1 = Driver("V0", 23)
        r1 = Rider("R1", 0, 7, 1, 10, 20, 1, 1, 2, 1)  # 0
        r2 = Rider("R2", 0, 7, 3, 10, 20, 1, 1, 2, 1)
        r3 = Rider("R3", 0, 7, 77, 10, 20, 1, 1, 2, 1)
        r4 = Rider("R4", 0, 7, 6, 10, 20, 1, 1, 2, 1)
        riders = {"R1": r1, "R2": r2, "R3": r3, "R4": r4}
        d1.setRiders(riders)

        d1.calcTripRoute()
        self.assertEqual("[7, 6, 3, 77, 1]", d1.showTripRoute())
        try:
            elem1 = d1.popTripRoute()
            self.assertEqual(7, elem1.getZoneID())
            self.assertEqual(PICKUP, elem1.getEvent())
            self.assertEqual(None, elem1.getRiderID())
            elem2 = d1.popTripRoute()
            self.assertEqual(6, elem2.getZoneID())
            self.assertEqual(DROPOFF, elem2.getEvent())
            self.assertEqual("R4", elem2.getRiderID())
            elem3 = d1.popTripRoute()
            self.assertEqual(3, elem3.getZoneID())
            self.assertEqual(DROPOFF, elem3.getEvent())
            self.assertEqual("R2", elem3.getRiderID())
            elem4 = d1.popTripRoute()
            self.assertEqual(77, elem4.getZoneID())
            self.assertEqual(DROPOFF, elem4.getEvent())
            self.assertEqual("R3", elem4.getRiderID())
            elem5 = d1.popTripRoute()
            self.assertEqual(1, elem5.getZoneID())
            self.assertEqual(DROPOFF, elem5.getEvent())
            self.assertEqual("R1", elem5.getRiderID())
            elem6 = d1.popTripRoute()
            self.fail("Expected exception here.")
        except:
            pass

    def testCalcTripRouteFailure(self):
        try:
            d1 = Driver("V0", 23)
            d1.calcTripRoute()
            self.fail("Expected exception here.")
        except:
            pass

    def testCalcTripEffortSuccess(self):
        d1 = Driver("V0", 23)
        Driver.timestamp = 20
        r1 = Rider("R1", 0, 7, 1, 10, 20, 1, 1, 2, 1)  # 0
        r2 = Rider("R2", 0, 7, 3, 10, 20, 1, 1, 2, 1)
        r3 = Rider("R3", 0, 7, 77, 10, 20, 1, 1, 2, 1)
        r4 = Rider("R4", 0, 7, 6, 10, 20, 1, 1, 2, 1)
        riders = {"R1": r1, "R2": r2, "R3": r3, "R4": r4}
        d1.setRiders(riders)
        d1.calcTripRoute()
        d1.calcTripEffort()

        elem1 = d1.popTripRoute()
        self.assertEqual(22, elem1.getEventTime())

        elem2 = d1.popTripRoute()
        self.assertEqual(23, elem2.getEventTime())
        rider1 = d1.getRider(elem2.getRiderID())
        self.assertEqual(23, rider1.getArrivalTimestamp())
        self.assertEqual(2, rider1.getDetourTime())

        elem3 = d1.popTripRoute()
        self.assertEqual(24, elem3.getEventTime())
        rider2 = d1.getRider(elem3.getRiderID())
        self.assertEqual(24, rider2.getArrivalTimestamp())
        self.assertEqual(2, rider2.getDetourTime())

        elem4 = d1.popTripRoute()
        self.assertEqual(25, elem4.getEventTime())
        rider3 = d1.getRider(elem4.getRiderID())
        self.assertEqual(25, rider3.getArrivalTimestamp())
        self.assertEqual(2, rider3.getDetourTime())

        elem5 = d1.popTripRoute()
        self.assertEqual(26, elem5.getEventTime())
        rider4 = d1.getRider(elem5.getRiderID())
        self.assertEqual(26, rider4.getArrivalTimestamp())
        self.assertEqual(2, rider4.getDetourTime())

        self.assertEqual(6, d1.getTripEffort())

    def testCalcTripEffortFailure(self):
        try:
            d1 = Driver("V0", 23)
            d1.calcTripEffort()
            self.fail("Expected exception here.")
        except:
            pass

    def testCalcTripProfitSuccess(self):
        d1 = Driver("V0", 23)
        r1 = Rider("R1", 0, 7, 1, 10, 20, 1, 1, 2, 1)  # 0
        r2 = Rider("R2", 0, 7, 3, 10, 20, 1, 1, 2, 1)
        r3 = Rider("R3", 0, 7, 77, 10, 20, 1, 1, 2, 1)
        r4 = Rider("R4", 0, 7, 6, 10, 20, 1, 1, 2, 1)
        riders = {"R1": r1, "R2": r2, "R3": r3, "R4": r4}
        d1.setRiders(riders)
        d1.calcTripRoute()
        d1.calcTripEffort()
        r1.calcPrice(4)
        r2.calcPrice(4)
        r3.calcPrice(4)
        r4.calcPrice(4)
        d1.calcTripProfit()
        self.assertAlmostEqual(26.0883, d1.getTripProfit(), delta=0.01)

    def testCalcTripProfitWithWrongPrice(self):
        try:
            d1 = Driver("V0", 23)
            r1 = Rider("R1", 0, 7, 1, 10, 20, 1, 1, 2, 1)  # 0
            r2 = Rider("R2", 0, 7, 3, 10, 20, 1, 1, 2, 1)
            r3 = Rider("R3", 0, 7, 77, 10, 20, 1, 1, 2, 1)
            r4 = Rider("R4", 0, 7, 6, 10, 20, 1, 1, 2, 1)
            riders = {"R1": r1, "R2": r2, "R3": r3, "R4": r4}
            d1.setRiders(riders)
            d1.calcTripRoute()
            d1.calcTripEffort()
            d1.calcTripProfit()
            self.fail("Expected Exception here.")
        except:
            pass

    def testCalcTripProfitWithNoRider(self):
        try:
            d1 = Driver("V0", 23)
            d1.calcTripProfit()
            self.fail("Expected Exception here.")
        except:
            pass

    def testNotifyRiderPrice(self):
        d1 = Driver("V0", 23)
        r1 = Rider("R1", 0, 7, 1, 10, 20, 1, 1, 2, 1)  # 0
        r2 = Rider("R2", 0, 7, 3, 10, 20, 1, 1, 2, 1)
        r3 = Rider("R3", 0, 7, 77, 10, 20, 1, 1, 2, 1)
        r4 = Rider("R4", 0, 7, 6, 10, 20, 1, 1, 2, 1)
        riders = {"R1": r1, "R2": r2, "R3": r3, "R4": r4}
        d1.setRiders(riders)
        d1.calcTripRoute()
        d1.calcTripEffort()
        d1.notifyRiderPrice()
        self.assertAlmostEqual(7.87208, r1.getPrice(), delta=0.01)
        self.assertAlmostEqual(7.87208, r2.getPrice(), delta=0.01)
        self.assertAlmostEqual(7.87208, r3.getPrice(), delta=0.01)
        self.assertAlmostEqual(7.87208, r4.getPrice(), delta=0.01)



    def testSetStatus(self):
        d1 = Driver("V0", 23)
        d1.setStatus(INSERVICE)
        self.assertEqual("inservice", d1.getStatus())

    def testTickWaitTime(self):
        d1 = Driver("V0", 23)
        d1.tickIdleTime()
        self.assertEqual(1, d1.getIdleTime())
