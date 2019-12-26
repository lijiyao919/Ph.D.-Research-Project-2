from src.Import.RequestList import RequestList
from src.Import.ImportData import ImportData
from src.Dispatcher.Dispatcher import Dispatcher
from src.Dispatcher.ClusteringStrategy import ClusteringStrategy
from src.Dispatcher.MatchingStrategy import MatchingStrategy
from src.Dispatcher.DriverStatusTracker import DriverStatusTracker
from src.Dispatcher.RiderStatusTracker import RiderStatusTracker
from src.Logger.Logger import Logger
from src.Driver.Driver import Driver
from src.Driver.RoutingStrategy import RoutingStrategy
from src.Rider import Rider
from src.Configure.Config import *
import time
import logging

class Simulation:

    def __init__(self):
        self.__logger = Logger('Simulation')
        self.__logger.info(-1, "__INIT__", None, None, "Create Simulation Object.")
        self.__logger.setLevel(logging.DEBUG)
        self.__driver_list = RequestList()
        self.__rider_list = RequestList()
        self.__dispatcher = Dispatcher()
        self.__cycle = 0
        self.__sim_time = []

    def importData(self,):
        ImportData.importDriverData(FILENAME_D, self.__driver_list)
        ImportData.importRiderData(FILENAME_R, self.__rider_list)

    def run(self):
        #Run simulation cycle
        for self.__cycle in range(SIMULATION_CYCLE_START, SIMULATION_CYCLE_END):
            # Initialize monitoring stuff
            for zone_id in range(1, 78):
                self.__dispatcher.cancel_rider[zone_id] = 0
                self.__dispatcher.no_work_driver[zone_id] = 0

            #Start simulation time of this cycle
            print("The Cycle Number: ", self.__cycle)

            # Synchronization the time with Modules(Driver, Dispatcher, Rider, and so on)
            self.__logger.info(self.__cycle, "RUN", None, None, "1. Synchronizing Time With Each Module.")
            #Dispatcher Module
            Dispatcher.timestamp = self.__cycle
            ClusteringStrategy.timestamp = self.__cycle
            MatchingStrategy.timestamp = self.__cycle
            DriverStatusTracker.timestamp = self.__cycle
            RiderStatusTracker.timestamp = self.__cycle
            #Driver Module
            Driver.timestamp = self.__cycle
            RoutingStrategy.timestamp = self.__cycle
            #Rider Module
            Rider.timestamp = self.__cycle
            #Import Module
            RequestList.timestamp = self.__cycle

            # Put the driver requests to dispatcher (The Driver List)
            self.__logger.info(self.__cycle, "RUN", None, None, "2. Put Drivers' Requests To Dispatcher From RequestList.")
            while not self.__driver_list.is_empty():
                curr_driver = self.__driver_list.remove()
                self.__logger.debug(self.__cycle, "RUN", None, None, "Current Driver Moved into Dict of Dispatcher: ", str(curr_driver))
                self.__dispatcher.handleDriverIntoDict(curr_driver)

            # Put the rider requests to dispatcher (The Rider List)
            self.__logger.info(self.__cycle, "RUN", None, None, "3. Put Rider' Requests To Dispatcher From RequestList.")
            while not self.__rider_list.is_empty() and self.__rider_list.first_element().getRequestTimeStamp() == self.__cycle:
                curr_rider = self.__rider_list.remove()
                self.__logger.debug(self.__cycle, "RUN", None, None, "Current Rider Moved into Dict of Dispatcher: ", str(curr_rider))
                self.__dispatcher.handleRiderIntoDict(curr_rider)


            #Show dispatch dicts
            print("waiting, serving, finished, canceled: ", self.__dispatcher.countRiderNumberInWaitDict(),
                  self.__dispatcher.countRiderNumberInServeDict(),
                  self.__dispatcher.countRiderNumberInFinishDict(),
                  self.__dispatcher.countRiderNumberInCancelDict())

            #match driver and rider by dispatcher
            start_sim = time.time()
            self.__logger.info(self.__cycle, "RUN", None, None, "4. Match Riders' Request to AN Appropriate Driver.")
            self.__dispatcher.matchRidertoDriver()
            end_sim = time.time()

            # Update simulator's states
            self.__logger.info(self.__cycle, "RUN", None, None, "5. Update State of Simulator.")
            self.__dispatcher.updateDriverInDict()
            self.__dispatcher.updateRidersInWaitDict()

            #Calc # of active driver desision time of this cycle
            diff_sim = end_sim - start_sim
            self.__sim_time.append(diff_sim)

            #Show up results
            self.__logger.info(self.__cycle, "RUN", None, None, "6. Show Up All Results of this Cycle.")
            print("Time Consume: ", diff_sim)
            print(self.filterMonitorDict(self.__dispatcher.cancel_rider))
            print(self.filterMonitorDict(self.__dispatcher.no_work_driver))
            if self.__cycle % SHOWN_INTERVAL == 0 and self.__cycle != SIMULATION_CYCLE_START:
                self.showPerformanceMetrics()
            print("\n")

        print("Simulation Terminated.\n")

    def filterMonitorDict(self, monitor_dict):
        ret="{"
        for zone_id, item in monitor_dict.items():
            if item > 0:
                ret=ret+str(zone_id)+":"+str(item)+", "
        ret=ret+"}"
        return ret

    def showPerformanceMetrics(self):
        print("\n")

        print("The Number of Riders occured so far: ", self.__dispatcher.countCurrentTotalRiderNumber())
        print("The Number of Drivers: ", self.__dispatcher.countTotalDriverNumber())
        print("The Number of Cycles: ", self.__cycle)

        print("***************************************************************")
        print("Driver Performace Metrics:")
        print("Average Profit: ", round(self.__dispatcher.calcAverageProfitOfDrivers(), 2))
        print("Average Idle Time: ", round(self.__dispatcher.calcAverageIdleTimeOfDrivers(), 2))

        print("***************************************************************")
        print("Rider Performace Metrics:")
        print("Average Waiting Time (Cycles): ", round(self.__dispatcher.calcAverageWaitTimeOfRiders(), 2))
        print("Average Detour Time (Cycles): ", round(self.__dispatcher.calcAverageDetourTimeOfRiders(), 2))
        print("Average Sat: ", round(self.__dispatcher.calcAverageSatOfRiders(), 2))
        print("Average Fare: ", round(self.__dispatcher.calcAverageFareOfRiders(), 2))
        print("Average Default Fare: ", round(self.__dispatcher.calcAverageDefaultFareRiders(), 2))

        print("***************************************************************")
        print("System Performace Metrics:")
        print("Serving Rate: ", round(1 - self.__dispatcher.countRiderNumberInCancelDict() / self.__dispatcher.countCurrentTotalRiderNumber(), 2))
        print("Average Running Time: ", round(sum(self.__sim_time) / len(self.__sim_time), 2))

        print("***************************************************************")
        print("\n")


if __name__ == "__main__":
    sim = Simulation()
    sim.importData()
    sim.run()