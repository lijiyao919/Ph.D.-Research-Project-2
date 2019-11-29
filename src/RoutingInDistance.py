from src.RoutingStrategy import RoutingStrategy
from src.RoutingElem import RoutingElem
from src.Config import *

class RoutingInDistance(RoutingStrategy):

    def __init__(self, riders, route):
        super().__init__(riders, route)

    def planRoute(self):
        #pickup zone
        src_zone = self.riders.items()[0][1].getSrcZone()
        elem = RoutingElem(src_zone, PICKUP, None)
        self.route.append(elem)

        #dropoff zone
        for rider_id, rider in sorted(self.riders.items(), key=lambda x: x[1].getShortestTime()):
            elem = RoutingElem(rider.getDestZone(), DROPOFF, rider_id)
            self.route.append(elem)
