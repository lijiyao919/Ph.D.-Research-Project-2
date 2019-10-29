from PriorityQueue import PriorityQueue
from Data.Map import AdjList_Chicago

class Graph:
    __edge = AdjList_Chicago
    __cache = {}

    @staticmethod
    def __calcShortestPath(src_z, dest_z):
        pq=PriorityQueue()
        distances = {vertex: float('infinity') for vertex in Graph.__edge}
        distances[src_z] = 0
        #print(distances)

        for vertex, distance in distances.items():
            pq.add_task(vertex, distance)

        while pq.isEmpty() is not True:
            current_distance, current_vertex = pq.pop_task()

            if (src_z, current_vertex) not in Graph.__cache:
                Graph.__cache[(src_z, current_vertex)] = current_distance

            if current_vertex == dest_z:
                return current_distance

            for neighbor in Graph.__edge[current_vertex]:
                if distances[neighbor] > distances[current_vertex]+1:
                    distances[neighbor] = distances[current_vertex]+1
                    pq.add_task(neighbor, distances[neighbor])

    @staticmethod
    def queryTravelCost(src_z, dest_z):
        if (src_z, dest_z) in Graph.__cache:
            #print('Read from cache.')
            return Graph.__cache[(src_z, dest_z)]
        else:
            return Graph.__calcShortestPath(src_z, dest_z)


