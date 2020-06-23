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
from src.Rider.Rider import Rider
from src.Configure.Config import *
from src.Import.ImportDemandEvaluation import ImportDemandEvaluation

import matplotlib.pyplot as plt
import numpy as np


class Simulation:

    def __init__(self):
        self.__logger = Logger('Simulation')
        #self.__logger.setLevel(logging.DEBUG)
        self.__logger.info(-1, "__INIT__", None, None, "Create Simulation Object.")
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
            ImportDemandEvaluation.timestamp = self.__cycle

            # Start simulation time of this cycle
            print("The Cycle Number: ", self.__cycle)
            #print("Time: ", ImportDemandEvaluation.time)

            # Put the driver requests to dispatcher (The Driver List)
            self.__logger.info(self.__cycle, "RUN", None, None, "2. Put Drivers' Requests To Dispatcher From RequestList.")
            while not self.__driver_list.is_empty():
                curr_driver = self.__driver_list.remove()
                self.__logger.debug(self.__cycle, "RUN", None, None, "Current Driver Moved into Dict of Dispatcher: ", str(curr_driver))
                self.__dispatcher.handleDriverIntoDict(curr_driver)
            self.__dispatcher.countDriverNumberEachZone() #count idle driver number before match

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
            self.__logger.info(self.__cycle, "RUN", None, None, "4. Match Riders' Request to AN Appropriate Driver.")
            self.__dispatcher.matchRidertoDriver()
            #show reward
            #print("Driver number move in idle: ", self.__dispatcher.driver_num_move)
            #print("Driver number can pick rider: ", self.__dispatcher.driver_num_serve)

            # Update simulator's states
            self.__logger.info(self.__cycle, "RUN", None, None, "5. Update State of Simulator.")
            self.__dispatcher.updateDriverInDict()
            self.__dispatcher.updateRidersInWaitDict()

            #Show up results
            self.__logger.info(self.__cycle, "RUN", None, None, "6. Show Up All Results of this Cycle.")
            #print(self.__dispatcher.cancel_rider)
            #print(self.__dispatcher.no_work_driver)
            #if self.__cycle % SHOWN_INTERVAL == 0 and self.__cycle != SIMULATION_CYCLE_START:
            #    self.showPerformanceMetrics()
            #print("\n")
        self.showPerformanceMetrics()
        print("Simulation Terminated.\n")

        #self.drawMonitorDict(self.__dispatcher.wait_rider, self.__dispatcher.no_work_driver)

    def drawMonitorDict(self, monitor_dict1, monitor_dict2):
        for time1, item1 in monitor_dict1.items():
            for time2, item2 in monitor_dict2.items():
                if time1 == time2:
                    #plt.figure(figsize=(30, 20))
                    fig, (ax1, ax2) = plt.subplots(2, figsize=(30,20))
                    fig.suptitle(str(time1))
                    ax1.plot(item1[0:78], label='Wait Rider# after match', color='r')
                    ax1.plot(item2[0:78], label='Idle Driver# after match', color='b')
                    ax1.set_xticks(np.arange(0, 78, step=1))
                    ax1.set_yticks(np.arange(0, 300, step=20))
                    ax1.set_ylabel("driver#")
                    ax1.legend()
                    ax2.plot(self.__dispatcher.idle_driver_before_match[time1], label='Idle Driver# before match', color='b')
                    ax2.set_xticks(np.arange(0, 78, step=1))
                    ax2.set_yticks(np.arange(0, 300, step=20))
                    ax2.set_xlabel("zones")
                    ax2.set_ylabel("driver#")
                    ax2.legend()
                    plt.savefig(SAVE_PATH.format(time1))
                    plt.close()

    def showPerformanceMetrics(self):
        print("\n")

        print("The Number of Riders occured so far: ", self.__dispatcher.countCurrentTotalRiderNumber())
        print("The Number of Drivers: ", self.__dispatcher.countTotalDriverNumber())
        print("The Number of Cycles: ", self.__cycle)

        print("***************************************************************")
        print("Driver Performace Metrics:")
        print("Average Revenue: ", round(self.__dispatcher.calcAverageProfitOfDrivers(), 2))
        print("Average Trip Effort: ", round(self.__dispatcher.calcAverageTripEffortOfDrivers(), 2))
        print("Average Profit: ", round(self.__dispatcher.calcAverageProfitOfDrivers() - COST_PER_CYCLE * self.__dispatcher.calcAverageTripEffortOfDrivers(), 2))
        print("Average Utilization: ", round((260-self.__dispatcher.calcAverageIdleTimeOfDrivers())/260, 2))

        print("***************************************************************")
        print("Rider Performace Metrics:")
        print("Average Waiting Time (Cycles): ", round(self.__dispatcher.calcAverageWaitTimeOfRiders(), 2))
        print("Average Detour Time (Cycles): ", round(self.__dispatcher.calcAverageDetourTimeOfRiders(), 2))
        print("Average Fare: ", round(self.__dispatcher.calcAverageFareOfRiders(), 2))
        print("Average Default Fare: ", round(self.__dispatcher.calcAverageDefaultFareRiders(), 2))

        print("***************************************************************")
        print("System Performace Metrics:")
        print("Serving Rate: ", round(1 - self.__dispatcher.countRiderNumberInCancelDict() / self.__dispatcher.countCurrentTotalRiderNumber(), 2))

        total = self.__dispatcher.countRiderNumberInServeDict()+self.__dispatcher.countRiderNumberInFinishDict()
        print("Pooling Rate in 4: ", round(self.__dispatcher.grp_in_4*4/total, 3))
        print("Pooling Rate in 3: ", round(self.__dispatcher.grp_in_3*3/total, 3))
        print("Pooling Rate in 2: ", round(self.__dispatcher.grp_in_2*2/total,3))
        print("Pooling Rate in 1: ", round(self.__dispatcher.grp_in_1/total,3))
        print("***************************************************************")


if __name__ == "__main__":
    sim = Simulation()
    sim.importData()
    sim.run()