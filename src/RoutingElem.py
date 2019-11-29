class RoutingElem:
    def __init__(self, zone_id, event, rider_id):
        self.__zone_id = zone_id
        self.__event = event     #pickup or dropoff
        self.__rider_id = rider_id
        self.__event_time = None

    def getZoneID(self):
        return self.__zone_id

    def getEvent(self):
        return self.__event

    def getRiderID(self):
        return self.__rider_id

    def setEventTime(self, time):
        self.__event_time = time

    def getEventTime(self):
        return self.__event_time

