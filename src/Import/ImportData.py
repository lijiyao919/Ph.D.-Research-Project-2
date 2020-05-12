from src.Configure.Config import *
from src.Driver.Driver import Driver
from src.Rider.Rider import Rider
import pandas as pd
import random

class ImportData:

    @staticmethod
    def importDriverData(file_name, driver_list):
        driver = pd.read_csv(file_name)
        numOfDriver = len(driver)

        #print("Import Driver Data:")
        for i in range(0, numOfDriver):
            obs = driver.iloc[i, :]
            actor_id = obs["ID"]
            zone_id = obs["Zone"]
            driver_list.add(Driver(actor_id, zone_id))
            #if i % 100 == 0:
            #    print(i)

    @staticmethod
    def importRiderData(file_name, rider_list):
        rider = pd.read_csv(file_name)

        #print("Import Rider Data:")
        for i in range(RIDER_ROW_START, RIDER_ROW_END):
            obs = rider.iloc[i, :]

            default_price = float(obs["Fare"])
            #if default_price > 200:
             #   continue
            timestamp = int(obs["Time"])
            actor_id = obs["ID"]
            pickup_zone = int(obs["Pickup"])
            dropoff_zone = int(obs["Dropoff"])
            src_lat = float(obs["Pickup Latitude"])
            src_lon = float(obs["Pickup Longitude"])
            dest_lat = float(obs["Dropoff Latitude"])
            dest_lon = float(obs["Dropoff Longitude"])
            patience = PATIENCE
            rider_list.add(Rider(actor_id, timestamp, pickup_zone, dropoff_zone, default_price, patience, src_lon, src_lat,
                            dest_lon, dest_lat))
            #if i % 1000 == 0:
            #    print(i)





