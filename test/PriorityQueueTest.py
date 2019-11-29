import unittest
from src.Graph.PriorityQueue import PriorityQueue

class PriorityQueueTest(unittest.TestCase):
    def testValidConstructor(self):
        pq = PriorityQueue()
        self.assertTrue(isinstance(pq.getHeap(), list))
        self.assertEquals(0, len(pq.getHeap()))
        self.assertTrue(isinstance(pq.getEntryFinder(), dict))
        self.assertEquals(0, len(pq.getEntryFinder()))

    def testIsEmptyFalse(self):
        pq = PriorityQueue()
        pq.add_task(10,20)
        self.assertFalse(pq.isEmpty())

    def testIsEmptyTrue(self):
        pq = PriorityQueue()
        self.assertTrue(pq.isEmpty())

    def testAddTask(self):
        pq = PriorityQueue()
        pq.add_task(10,1)
        pq.add_task(11,1)
        pq.add_task(12,2)
        self.assertEquals([[1, 0, 10], [1, 1, 11], [2, 2, 12]], pq.getHeap())
        self.assertEquals({10: [1, 0, 10], 11: [1, 1, 11], 12: [2, 2, 12]}, pq.getEntryFinder())
        pq.add_task(11,0)
        self.assertEquals([[0, 3, 11], [1, 0, 10], [2, 2, 12], [1, 1, '<removed-task>']], pq.getHeap())
        self.assertEquals({10: [1, 0, 10], 11: [0, 3, 11], 12: [2, 2, 12]}, pq.getEntryFinder())

    def testPopTask(self):
        try:
            pq = PriorityQueue()
            pq.add_task(10, 1)
            pq.add_task(11, 1)
            pq.add_task(12, 2)
            pq.add_task(11, 0)
            self.assertEquals((0, 11), pq.pop_task())
            self.assertEquals((1, 10), pq.pop_task())
            self.assertEquals((2, 12), pq.pop_task())
            pq.pop_task()
            self.fail("Expected exception here.")
        except:
            pass

