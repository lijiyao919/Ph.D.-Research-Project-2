import unittest

from src.Dispatcher.DriverStatusTracker import DriverStatusTracker
from src.Dispatcher.RiderStatusTracker import RiderStatusTracker
from src.Rider.Rider import Rider
from src.Driver.Driver import Driver
from src.Dispatcher.Dispatcher import Dispatcher
from src.Configure.Config import *

class DispatcherTest(unittest.TestCase):
    def testConstructor(self):
        dispatcher = Dispatcher()

        #driver dict
        for zone_id in range(1, 78):
            self.assertEqual(None, dispatcher.getDriverFromDriverDict(zone_id, None))
        self.assertEqual("1: {}", dispatcher.showDriverDict(1))
        self.assertEqual("20: {}", dispatcher.showDriverDict(20))
        self.assertEqual("77: {}", dispatcher.showDriverDict(77))
        self.assertEqual(0, dispatcher.getDriverNumberOfZone(1))
        self.assertEqual(0, dispatcher.getDriverNumberOfZone(20))
        self.assertEqual(0, dispatcher.getDriverNumberOfZone(77))
        self.assertEqual(0, dispatcher.countTotalDriverNumber())

        #wait dict
        for zone_id in range(1, 78):
            for dir_id in range(0, 12):
                self.assertEqual(None, dispatcher.getGroupFromWaitDict(zone_id, dir_id, None))
        self.assertEqual("1: {0: {}, 1: {}, 2: {}, 3: {}, 4: {}, 5: {}, 6: {}, 7: {}, 8: {}, 9: {}, 10: {}, 11: {}, }", dispatcher.showRiderWaitDict(1))
        self.assertEqual(0, dispatcher.getRequestNumberOfZone(1))
        self.assertEqual(0, dispatcher.getRequestNumberOfZone(20))
        self.assertEqual(0, dispatcher.getRequestNumberOfZone(77))
        self.assertEqual(0, dispatcher.countRiderNumberInWaitDict())

        #serve dict
        self.assertEqual(None, dispatcher.getRiderFromServedDict(None))
        self.assertEqual("{}", dispatcher.showRiderServedDict())
        self.assertEqual(0, dispatcher.countRiderNumberInServeDict())

        #finish dict
        self.assertEqual(None, dispatcher.getRiderFromFinishedDict(None))
        self.assertEqual("{}", dispatcher.showRiderFinishedDict())
        self.assertEqual(0, dispatcher.countRiderNumberInFinishDict())

        #cancel dict
        self.assertEqual(None, dispatcher.getRiderFromCanceledDict(None))
        self.assertEqual("{}", dispatcher.showRiderCanceledDict())
        self.assertEqual(0, dispatcher.countRiderNumberInCancelDict())
        self.assertEqual(0, dispatcher.countCurrentTotalRiderNumber())

    def testHandleDriverIntoDictSuccess(self):
        d1 = Driver("D1", 1)
        d2 = Driver("D2", 20)
        d3 = Driver("D3", 77)
        d4 = Driver("D4", 77)

        dispatcher = Dispatcher()
        dispatcher.handleDriverIntoDict(d1)
        dispatcher.handleDriverIntoDict(d2)
        dispatcher.handleDriverIntoDict(d3)
        dispatcher.handleDriverIntoDict(d4)

        self.assertEqual("1: {D1, }", dispatcher.showDriverDict(1))
        self.assertEqual(d1, dispatcher.getDriverFromDriverDict(1, "D1"))
        self.assertEqual(1, dispatcher.getDriverNumberOfZone(1))
        self.assertEqual("20: {D2, }", dispatcher.showDriverDict(20))
        self.assertEqual(d2, dispatcher.getDriverFromDriverDict(20, "D2"))
        self.assertEqual(1, dispatcher.getDriverNumberOfZone(20))
        self.assertEqual("77: {D3, D4, }", dispatcher.showDriverDict(77))
        self.assertEqual(d3, dispatcher.getDriverFromDriverDict(77, "D3"))
        self.assertEqual(d4, dispatcher.getDriverFromDriverDict(77, "D4"))
        self.assertEqual(2, dispatcher.getDriverNumberOfZone(77))
        self.assertEqual(4, dispatcher.countTotalDriverNumber())
        self.assertEqual(0, dispatcher.countCurrentTotalRiderNumber())

    def testHandleDriverIntoDictNotDriver(self):
        try:
            r1 = Rider("R1", 0, 1, 6, 10, 20, 1, 1, 2, 1)  # 0
            dispatcher = Dispatcher()
            dispatcher.handleDriverIntoDict(r1)
            self.fail("Expected exception here.")
        except:
            pass

    def testHandleDriverIntoDictWithSameDriver(self):
        try:
            d1 = Driver("D1", 7)
            d2 = Driver("D1", 7)
            dispatcher = Dispatcher()
            dispatcher.handleDriverIntoDict(d1)
            dispatcher.handleDriverIntoDict(d2)
            self.fail("Expected exception here.")
        except:
            pass

    def testHandleRiderIntoDictSuccess(self):
        r1 = Rider("R1", 0, 1, 6, 10, 20, 1, 1, 2, 1)  # 0
        r2 = Rider("R2", 0, 1, 6, 10, 20, 1, 1, 2, 1)
        r3 = Rider("R3", 0, 1, 6, 10, 20, 1, 1, 2, 1)
        r4 = Rider("R4", 0, 1, 6, 10, 20, 1, 1, 2, 1)
        r5 = Rider("R5", 0, 1, 6, 10, 20, 1, 1, 2, 1)
        r6 = Rider("R6", 0, 1, 6, 10, 20, 1, 1, 2, 1)
        r7 = Rider("R7", 0, 1, 6, 10, 20, 1, 1, 2, 1)
        r8 = Rider("R8", 0, 1, 6, 10, 20, 1, 1, 2, 1)
        r9 = Rider("R9", 0, 1, 6, 10, 20, 1, 1, 2, 1)

        dispatcher = Dispatcher()
        dispatcher.handleRiderIntoDict(r1)
        dispatcher.handleRiderIntoDict(r2)
        dispatcher.handleRiderIntoDict(r3)
        dispatcher.handleRiderIntoDict(r4)
        dispatcher.handleRiderIntoDict(r5)
        dispatcher.handleRiderIntoDict(r6)
        dispatcher.handleRiderIntoDict(r7)
        dispatcher.handleRiderIntoDict(r8)
        dispatcher.handleRiderIntoDict(r9)

        self.assertEqual(9, dispatcher.getRequestNumberOfZone(1))
        self.assertEqual("1: {0: {}, 1: {}, 2: {}, 3: {}, 4: {}, 5: {}, 6: {1: [R1, R2, R3, R4, ], 2: [R5, R6, R7, R8, ], 3: [R9, ], }, 7: {}, 8: {}, 9: {}, 10: {}, 11: {}, }", dispatcher.showRiderWaitDict(1))
        self.assertEqual(9, dispatcher.countRiderNumberInWaitDict())

        r10 = Rider("R10", 0, 7, 6, 10, 20, 1, 1, 1, 2)  # 90
        dispatcher.handleRiderIntoDict(r10)
        self.assertEqual(1, dispatcher.getRequestNumberOfZone(7))
        self.assertEqual("7: {0: {}, 1: {}, 2: {}, 3: {}, 4: {}, 5: {}, 6: {}, 7: {}, 8: {}, 9: {1: [R10, ], }, 10: {}, 11: {}, }", dispatcher.showRiderWaitDict(7))
        self.assertEqual(10, dispatcher.countRiderNumberInWaitDict())

        r16 = Rider("R16", 0, 1, 6, 10, 20, 1, 1, 2, 1) #0
        r17 = Rider("R17", 0, 1, 6, 10, 20, 1, 1, 2, 1)
        r18 = Rider("R18", 0, 1, 6, 10, 20, 1, 1, 2, 1)
        r19 = Rider("R19", 0, 1, 6, 10, 20, 1, 1, 2, 1)
        dispatcher.handleRiderIntoDict(r16)
        dispatcher.handleRiderIntoDict(r17)
        dispatcher.handleRiderIntoDict(r18)
        dispatcher.handleRiderIntoDict(r19)
        self.assertEqual(13, dispatcher.getRequestNumberOfZone(1))
        self.assertEqual("1: {0: {}, 1: {}, 2: {}, 3: {}, 4: {}, 5: {}, 6: {1: [R1, R2, R3, R4, ], 2: [R5, R6, R7, R8, ], 3: [R16, R17, R18, R9, ], 4: [R19, ], }, 7: {}, 8: {}, 9: {}, 10: {}, 11: {}, }",
                          dispatcher.showRiderWaitDict(1))
        self.assertEqual(14, dispatcher.countRiderNumberInWaitDict())
        self.assertEqual(14, dispatcher.countCurrentTotalRiderNumber())

    def testHandleRiderIntoDictFailure(self):
        try:
            d1 = Driver("D1", 7)
            dispatcher = Dispatcher()
            dispatcher.handleRiderIntoDict(d1)
            self.fail("Expected exception here.")
        except:
            pass

    def testMatchRidertoDriver(self):
        r1 = Rider("R1", 0, 1, 6, 10, 20, 1, 1, 2, 1)  # 0
        r2 = Rider("R2", 0, 1, 6, 10, 20, 1, 1, 2, 1)
        r5 = Rider("R5", 0, 1, 6, 10, 20, 1, 1, 2, 1)
        r6 = Rider("R6", 0, 1, 6, 10, 20, 1, 1, 2, 1)
        r8 = Rider("R8", 0, 1, 6, 10, 20, 1, 1, 2, 1)
        r9 = Rider("R9", 0, 1, 7, 10, 20, 1, 1, 2, 1)
        r3 = Rider("R3", 0, 1, 4, 10, 20, 1, 1, 1, 2)  #90
        r4 = Rider("R4", 0, 1, 6, 10, 20, 1, 1, 1, 2)
        r7 = Rider("R7", 0, 1, 8, 10, 20, 1, 1, 1, 2)
        r10 = Rider("R10", 0, 1, 6, 10, 20, 1, 1, 2, 2) #45
        r11 = Rider("R11", 0, 1, 28, 10, 20, 1, 1, 2, 2)
        r12 = Rider("R12", 0, 1, 8, 10, 20, 1, 1, 2, 2)
        r13 = Rider("R13", 0, 1, 6, 10, 20, 1, 1, 0, 2)  # 135
        r14 = Rider("R14", 0, 1, 6, 10, 20, 1, 1, 0, 1)  #-180
        r15 = Rider("R15", 0, 1, 6, 10, 20, 1, 1, 1, 0)  # -90

        d1 = Driver("D1", 2)
        d2 = Driver("D2", 2)
        d3 = Driver("D3", 2)
        d4 = Driver("D4", 1)
        d5 = Driver("D5", 1)
        d6 = Driver("D6", 77)

        dispatcher = Dispatcher()
        Dispatcher.timestamp = 0
        Driver.timestamp = 0
        Rider.timestamp = 0

        dispatcher.handleDriverIntoDict(d1)
        dispatcher.handleDriverIntoDict(d2)
        dispatcher.handleDriverIntoDict(d3)
        dispatcher.handleDriverIntoDict(d4)
        dispatcher.handleDriverIntoDict(d5)
        dispatcher.handleDriverIntoDict(d6)
        dispatcher.handleRiderIntoDict(r1)
        dispatcher.handleRiderIntoDict(r2)
        dispatcher.handleRiderIntoDict(r3)
        dispatcher.handleRiderIntoDict(r4)
        dispatcher.handleRiderIntoDict(r5)
        dispatcher.handleRiderIntoDict(r6)
        dispatcher.handleRiderIntoDict(r7)
        dispatcher.handleRiderIntoDict(r8)
        dispatcher.handleRiderIntoDict(r9)
        dispatcher.handleRiderIntoDict(r10)
        dispatcher.handleRiderIntoDict(r11)
        dispatcher.handleRiderIntoDict(r12)
        dispatcher.handleRiderIntoDict(r13)
        dispatcher.handleRiderIntoDict(r14)
        dispatcher.handleRiderIntoDict(r15)

        print(dispatcher.showRiderWaitDict(1))
        dispatcher.matchRidertoDriver()
        print(dispatcher.showRiderWaitDict(1))

        #observer dispatch
        self.assertEqual("{R1, R10, R11, R12, R14, R15, R2, R3, R4, R5, R6, R7, R8, R9, }", dispatcher.showRiderServedDict())
        self.assertEqual("R13", dispatcher.getRiderFromWaitDict(1, 10, 1, "R13").getID())
        self.assertEqual(6, dispatcher.countTotalDriverNumber())
        self.assertEqual(1, dispatcher.countRiderNumberInWaitDict())
        self.assertEqual(14, dispatcher.countRiderNumberInServeDict())

        # observer rider
        self.assertEqual(SERVING, dispatcher.getRiderFromServedDict("R14").getStatus())
        self.assertEqual(1, dispatcher.getRiderFromServedDict("R14").getDetourTime())
        self.assertAlmostEqual(9.132, dispatcher.getRiderFromServedDict("R14").getPrice(), delta=0.01)
        self.assertAlmostEqual(2.452, dispatcher.getRiderFromServedDict("R14").getSat(), delta=0.01)
        self.assertEqual(4, dispatcher.getRiderFromServedDict("R14").getArrivalTimestamp())

        self.assertEqual(SERVING, dispatcher.getRiderFromServedDict("R15").getStatus())
        self.assertEqual(0, dispatcher.getRiderFromServedDict("R15").getDetourTime())
        self.assertAlmostEqual(9.6, dispatcher.getRiderFromServedDict("R15").getPrice(), delta=0.01)
        self.assertAlmostEqual(1.822, dispatcher.getRiderFromServedDict("R15").getSat(), delta=0.01)
        self.assertEqual(3, dispatcher.getRiderFromServedDict("R15").getArrivalTimestamp())

        self.assertEqual(SERVING, dispatcher.getRiderFromServedDict("R1").getStatus())
        self.assertEqual(1, dispatcher.getRiderFromServedDict("R1").getDetourTime())
        self.assertAlmostEqual(8.276, dispatcher.getRiderFromServedDict("R1").getPrice(), delta=0.01)
        self.assertAlmostEqual(12.057, dispatcher.getRiderFromServedDict("R1").getSat(), delta=0.01)
        self.assertEqual(4, dispatcher.getRiderFromServedDict("R1").getArrivalTimestamp())

        self.assertEqual(SERVING, dispatcher.getRiderFromServedDict("R2").getStatus())
        self.assertEqual(1, dispatcher.getRiderFromServedDict("R2").getDetourTime())
        self.assertAlmostEqual(8.276, dispatcher.getRiderFromServedDict("R2").getPrice(), delta=0.01)
        self.assertAlmostEqual(12.057, dispatcher.getRiderFromServedDict("R2").getSat(), delta=0.01)
        self.assertEqual(4, dispatcher.getRiderFromServedDict("R2").getArrivalTimestamp())

        self.assertEqual(SERVING, dispatcher.getRiderFromServedDict("R5").getStatus())
        self.assertEqual(1, dispatcher.getRiderFromServedDict("R5").getDetourTime())
        self.assertAlmostEqual(8.276, dispatcher.getRiderFromServedDict("R5").getPrice(), delta=0.01)
        self.assertAlmostEqual(12.057, dispatcher.getRiderFromServedDict("R5").getSat(), delta=0.01)
        self.assertEqual(4, dispatcher.getRiderFromServedDict("R5").getArrivalTimestamp())

        self.assertEqual(SERVING, dispatcher.getRiderFromServedDict("R6").getStatus())
        self.assertEqual(1, dispatcher.getRiderFromServedDict("R6").getDetourTime())
        self.assertAlmostEqual(8.276, dispatcher.getRiderFromServedDict("R6").getPrice(), delta=0.01)
        self.assertAlmostEqual(12.057, dispatcher.getRiderFromServedDict("R6").getSat(), delta=0.01)
        self.assertEqual(4, dispatcher.getRiderFromServedDict("R6").getArrivalTimestamp())

        self.assertEqual(SERVING, dispatcher.getRiderFromServedDict("R8").getStatus())
        self.assertEqual(0, dispatcher.getRiderFromServedDict("R8").getDetourTime())
        self.assertAlmostEqual(9.3, dispatcher.getRiderFromServedDict("R8").getPrice(), delta=0.01)
        self.assertAlmostEqual(2.858, dispatcher.getRiderFromServedDict("R8").getSat(), delta=0.01)
        self.assertEqual(3, dispatcher.getRiderFromServedDict("R8").getArrivalTimestamp())

        self.assertEqual(SERVING, dispatcher.getRiderFromServedDict("R9").getStatus())
        self.assertEqual(0, dispatcher.getRiderFromServedDict("R9").getDetourTime())
        self.assertAlmostEqual(9.3, dispatcher.getRiderFromServedDict("R9").getPrice(), delta=0.01)
        self.assertAlmostEqual(2.858, dispatcher.getRiderFromServedDict("R9").getSat(), delta=0.01)
        self.assertEqual(4, dispatcher.getRiderFromServedDict("R9").getArrivalTimestamp())

        self.assertEqual(SERVING, dispatcher.getRiderFromServedDict("R10").getStatus())
        self.assertEqual(1, dispatcher.getRiderFromServedDict("R10").getDetourTime())
        self.assertAlmostEqual(8.561, dispatcher.getRiderFromServedDict("R10").getPrice(), delta=0.01)
        self.assertAlmostEqual(7.432, dispatcher.getRiderFromServedDict("R10").getSat(), delta=0.01)
        self.assertEqual(4, dispatcher.getRiderFromServedDict("R10").getArrivalTimestamp())

        self.assertEqual(SERVING, dispatcher.getRiderFromServedDict("R11").getStatus())
        self.assertEqual(1, dispatcher.getRiderFromServedDict("R11").getDetourTime())
        self.assertAlmostEqual(8.561, dispatcher.getRiderFromServedDict("R11").getPrice(), delta=0.01)
        self.assertAlmostEqual(7.432, dispatcher.getRiderFromServedDict("R11").getSat(), delta=0.01)
        self.assertEqual(7, dispatcher.getRiderFromServedDict("R11").getArrivalTimestamp())

        self.assertEqual(SERVING, dispatcher.getRiderFromServedDict("R12").getStatus())
        self.assertEqual(1, dispatcher.getRiderFromServedDict("R12").getDetourTime())
        self.assertAlmostEqual(8.561, dispatcher.getRiderFromServedDict("R12").getPrice(), delta=0.01)
        self.assertAlmostEqual(7.432, dispatcher.getRiderFromServedDict("R12").getSat(), delta=0.01)
        self.assertEqual(6, dispatcher.getRiderFromServedDict("R12").getArrivalTimestamp())

        self.assertEqual(SERVING, dispatcher.getRiderFromServedDict("R3").getStatus())
        self.assertEqual(1, dispatcher.getRiderFromServedDict("R3").getDetourTime())
        self.assertAlmostEqual(8.561, dispatcher.getRiderFromServedDict("R3").getPrice(), delta=0.01)
        self.assertAlmostEqual(7.432, dispatcher.getRiderFromServedDict("R3").getSat(), delta=0.01)
        self.assertEqual(3, dispatcher.getRiderFromServedDict("R3").getArrivalTimestamp())

        self.assertEqual(SERVING, dispatcher.getRiderFromServedDict("R4").getStatus())
        self.assertEqual(1, dispatcher.getRiderFromServedDict("R4").getDetourTime())
        self.assertAlmostEqual(8.561, dispatcher.getRiderFromServedDict("R4").getPrice(), delta=0.01)
        self.assertAlmostEqual(7.432, dispatcher.getRiderFromServedDict("R4").getSat(), delta=0.01)
        self.assertEqual(4, dispatcher.getRiderFromServedDict("R4").getArrivalTimestamp())

        self.assertEqual(SERVING, dispatcher.getRiderFromServedDict("R7").getStatus())
        self.assertEqual(1, dispatcher.getRiderFromServedDict("R7").getDetourTime())
        self.assertAlmostEqual(8.561, dispatcher.getRiderFromServedDict("R7").getPrice(), delta=0.01)
        self.assertAlmostEqual(7.432, dispatcher.getRiderFromServedDict("R7").getSat(), delta=0.01)
        self.assertEqual(6, dispatcher.getRiderFromServedDict("R7").getArrivalTimestamp())

        self.assertEqual(0, dispatcher.calcAverageWaitTimeOfRiders())
        self.assertAlmostEqual(0.786, dispatcher.calcAverageDetourTimeOfRiders(), delta=0.01)
        self.assertAlmostEqual(0, dispatcher.calcAverageWaitTimeOfRiders())
        self.assertEqual(10, dispatcher.calcAverageDefaultFareRiders())
        self.assertAlmostEqual(8.7, dispatcher.calcAverageFareOfRiders(),delta=0.01)
        self.assertAlmostEqual(7.343, dispatcher.calcAverageSatOfRiders(), delta=0.01)

        #observe driver
        self.assertEqual("[R14]", dispatcher.getDriverFromDriverDict(2, "D1").showRidersOnBoard())
        self.assertEqual("[1, 6]", dispatcher.getDriverFromDriverDict(2, "D1").showTripRoute())
        self.assertEqual(INSERVICE, dispatcher.getDriverFromDriverDict(2,"D1").getStatus())
        self.assertEqual(4, dispatcher.getDriverFromDriverDict(2,"D1").getTripEffort())
        self.assertAlmostEqual(5.532, dispatcher.getDriverFromDriverDict(2, "D1").getTripProfit(), delta=0.01)

        self.assertEqual("[R15]", dispatcher.getDriverFromDriverDict(1, "D4").showRidersOnBoard())
        self.assertEqual("[1, 6]", dispatcher.getDriverFromDriverDict(1, "D4").showTripRoute())
        self.assertEqual(INSERVICE, dispatcher.getDriverFromDriverDict(1, "D4").getStatus())
        self.assertEqual(3, dispatcher.getDriverFromDriverDict(1, "D4").getTripEffort())
        self.assertAlmostEqual(6.9, dispatcher.getDriverFromDriverDict(1, "D4").getTripProfit(), delta=0.01)

        self.assertEqual("[R1, R2, R5, R6]", dispatcher.getDriverFromDriverDict(2, "D2").showRidersOnBoard())
        self.assertEqual("[1, 6, 6, 6, 6]", dispatcher.getDriverFromDriverDict(2, "D2").showTripRoute())
        self.assertEqual(INSERVICE, dispatcher.getDriverFromDriverDict(2, "D2").getStatus())
        self.assertEqual(4, dispatcher.getDriverFromDriverDict(2, "D2").getTripEffort())
        self.assertAlmostEqual(29.503, dispatcher.getDriverFromDriverDict(2, "D2").getTripProfit(), delta=0.01)

        self.assertEqual("[R8, R9]", dispatcher.getDriverFromDriverDict(1, "D5").showRidersOnBoard())
        self.assertEqual("[1, 6, 7]", dispatcher.getDriverFromDriverDict(1, "D5").showTripRoute())
        self.assertEqual(INSERVICE, dispatcher.getDriverFromDriverDict(1, "D5").getStatus())
        self.assertEqual(4, dispatcher.getDriverFromDriverDict(1, "D5").getTripEffort())
        self.assertAlmostEqual(15, dispatcher.getDriverFromDriverDict(1, "D5").getTripProfit(), delta=0.01)

        self.assertEqual("[R10, R11, R12]", dispatcher.getDriverFromDriverDict(2, "D3").showRidersOnBoard())
        self.assertEqual("[1, 6, 8, 28]", dispatcher.getDriverFromDriverDict(2, "D3").showTripRoute())
        self.assertEqual(INSERVICE, dispatcher.getDriverFromDriverDict(2, "D3").getStatus())
        self.assertEqual(7, dispatcher.getDriverFromDriverDict(2, "D3").getTripEffort())
        self.assertAlmostEqual(19.383, dispatcher.getDriverFromDriverDict(2, "D3").getTripProfit(), delta=0.01)

        self.assertEqual("[R3, R4, R7]", dispatcher.getDriverFromDriverDict(77, "D6").showRidersOnBoard())
        self.assertEqual("[1, 4, 6, 8]", dispatcher.getDriverFromDriverDict(77, "D6").showTripRoute())
        self.assertEqual(INSERVICE, dispatcher.getDriverFromDriverDict(77, "D6").getStatus())
        self.assertEqual(6, dispatcher.getDriverFromDriverDict(77, "D6").getTripEffort())
        self.assertAlmostEqual(20.283, dispatcher.getDriverFromDriverDict(77, "D6").getTripProfit(), delta=0.01)
        self.assertEqual(15, dispatcher.countCurrentTotalRiderNumber())
        self.assertAlmostEqual(16.1002, dispatcher.calcAverageProfitOfDrivers(), delta=0.01)
        self.assertAlmostEqual(0, dispatcher.calcAverageIdleTimeOfDrivers(), delta=0.01)

    def testUpdateDriverInDictWhenIdle(self):
        d1 = Driver("D1", 1)
        dispatcher = Dispatcher()

        dispatcher.handleDriverIntoDict(d1)
        dispatcher.updateDriverInDict()
        self.assertEqual(1, d1.getIdleTime())

    def testUpdateDriverInDictWhenInService(self):
        Driver.timestamp = 0
        Rider.timestamp = 0
        Dispatcher.timestamp = 0
        DriverStatusTracker.timestamp = 0

        d1 = Driver("D1", 22)
        r1 = Rider("R1", 0, 7, 1, 10, 20, 1, 1, 2, 1)  # 0
        r2 = Rider("R2", 0, 7, 3, 10, 20, 1, 1, 2, 1)
        r3 = Rider("R3", 0, 7, 6, 10, 20, 1, 1, 2, 1)
        r4 = Rider("R4", 0, 7, 6, 10, 20, 1, 1, 2, 1)

        dispatch = Dispatcher()
        dispatch.handleDriverIntoDict(d1)
        dispatch.handleRiderIntoDict(r1)
        dispatch.handleRiderIntoDict(r2)
        dispatch.handleRiderIntoDict(r3)
        dispatch.handleRiderIntoDict(r4)
        dispatch.matchRidertoDriver()
        dispatch.updateDriverInDict()
        self.assertEqual("[7, 6, 6, 3, 1]", d1.showTripRoute())
        self.assertEqual("[R1, R2, R3, R4]", d1.showRidersOnBoard())

        Driver.timestamp = 1
        Rider.timestamp = 1
        Dispatcher.timestamp = 1
        DriverStatusTracker.timestamp = 1
        dispatch.updateDriverInDict()
        self.assertEqual("[6, 6, 3, 1]", d1.showTripRoute())
        self.assertEqual("[R1, R2, R3, R4]", d1.showRidersOnBoard())
        self.assertEqual("{R1, R2, R3, R4, }", dispatch.showRiderServedDict())

        Driver.timestamp = 2
        Rider.timestamp = 2
        Dispatcher.timestamp = 2
        DriverStatusTracker.timestamp = 2
        dispatch.updateDriverInDict()
        self.assertEqual("[3, 1]", d1.showTripRoute())
        self.assertEqual("[R1, R2]", d1.showRidersOnBoard())
        self.assertEqual(FINISHED, r3.getStatus())
        self.assertEqual(FINISHED, r4.getStatus())
        self.assertEqual("{R1, R2, }", dispatch.showRiderServedDict())
        self.assertEqual("{R3, R4, }", dispatch.showRiderFinishedDict())

        Driver.timestamp = 3
        Rider.timestamp = 3
        Dispatcher.timestamp = 3
        DriverStatusTracker.timestamp = 3
        dispatch.updateDriverInDict()
        self.assertEqual("[1]", d1.showTripRoute())
        self.assertEqual("[R1]", d1.showRidersOnBoard())
        self.assertEqual(FINISHED, r2.getStatus())
        self.assertEqual("{R1, }", dispatch.showRiderServedDict())
        self.assertEqual("{R2, R3, R4, }", dispatch.showRiderFinishedDict())

        Driver.timestamp = 5
        Rider.timestamp = 5
        Dispatcher.timestamp = 5
        DriverStatusTracker.timestamp = 5
        dispatch.updateDriverInDict()
        self.assertEqual("[]", d1.showTripRoute())
        self.assertEqual("[]", d1.showRidersOnBoard())
        self.assertEqual(FINISHED, r1.getStatus())
        self.assertEqual(IDLE, d1.getStatus())
        self.assertEqual("{}", dispatch.showRiderServedDict())
        self.assertEqual("{R1, R2, R3, R4, }", dispatch.showRiderFinishedDict())
        self.assertEqual(1, dispatch.countTotalDriverNumber())
        self.assertEqual(4, dispatch.countCurrentTotalRiderNumber())

    def testUpdateDriverInDictFailure(self):
        try:
            d1=Driver("D1", 22)
            d1.setStatus("ffff")
            dispatch = Dispatcher()
            dispatch.handleDriverIntoDict(d1)
            dispatch.updateDriverInDict()
            self.fail("Expected exception here.")
        except:
            pass

    def testUpdateRidersInWaitDict(self):
        r1 = Rider("R1", 0, 7, 1, 10, 20, 1, 1, 2, 1)
        dispatch = Dispatcher()
        dispatch.handleRiderIntoDict(r1)

        RiderStatusTracker.timestamp = 1
        dispatch.updateRidersInWaitDict()
        self.assertEqual(WAITING, r1.getStatus())
        self.assertEqual("7: {0: {}, 1: {}, 2: {}, 3: {}, 4: {}, 5: {}, 6: {1: [R1, ], }, 7: {}, 8: {}, 9: {}, 10: {}, 11: {}, }", dispatch.showRiderWaitDict(7))
        self.assertEqual(1, r1.getWaitTime())
        self.assertEqual(1, dispatch.countRiderNumberInWaitDict())

        RiderStatusTracker.timestamp = 21
        dispatch.updateRidersInWaitDict()
        self.assertEqual(CANCEL, r1.getStatus())
        self.assertEqual("7: {0: {}, 1: {}, 2: {}, 3: {}, 4: {}, 5: {}, 6: {}, 7: {}, 8: {}, 9: {}, 10: {}, 11: {}, }", dispatch.showRiderWaitDict(7))
        self.assertEqual("{R1, }", dispatch.showRiderCanceledDict())
        self.assertEqual(1, r1.getWaitTime())
        self.assertEqual(1, dispatch.countRiderNumberInCancelDict())