from PriorityQueue import PriorityQueue
from Data.Map import AdjList_Chicago


class Graph:
    edge = AdjList_Chicago
    cache = {}

    @staticmethod
    def calcShortestPath(src, dest):
        pq=PriorityQueue()
        distances = {vertex: float('infinity') for vertex in Graph.edge}
        distances[src] = 0
        #print(distances)

        for vertex, distance in distances.items():
            pq.add_task(vertex, distance)

        while pq.isEmpty() is not True:
            current_distance, current_vertex = pq.pop_task()

            if (src, current_vertex) not in Graph.cache:
                Graph.cache[(src, current_vertex)] = current_distance

            if current_vertex == dest:
                return current_distance

            for neighbor in Graph.edge[current_vertex]:
                if distances[neighbor] > distances[current_vertex]+1:
                    distances[neighbor] = distances[current_vertex]+1
                    pq.add_task(neighbor, distances[neighbor])

    @staticmethod
    def queryTravelCost(src, dest):
        if (src, dest) in Graph.cache:
            #print('Read from cache.')
            return Graph.cache[(src, dest)]
        else:
            return Graph.calcShortestPath(src,dest)


#print(Graph.queryTravelCost('32', '76'))
#print(Graph.queryTravelCost('32', '25'))