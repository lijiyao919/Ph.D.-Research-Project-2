from PriorityQueue import PriorityQueue
from Data.Map import AdjList_Chicago


class Graph:
    def __init__(self):
        self.edge = AdjList_Chicago
        self.cache = {}

    def calcShortestPath(self, src, dest):
        pq=PriorityQueue()
        distances = {vertex: float('infinity') for vertex in self.edge}
        distances[src] = 0
        #print(distances)

        for vertex, distance in distances.items():
            pq.add_task(vertex, distance)

        while pq.isEmpty() is not True:
            current_distance, current_vertex = pq.pop_task()

            if (src, current_vertex) not in self.cache:
                self.cache[(src, current_vertex)] = current_distance

            if current_vertex == dest:
                return current_distance

            for neighbor in self.edge[current_vertex]:
                if distances[neighbor] > distances[current_vertex]+1:
                    distances[neighbor] = distances[current_vertex]+1
                    pq.add_task(neighbor, distances[neighbor])

    def queryTravelCost(self, src, dest):
        if (src, dest) in self.cache:
            print('Read from cache.')
            return self.cache[(src, dest)]
        else:
            return self.calcShortestPath(src,dest)

'''gp = Graph()
print(gp.queryTravelCost('32', '76'))
print(gp.queryTravelCost('32', '25'))'''