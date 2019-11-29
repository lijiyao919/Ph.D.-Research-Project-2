import unittest
from src.Rider import Rider
from src.Driver import Driver
from src.Dispatcher import Dispatcher

class DispatcherTest(unittest.TestCase):
    def testValidConstruction(self):
        dispatcher = Dispatcher()
        print(dispatcher.showDriverDict())
        print(dispatcher.showRiderWaitDict())
        print(dispatcher.showRiderServedDict())
        print(dispatcher.showRiderFinishedDict())
        print(dispatcher.showRiderCanceledDict())
        print(dispatcher.showAssignGidDict())

    def testHandleDriverRequest(self):
        d1 = Driver("D1", 7)
        d2 = Driver("D2", 7)
        d3 = Driver("D3", 7)
        d4 = Driver("D4", 32)
        d5 = Driver("D5", 32)
        d6 = Driver("D6", 28)
        d7 = Driver("D7", 7)

        dispatcher = Dispatcher()
        dispatcher.handleDriverIntoDict(d1)
        dispatcher.handleDriverIntoDict(d2)
        dispatcher.handleDriverIntoDict(d3)
        dispatcher.handleDriverIntoDict(d4)
        dispatcher.handleDriverIntoDict(d5)
        dispatcher.handleDriverIntoDict(d6)
        dispatcher.handleDriverIntoDict(d7)

        print(dispatcher.showDriverDict())

    def testHandleRiderRequest(self):
        r1 = Rider("R1", 0, 7, 6, 10, 20, 1, 1, 2, 1)  # 0
        r2 = Rider("R2", 0, 7, 6, 10, 20, 1, 1, 2, 1)
        r3 = Rider("R3", 0, 7, 6, 10, 20, 1, 1, 2, 1)
        r4 = Rider("R4", 0, 7, 6, 10, 20, 1, 1, 2, 1)
        r5 = Rider("R5", 0, 7, 6, 10, 20, 1, 1, 2, 1)
        r6 = Rider("R6", 0, 7, 6, 10, 20, 1, 1, 2, 1)
        r7 = Rider("R7", 0, 7, 6, 10, 20, 1, 1, 2, 1)
        r8 = Rider("R8", 0, 7, 6, 10, 20, 1, 1, 2, 1)
        r9 = Rider("R9", 0, 7, 6, 10, 20, 1, 1, 2, 1)

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


        r10 = Rider("R10", 0, 7, 6, 10, 20, 1, 1, 1, 2)  # 90
        r12 = Rider("R12", 0, 7, 6, 10, 20, 1, 1, 1, 2)
        r13 = Rider("R13", 0, 7, 6, 10, 20, 1, 1, 1, 2)
        r14 = Rider("R14", 0, 7, 6, 10, 20, 1, 1, 1, 2)
        r15 = Rider("R15", 0, 7, 6, 10, 20, 1, 1, 1, 2)

        dispatcher.handleRiderIntoDict(r10)
        dispatcher.handleRiderIntoDict(r12)
        dispatcher.handleRiderIntoDict(r13)
        dispatcher.handleRiderIntoDict(r14)
        dispatcher.handleRiderIntoDict(r15)

        r16 = Rider("R16", 0, 7, 6, 10, 20, 1, 1, 2, 1) #0
        r17 = Rider("R17", 0, 7, 6, 10, 20, 1, 1, 2, 1)
        r18 = Rider("R18", 0, 7, 6, 10, 20, 1, 1, 2, 1)
        r19 = Rider("R19", 0, 7, 6, 10, 20, 1, 1, 2, 1)
        dispatcher.handleRiderIntoDict(r16)
        dispatcher.handleRiderIntoDict(r17)
        dispatcher.handleRiderIntoDict(r18)
        dispatcher.handleRiderIntoDict(r19)

        self.assertEqual(18, dispatcher.countRiderNumberInWaitDict())
        print(dispatcher.showRiderWaitDict())

    def testCheckRiderPatience(self):
        r1 = Rider("R1", 0, 7, 1, 10, 20, 1, 1, 2, 1)
        r2 = Rider("R2", 0, 7, 1, 10, 20, 1, 1, 2, 1)
        r3 = Rider("R3", 0, 7, 1, 10, 20, 1, 1, 2, 1)
        r4 = Rider("R4", 0, 7, 1, 10, 20, 1, 1, 2, 1)
        dispatcher = Dispatcher()
        dispatcher.handleRiderIntoDict(r1)
        dispatcher.handleRiderIntoDict(r2)
        dispatcher.handleRiderIntoDict(r3)
        dispatcher.handleRiderIntoDict(r4)
        Dispatcher.timestamp=21

        dispatcher.removeTimeoutRiderFromWaitDict()

        self.assertEqual(0, dispatcher.countRiderNumberInWaitDict())
        self.assertEqual(4, dispatcher.countRiderNumberInCancelDict())
        print(dispatcher.showRiderWaitDict())
        print(dispatcher.showRiderCanceledDict())


    def testPlanRoute(self):
        r1 = Rider("R1", 0, 7, 1, 10, 20, 1, 1, 2, 1)  # 0
        r2 = Rider("R2", 0, 7, 3, 10, 20, 1, 1, 2, 1)
        r3 = Rider("R3", 0, 7, 77, 10, 20, 1, 1, 2, 1)
        r4 = Rider("R4", 0, 7, 6, 10, 20, 1, 1, 2, 1)
        d1 = Driver("D1", 6)

        riders={}
        riders["R4"] = r4
        riders["R1"] = r1
        riders["R2"] = r2
        riders["R3"] = r3

        dispatcher = Dispatcher();
        route, total_effort = dispatcher.planRoute(riders, d1)
        self.assertEqual(5, total_effort)
        print(route)

    def testMatchRidertoDriver(self):
        r1 = Rider("R1", 0, 7, 1, 10, 20, 1, 1, 2, 1)  # 0
        r2 = Rider("R2", 0, 7, 3, 10, 20, 1, 1, 2, 1)
        r3 = Rider("R3", 0, 7, 77, 10, 20, 1, 1, 2, 1)
        r4 = Rider("R4", 0, 7, 6, 10, 20, 1, 1, 2, 1)
        r5 = Rider("R5", 0, 7, 6, 10, 20, 1, 1, 2, 1)

        d1 = Driver("D1", 6)
        d2 = Driver("D2", 6)
        d3 = Driver("D3", 6)
        d4 = Driver("D4", 5)

        dispatch = Dispatcher()
        dispatch.handleDriverIntoDict(d1)
        dispatch.handleDriverIntoDict(d2)
        dispatch.handleDriverIntoDict(d3)
        dispatch.handleDriverIntoDict(d4)

        dispatch.handleRiderIntoDict(r1)
        dispatch.handleRiderIntoDict(r2)
        dispatch.handleRiderIntoDict(r3)
        dispatch.handleRiderIntoDict(r4)
        dispatch.handleRiderIntoDict(r5)

        print(dispatch.showRiderWaitDict())
        print(dispatch.showRiderServedDict())

        dispatch.matchRidertoDriver()
        print("check Driver:")
        print(d1)
        print(d2)
        print(d3)
        print(d4)

        print("check Rider:")
        print(r1)
        print(r2)
        print(r3)
        print(r4)
        print(r5)

        self.assertEqual(0, dispatch.countRiderNumberInWaitDict())
        self.assertEqual(5, dispatch.countRiderNumberInServeDict())
        print("check dispatcher")
        print(dispatch.showRiderWaitDict())
        print(dispatch.showRiderServedDict())

    def testUpdateDriverStatus(self):
        r1 = Rider("R1", 0, 7, 1, 10, 20, 1, 1, 2, 1)  # 0
        d1 = Driver("D1", 6)
        d2 = Driver("D2", 20)
        dispatch = Dispatcher()
        dispatch.handleDriverIntoDict(d1)
        dispatch.handleDriverIntoDict(d2)
        dispatch.handleRiderIntoDict(r1)
        dispatch.matchRidertoDriver()

        print(r1)
        print(d1)
        print(dispatch.showRiderServedDict())
        print(dispatch.showRiderFinishedDict())
        self.assertEqual(0, d2.getIdleTime())
        Dispatcher.timestamp=10

        dispatch.updateDriverStatus()

        print("After Update: ")
        print(r1)
        print(d1)
        print(dispatch.showRiderServedDict())
        print(dispatch.showRiderFinishedDict())
        self.assertEqual(1, d2.getIdleTime())
        self.assertEqual(1, dispatch.countRiderNumberInFinishDict())

    def testUpdateRiderStatus(self):
        r1 = Rider("R1", 0, 7, 1, 10, 20, 1, 1, 2, 1)
        dispatch = Dispatcher()
        dispatch.handleRiderIntoDict(r1)

        self.assertEqual(0,r1.getWaitTime())
        dispatch.updateRiderStatus()
        self.assertEqual(1,r1.getWaitTime())










