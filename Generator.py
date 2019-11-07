from Config import *
import pandas as pd

def createDriverRequest():
    d = {"Time": [],
         "ID": [],
         "Zone": [] }
    cols = ["Time", "ID", "Zone"]
    cnt = 0

    for zone in [8, 32]:
        for i in range(0, BUSIEST_ZONE):
            time = SIMULATION_CYCLE_START
            id = "D" + str(cnt)
            d["Time"].append(time)
            d["ID"].append(id)
            d["Zone"].append(zone)
            cnt+=1

    for zone in [28]:
        for i in range(0, BUSIER_ZONE):
            time = SIMULATION_CYCLE_START
            id = "D" + str(cnt)
            d["Time"].append(time)
            d["ID"].append(id)
            d["Zone"].append(zone)
            cnt+=1

    for zone in [3,22,24,33,56,76,77]:
        for i in range(0, BUSY_ZONE):
            time = SIMULATION_CYCLE_START
            id = "D" + str(cnt)
            d["Time"].append(time)
            d["ID"].append(id)
            d["Zone"].append(zone)
            cnt += 1

    for zone in [1,2,3,4,5,14,15,16,21,22,41]:
        for i in range(0, COMMON_ZONE):
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


