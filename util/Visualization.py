import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from src.Configure.Config import *

curr_date = 11

class Visualization:
    def __init__(self):
        self.begin_time = 0
        self.final_time = 479  # 11:45PM
        self.pickup_table = {}
        self.dropoff_table = {}
        self.transition_table = {}

    # Intitialize state_value_table(state is time&zone, value is the demand evaluation)
    def __initilize_table(self):
        print('Initialize the State Value Table.')
        curr_time = self.begin_time  # 2016-04-01 23:45:00
        while curr_time <= self.final_time:
            curr_state_t = curr_time
            self.pickup_table[curr_state_t] = np.zeros(78, dtype=np.float64)
            self.dropoff_table[curr_state_t] = np.zeros(78, dtype=np.float64)
            curr_time = curr_time + 1

    def __readCSV(self):
        df = pd.read_csv(FILENAME_R)
        df['Fare'] = df['Fare'].astype('float64') #e.g. 1,200===>1200.0
        return df

    def handleRequestCount(self):
        print('Count pickup and dropoff in each zone.')
        self.__initilize_table()

        df = self.__readCSV()
        g_time = df.groupby('Time')
        curr_time = self.final_time

        while curr_time >= self.begin_time:
            # clac the reward (current number of requests in each zone)
            pickup_count = np.zeros(78, dtype=np.int16)
            dropoff_count = np.zeros(78, dtype=np.int16)
            curr_df = g_time.get_group(curr_time)
            curr_state_t = curr_time

            row = 0
            while row < len(curr_df['Pickup']):
                pickup_count[curr_df['Pickup'].iloc[row]] += 1
                dropoff_count[curr_df['Dropoff'].iloc[row]] += 1
                row += 1
            # update the state value
            print('The current time: ', curr_state_t)
            self.pickup_table[curr_state_t] = pickup_count
            self.dropoff_table[curr_state_t] = dropoff_count

            print(curr_df.groupby('Pickup').size())  # print for compare
            print(curr_df.groupby('Dropoff').size())
            curr_time = curr_time - 1

    def handleTransitionTable(self, zone_id):
        print('Count from zone_id to the other zones.')
        self.__initilize_table()

        df = self.__readCSV()
        g_time = df.groupby('Time')
        curr_time = self.final_time

        while curr_time >= self.begin_time:
            # clac the reward (current number of requests in each zone)
            dropoff_count = np.zeros(78, dtype=np.int16)
            curr_df = g_time.get_group(curr_time)
            curr_state_t = curr_time

            row = 0
            while row < len(curr_df['Pickup']):
                if curr_df['Pickup'].iloc[row] == zone_id:
                    dropoff_count[curr_df['Dropoff'].iloc[row]] += 1
                row += 1
            # update the state value
            print('The current time: ', curr_state_t)
            self.transition_table[curr_state_t] = dropoff_count

            print(self.transition_table[curr_state_t])
            curr_time = curr_time - 1
        self.showTransitDesCount()


    def showTransitDesCount(self):
        for time in range(220, self.final_time+1):
            plt.figure(figsize=(30, 20))
            plt.bar(range(0,78), self.transition_table[time])
            plt.title(str(time))
            plt.xticks(range(0, 78, 1))
            plt.savefig("C:/Users/a02231961/PycharmProjects/Ph.D.-Research-Project-2/fig1/t_{}.jpg".format(time), dpi=300)
            plt.close()


v= Visualization()
v.handleTransitionTable(32)
