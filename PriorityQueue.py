import itertools
from heapq import heappush, heappop

class PriorityQueue:
    #static variable
    REMOVED = '<removed-task>'   # placeholder for a removed task
    counter = itertools.count()  # unique sequence count

    def __init__(self):
        self.heap = []              # list of entries arranged in a heap
        self.entry_finder = {}    # mapping of tasks to entries

    def isEmpty(self):
        if len(self.entry_finder) == 0:
            return True
        else:
            return False

    def add_task(self, task, priority=0):
        'Add a new task or update the priority of an existing task'
        if task in self.entry_finder:
            self.remove_task(task)
        count = next(PriorityQueue.counter)
        entry = [priority, count, task]
        self.entry_finder[task] = entry
        heappush(self.heap, entry)

    def remove_task(self, task):
        'Mark an existing task as REMOVED.  Raise KeyError if not found.'
        entry = self.entry_finder.pop(task)
        entry[-1] = PriorityQueue.REMOVED

    def pop_task(self):
        'Remove and return the lowest priority task. Raise KeyError if empty.'
        while self.heap:
            priority, count, task = heappop(self.heap)
            if task is not PriorityQueue.REMOVED:
                del self.entry_finder[task]
                return (priority, task)
        raise KeyError('pop from an empty priority queue')

