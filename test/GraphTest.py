import unittest
from src.Graph.Graph import Graph

class GraphTest(unittest.TestCase):
    def testQueryTravelCost(self):
        self.assertEqual(1, Graph.queryTravelCost(7, 6))
        self.assertEqual(3, Graph.queryTravelCost(7, 19))
        self.assertEqual(3, Graph.queryTravelCost(8, 30))
        self.assertEqual(1, Graph.queryTravelCost(7, 6))
        self.assertEqual(0, Graph.queryTravelCost(6, 6))