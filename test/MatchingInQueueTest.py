import unittest
import datetime
from src.Dispatcher.MatchingStrategy import MatchingStrategy
from src.Dispatcher.MatchingInQueue import MatchingInQueue

class MatchingInQueueTest(unittest.TestCase):
    def testGetRationOfSupplyDemand(self):
        matcher = MatchingInQueue(None, None, None)
        MatchingStrategy.time = datetime.datetime(2016, 4, 11, hour=12, minute=00)
        self.assertEqual(6.6657924706520815,matcher.getRatioOfSupplyDemand(1))
        self.assertEqual(7.192340920182494, matcher.getRatioOfSupplyDemand(2))

        MatchingStrategy.time = datetime.datetime(2016, 4, 11, hour=12, minute=30)
        self.assertEqual(9.627201307366894, matcher.getRatioOfSupplyDemand(1))
        self.assertEqual(6.089835889395818, matcher.getRatioOfSupplyDemand(2))
