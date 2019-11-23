from RequestReader import readRequestFromCsv
from RequestList import RequestList
from Dispatcher import Dispatcher
from Logger import Logger
from Driver import Driver
from Rider import Rider
from Config import *
import time
import logging

class Simulation:

    def __init__(self):
        self.logger = Logger('Simulation')
        self.logger.info(-1, "__INIT__", None, None, "Create Simulation Object.")
        self.logger.setLevel(logging.DEBUG)
        self.driver_list = RequestList()
        self.rider_list = RequestList()
        self.dispatcher = Dispatcher()
        self.cycle = 0
        self.sim_time = []


    def run(self):

        #Run simulation cycle
        for self.cycle in range(SIMULATION_CYCLE_START, SIMULATION_CYCLE_END):

            #Start simulation time of this cycle
            print("The Cycle Number: ", self.cycle)

            # Synchronization the time with Modules(Driver, Dispatcher, Rider, and so on)
            self.logger.info(self.cycle, "RUN", None, None, "1. Synchronizing Time With Each Module.")
            Driver.timestamp = self.cycle
            Rider.timestamp = self.cycle
            Dispatcher.timestamp = self.cycle
            RequestList.timestamp = self.cycle

            # Put the driver requests to dispatcher (The Driver List)
            self.logger.info(self.cycle, "RUN", None, None, "2. Put Drivers' Requests To Dispatcher From RequestList.")
            while not self.driver_list.is_empty() and self.driver_list.first_element().timestamp == self.cycle:
                curr_driver_request = self.driver_list.remove()
                self.logger.debug(self.cycle, "RUN", None, None, "Current Driver Request Moved into Dict of Dispatcher: ", str(curr_driver_request))
                self.dispatcher.handleDriverRequest(curr_driver_request.driver)

            # Put the rider requests to dispatcher (The Rider List)
            self.logger.info(self.cycle, "RUN", None, None, "3. Put Rider' Requests To Dispatcher From RequestList.")
            while not self.rider_list.is_empty() and self.rider_list.first_element().timestamp == self.cycle:
                curr_rider_request = self.rider_list.remove()
                self.logger.debug(self.cycle, "RUN", None, None, "Current Rider Request Moved into Dict of Dispatcher: ", str(curr_rider_request))
                self.dispatcher.handleRiderRequest(curr_rider_request.rider)

            #Show Driver and Rider in each zone
            print(self.dispatcher.showDriverNumberOfEachZone())
            print(self.dispatcher.showRiderNumberOfEachZone())

            #Update Riders' patience
            self.logger.info(self.cycle, "RUN", None, None, "4. Check Which Rider's Request Should be Cancelled in Rider List of Dispathcer.")
            self.dispatcher.checkRiderPatience()

            #Show dispatch dicts
            print("waiting, serving, finished, canceled: ", self.dispatcher.getRiderWaitDictLen(),
                  self.dispatcher.getRiderServeDictLen(),
                  self.dispatcher.getRiderFinishDictLen(),
                  self.dispatcher.getRiderCancelDictLen())

            #match driver and rider by dispatcher
            start_sim = time.time()
            self.logger.info(self.cycle, "RUN", None, None, "5. Match Riders' Request to AN Appropriate Driver.")
            self.dispatcher.matchRidertoDriver()
            end_sim = time.time()

            # Update simulator's states
            self.logger.info(self.cycle, "RUN", None, None, "6. Update State of Simulator.")
            self.dispatcher.updateDriverStatus()
            self.dispatcher.updateRiderStatus()

            #Calc # of active driver desision time of this cycle
            diff_sim = end_sim - start_sim
            self.sim_time.append(diff_sim)

            #Show up results
            self.logger.info(self.cycle, "RUN", None, None, "7. Show Up All Results of this Cycle.")
            if self.cycle % SHOWN_INTERVAL == 0 and self.cycle != SIMULATION_CYCLE_START:
                self.show()
            print("Time Consume: ", diff_sim)

        print("Simulation Terminated.\n")

    def show(self):
        print("\n")

        print("The Number of Riders occured so far: ", self.dispatcher.getCurrentTotalNumberOfRider())
        print("The Number of Riders to be served: ", self.dispatcher.getRiderWaitDictLen())
        print("The Number of Drivers: ", self.dispatcher.getDriverDictLen())
        print("The Number of Cycles: ", self.cycle)

        print("***************************************************************")
        print("Driver Performace Metrics:")
        print("Average Profit: ", round(self.dispatcher.calcAverageProfitOfDrivers(), 2))
        print("Average Idle Time: ", round(self.dispatcher.calcAverageIdleTimeOfDrivers(), 2))

        print("***************************************************************")
        print("Rider Performace Metrics:")
        print("Average Waiting Time (Cycles): ", round(self.dispatcher.calcAverageWaitTimeOfRiders(), 2))
        print("Average Detour Time (Cycles): ", round(self.dispatcher.calcAverageDetourTimeOfRiders(), 2))
        print("Average Sat: ", round(self.dispatcher.calcAverageSatOfRiders(), 2))
        print("Average Fare: ", round(self.dispatcher.calcAverageFareOfRiders(), 2))
        print("Average Default Fare: ", round(self.dispatcher.calcAverageDefaultFareRiders(), 2))

        print("***************************************************************")
        print("System Performace Metrics:")
        print("Serving Rate: ", round(1-self.dispatcher.getRiderCancelDictLen()/self.dispatcher.getCurrentTotalNumberOfRider(),2))
        print("Average Running Time: ", round(sum(self.sim_time)/len(self.sim_time), 2))

        print("***************************************************************")
        print("\n")


if __name__ == "__main__":
    sim = Simulation()
    readRequestFromCsv(sim.driver_list, sim.rider_list)
    sim.run()