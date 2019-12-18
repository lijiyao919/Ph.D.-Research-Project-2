from src.Driver.RoutingStrategy import RoutingStrategy
from src.Driver.RoutingElem import RoutingElem
from src.Configure.Config import *

class RoutingInDistance(RoutingStrategy):

    def __init__(self, riders, route):
        super().__init__(riders, route)

    def planRoute(self):
        if len(self.riders) > 0:
            #pickup zone
            for rider in self.riders.values():
                src_zone = rider.getSrcZone()
                break
            elem = RoutingElem(src_zone, PICKUP, None)
            self.route.append(elem)

            #dropoff zone
            for rider_id, rider in sorted(self.riders.items(), key=lambda x: x[1].getShortestTime()):
                elem = RoutingElem(rider.getDestZone(), DROPOFF, rider_id)
                self.route.append(elem)
        else:
            self.logger.error(RoutingStrategy.timestamp, "planRoute", None, None, "Trip route is empty.")
            raise Exception("Trip route is empty.")