from src.Configure.Config import *
import pandas as pd
import random

def createRiderRequest():
    rider = pd.read_csv(FILENAME_Chicago)
    d = {"Time": [],
         "ID": [],
         "Pickup": [],
         "Dropoff": [],
         "Fare": [],
         "Pickup Latitude": [],
         "Pickup Longitude": [],
         "Dropoff Latitude": [],
         "Dropoff Longitude": []}
    cols = ["Time", "ID", "Pickup", "Dropoff", "Fare", "Pickup Latitude", "Pickup Longitude", "Dropoff Latitude", "Dropoff Longitude"]
    cnt = 0

    print("Import data ...")
    for i in range(0, 57172):
        obs = rider.iloc[i, :]

        #time
        timestamp = ((pd.to_datetime(obs["Trip Start Timestamp"]) - pd.Timestamp(2016, 4, 11, 0)) / pd.to_timedelta(1,unit='m')) / SIMULATION_CYCLE
        timestamp = timestamp + round(random.uniform(0,4))
        d["Time"].append(timestamp)

        #id
        actor_id = "R" + str(i)
        d["ID"].append(actor_id)

        #price
        default_price = float(obs["Trip Total"].replace(',', ''))
        d["Fare"].append(default_price)

        #zone id
        pickup_zone = int(obs["Pickup Community Area"])
        dropoff_zone = int(obs["Dropoff Community Area"])
        d["Pickup"].append(pickup_zone)
        d["Dropoff"].append(dropoff_zone)

        #zone location
        src_lat = float(obs["Pickup Centroid Latitude"])
        d["Pickup Latitude"].append(src_lat)
        src_lon = float(obs["Pickup Centroid Longitude"])
        d["Pickup Longitude"].append(src_lon)
        dest_lat = float(obs["Dropoff Centroid Latitude"])
        d["Dropoff Latitude"].append(dest_lat)
        dest_lon = float(obs["Dropoff Centroid Longitude"])
        d["Dropoff Longitude"].append(dest_lon)

    print("Write data ...")
    fileName = FILENAME_R
    df = pd.DataFrame(d)
    df = df[cols]
    df.to_csv(fileName, index=False)

#file have to be sorted after generated
createRiderRequest()