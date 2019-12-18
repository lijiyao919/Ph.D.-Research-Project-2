from src.Configure.Config import *
import pandas as pd

def createDriverRequest():
    d = {"Time": [],
         "ID": [],
         "Zone": [] }
    cols = ["Time", "ID", "Zone"]
    cnt = 0

    for zone in [1, 2, 9, 10, 11, 12,13,14,15,16,19,20,21,23,25,26,27,29,30,31,34,35,38,40,41,44]:
        for i in range(0, 1):
            time = SIMULATION_CYCLE_START
            id = "D" + str(cnt)
            d["Time"].append(time)
            d["ID"].append(id)
            d["Zone"].append(zone)
            cnt+=1

    for zone in [3, 22]:
        for i in range(0, 2):
            time = SIMULATION_CYCLE_START
            id = "D" + str(cnt)
            d["Time"].append(time)
            d["ID"].append(id)
            d["Zone"].append(zone)
            cnt+=1

    for zone in [4,24, 77]:
        for i in range(0, 4):
            time = SIMULATION_CYCLE_START
            id = "D" + str(cnt)
            d["Time"].append(time)
            d["ID"].append(id)
            d["Zone"].append(zone)
            cnt += 1

    for zone in [7]:
        for i in range(0, 5):
            time = SIMULATION_CYCLE_START
            id = "D" + str(cnt)
            d["Time"].append(time)
            d["ID"].append(id)
            d["Zone"].append(zone)
            cnt += 1

    for zone in [5,6,56]:
        for i in range(0, 10):
            time = SIMULATION_CYCLE_START
            id = "D" + str(cnt)
            d["Time"].append(time)
            d["ID"].append(id)
            d["Zone"].append(zone)
            cnt += 1

    for zone in [8, 28, 32, 76]:
        for i in range(0, 20):
            time = SIMULATION_CYCLE_START
            id = "D" + str(cnt)
            d["Time"].append(time)
            d["ID"].append(id)
            d["Zone"].append(zone)
            cnt += 1

    fileName = "./Test/Chicago_d.csv"
    df = pd.DataFrame(d)
    df = df[cols]
    df.to_csv(fileName, index=False)

createDriverRequest()


