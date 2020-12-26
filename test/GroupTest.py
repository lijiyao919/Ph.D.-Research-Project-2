import unittest
from src.Rider.Group import Group
from src.Rider.Rider import Rider

class GroupTest(unittest.TestCase):
    def testConstructor(self):
        g1 = Group(1)
        self.assertEqual("{1: []}", str(g1))

    def testAddRiders(self):
        r1 = Rider(1, 0, 7, 6, 10, 20, 1, 1, 2, 1)
        r2 = Rider(2, 0, 7, 8, 10, 20, 1, 1, 2, 1)
        r3 = Rider(3, 0, 7, 10, 10, 20, 1, 1, 2, 1)
        r4 = Rider(4, 0, 7, 12, 10, 20, 1, 1, 2, 1)

        g1 = Group(1)
        g1.addRider(r1)
        g1.addRider(r2)

        self.assertEqual(2, g1.getGroupSize())
        self.assertEqual(8, g1.getDestination())
        self.assertEqual(True, g1.isInGroup(r1))
        self.assertEqual(True, g1.isInGroup(r2))
        self.assertEqual(False, g1.isInGroup(r3))
        self.assertEqual(False, g1.isInGroup(r4))

        id = 1
        for rider in g1.getRiders().values():
            self.assertEqual(id, rider.getID())
            id += 1

        g1.addRider(r3)
        g1.addRider(r4)
        self.assertEqual(4, g1.getGroupSize())
        self.assertEqual(12, g1.getDestination())
        self.assertEqual(True, g1.isInGroup(r1))
        self.assertEqual(True, g1.isInGroup(r2))
        self.assertEqual(True, g1.isInGroup(r3))
        self.assertEqual(True, g1.isInGroup(r4))

        id = 1
        for rider in g1.getRiders().values():
            self.assertEqual(id, rider.getID())
            id += 1





