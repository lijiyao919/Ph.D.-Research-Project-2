from Config import *
from Driver import Driver
from Rider import Rider
import pandas as pd
import math


class RiderRequest:
    def __init__(self, timestamp, label, rider):
        self.timestamp = timestamp
        self.label = label
        self.rider = rider

    def __str__(self):
        ret = "{" + str(self.timestamp) + ", " + str(self.label) + ", " + str(self.rider) + "}"
        return ret


class DriverRequest:
    def __init__(self, timestamp, label, driver):
        self.timestamp = timestamp
        self.label = label
        self.driver = driver

    def __str__(self):
        ret = "{" + str(self.timestamp) + ", " + str(self.label) + ", " + str(self.driver) + "}"
        return ret


def readRequestFromCsv(driver_request_list, rider_request_list):
    print(FILENAME_R)
    rider = pd.read_csv(FILENAME_R)
    driver = pd.read_csv(FILENAME_D)
    numOfDriver = len(driver)

    print("Import Driver Data:")
    for i in range(0,numOfDriver):
        obs = driver.iloc[i, :]
        timestamp = obs["Time"]
        actor_id =  obs["ID"]
        zone_id = obs["Zone"]
        request = DriverRequest(timestamp, "DriverRequest", Driver(actor_id, zone_id))
        if request is not None:
            driver_request_list.add(request)
        else:
            pass
            #log error
        if i%100 == 0:
            print(i)

    print("Import Rider Data:")
    for i in range(RIDER_ROW_START, RIDER_ROW_END):
        obs = rider.iloc[i,:]

        timestamp = ((pd.to_datetime(obs["Trip Start Timestamp"])- pd.Timestamp(2016, 4, 11, 0))/pd.to_timedelta(1, unit='m'))/SIMULATION_CYCLE
        actor_id = "R" + str(i)
        pickup_zone = int(obs["Pickup Community Area"])
        dropoff_zone = int(obs["Dropoff Community Area"])
        default_price = float(obs["Trip Total"])
        src_lat = float(obs["Pickup Centroid Latitude"])
        src_lon = float(obs["Pickup Centroid Longitude"])
        dest_lat = float(obs["Dropoff Centroid Latitude"])
        dest_lon = float(obs["Dropoff Centroid Longitude"])
        patience = 40
        request = RiderRequest(timestamp, "RiderRequest", Rider(actor_id, timestamp, pickup_zone, dropoff_zone, default_price, patience, src_lon, src_lat, dest_lon, dest_lat))
        if request is not None:
            rider_request_list.add(request)
        else:
            pass
            #pass

        if i%1000 == 0:
            print(i)
