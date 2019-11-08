import unittest
from Rider import Rider
from Driver import Driver
from Dispatcher import Dispatcher

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
        dispatcher.handleDriverRequest(d1)
        dispatcher.handleDriverRequest(d2)
        dispatcher.handleDriverRequest(d3)
        dispatcher.handleDriverRequest(d4)
        dispatcher.handleDriverRequest(d5)
        dispatcher.handleDriverRequest(d6)
        dispatcher.handleDriverRequest(d7)

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
        dispatcher.handleRiderRequest(r1)
        dispatcher.handleRiderRequest(r2)
        dispatcher.handleRiderRequest(r3)
        dispatcher.handleRiderRequest(r4)
        dispatcher.handleRiderRequest(r5)
        dispatcher.handleRiderRequest(r6)
        dispatcher.handleRiderRequest(r7)
        dispatcher.handleRiderRequest(r8)
        dispatcher.handleRiderRequest(r9)


        r10 = Rider("R10", 0, 7, 6, 10, 20, 1, 1, 1, 2)  # 90
        r12 = Rider("R12", 0, 7, 6, 10, 20, 1, 1, 1, 2)
        r13 = Rider("R13", 0, 7, 6, 10, 20, 1, 1, 1, 2)
        r14 = Rider("R14", 0, 7, 6, 10, 20, 1, 1, 1, 2)
        r15 = Rider("R15", 0, 7, 6, 10, 20, 1, 1, 1, 2)

        dispatcher.handleRiderRequest(r10)
        dispatcher.handleRiderRequest(r12)
        dispatcher.handleRiderRequest(r13)
        dispatcher.handleRiderRequest(r14)
        dispatcher.handleRiderRequest(r15)

        r16 = Rider("R16", 0, 7, 6, 10, 20, 1, 1, 2, 1) #0
        r17 = Rider("R17", 0, 7, 6, 10, 20, 1, 1, 2, 1)
        r18 = Rider("R18", 0, 7, 6, 10, 20, 1, 1, 2, 1)
        r19 = Rider("R19", 0, 7, 6, 10, 20, 1, 1, 2, 1)
        dispatcher.handleRiderRequest(r16)
        dispatcher.handleRiderRequest(r17)
        dispatcher.handleRiderRequest(r18)
        dispatcher.handleRiderRequest(r19)

        self.assertEqual(18, dispatcher.getRiderWaitDictLen())
        print(dispatcher.showRiderWaitDict())

    def testCheckRiderPatience(self):
        r1 = Rider("R1", 0, 7, 1, 10, 20, 1, 1, 2, 1)
        r2 = Rider("R2", 0, 7, 1, 10, 20, 1, 1, 2, 1)
        r3 = Rider("R3", 0, 7, 1, 10, 20, 1, 1, 2, 1)
        r4 = Rider("R4", 0, 7, 1, 10, 20, 1, 1, 2, 1)
        dispatcher = Dispatcher()
        dispatcher.handleRiderRequest(r1)
        dispatcher.handleRiderRequest(r2)
        dispatcher.handleRiderRequest(r3)
        dispatcher.handleRiderRequest(r4)
        Dispatcher.timestamp=21

        dispatcher.checkRiderPatience()

        self.assertEqual(0, dispatcher.getRiderWaitDictLen())
        self.assertEqual(4, dispatcher.getRiderCancelDictLen())
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
        dispatch.handleDriverRequest(d1)
        dispatch.handleDriverRequest(d2)
        dispatch.handleDriverRequest(d3)
        dispatch.handleDriverRequest(d4)

        dispatch.handleRiderRequest(r1)
        dispatch.handleRiderRequest(r2)
        dispatch.handleRiderRequest(r3)
        dispatch.handleRiderRequest(r4)
        dispatch.handleRiderRequest(r5)

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

        self.assertEqual(0, dispatch.getRiderWaitDictLen())
        self.assertEqual(5, dispatch.getRiderServeDictLen())
        print("check dispatcher")
        print(dispatch.showRiderWaitDict())
        print(dispatch.showRiderServedDict())

    def testUpdateDriverStatus(self):
        r1 = Rider("R1", 0, 7, 1, 10, 20, 1, 1, 2, 1)  # 0
        d1 = Driver("D1", 6)
        d2 = Driver("D2", 20)
        dispatch = Dispatcher()
        dispatch.handleDriverRequest(d1)
        dispatch.handleDriverRequest(d2)
        dispatch.handleRiderRequest(r1)
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
        self.assertEqual(1, dispatch.getRiderFinishDictLen())

    def testUpdateRiderStatus(self):
        r1 = Rider("R1", 0, 7, 1, 10, 20, 1, 1, 2, 1)
        dispatch = Dispatcher()
        dispatch.handleRiderRequest(r1)

        self.assertEqual(0,r1.getWaitTime())
        dispatch.updateRiderStatus()
        self.assertEqual(1,r1.getWaitTime())










