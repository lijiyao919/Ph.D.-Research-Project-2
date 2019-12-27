from src.Configure.Config import *
from src.Driver.Driver import Driver
from src.Rider.Rider import Rider
import pandas as pd


class ImportData:

    @staticmethod
    def importDriverData(file_name, driver_list):
        driver = pd.read_csv(file_name)
        numOfDriver = len(driver)

        print("Import Driver Data:")
        for i in range(0, numOfDriver):
            obs = driver.iloc[i, :]
            actor_id = obs["ID"]
            zone_id = obs["Zone"]
            driver_list.add(Driver(actor_id, zone_id))
            if i % 100 == 0:
                print(i)

    @staticmethod
    def importRiderData(file_name, rider_list):
        rider = pd.read_csv(file_name)

        print("Import Rider Data:")
        for i in range(RIDER_ROW_START, RIDER_ROW_END):
            obs = rider.iloc[i, :]

            timestamp = ((pd.to_datetime(obs["Trip Start Timestamp"]) - pd.Timestamp(2016, 4, 11, 0)) / pd.to_timedelta(1, unit='m')) / SIMULATION_CYCLE
            actor_id = "R" + str(i)
            pickup_zone = int(obs["Pickup Community Area"])
            dropoff_zone = int(obs["Dropoff Community Area"])
            default_price = float(obs["Trip Total"].replace(',', ''))
            src_lat = float(obs["Pickup Centroid Latitude"])
            src_lon = float(obs["Pickup Centroid Longitude"])
            dest_lat = float(obs["Dropoff Centroid Latitude"])
            dest_lon = float(obs["Dropoff Centroid Longitude"])
            patience = PATIENCE
            rider_list.add(Rider(actor_id, timestamp, pickup_zone, dropoff_zone, default_price, patience, src_lon, src_lat,
                            dest_lon, dest_lat))
            if i % 1000 == 0:
                print(i)





