import pandas as pd
import datetime
import numpy as np
import matplotlib.pyplot as plt

curr_date = 11

class Visualization:
    def __init__(self):
        self.begin_time = datetime.datetime(2016, 4, curr_date, hour=0, minute=0)  # year, month and day is not important here
        self.final_time = datetime.datetime(2016, 4, curr_date, hour=23, minute=45)  # year, month and day is not important here
        self.delta_time = datetime.timedelta(minutes=15)
        self.pickup_table = {}
        self.dropoff_table = {}
        self.transition_table = {}

    # Intitialize state_value_table(state is time&zone, value is the demand evaluation)
    def __initilize_table(self):
        print('Initialize the State Value Table.')
        curr_time = self.begin_time  # 2016-04-01 23:45:00
        while curr_time <= self.final_time:
            curr_state_t = curr_time.strftime('%m/%d/%Y %H:%M').split(' ')[1]  # e.g. 23:45 (string type)
            self.pickup_table[curr_state_t] = np.zeros(78, dtype=np.float64)
            self.dropoff_table[curr_state_t] = np.zeros(78, dtype=np.float64)
            curr_time = curr_time + self.delta_time

    def __readCSV(self, curr_date):
        df = pd.read_csv("C:/Users/a02231961/PycharmProjects/Ph.D.-Research-Project-2/data/Chicago_April_11_2016.csv")
        df['Trip Start Timestamp'] = df['Trip Start Timestamp'].astype('datetime64[ns]') #e.g. 4/4/2016 0:00===> 2016-04-04 00:00:00
        df['Trip Total'] = df['Trip Total'].str.replace(',', '').astype('float64') #e.g. 1,200===>1200.0
        return df

    def handleRequestCount(self):
        print('Count pickup and dropoff in each zone.')
        self.__initilize_table()

        df = self.__readCSV(curr_date)
        g_time = df.groupby('Trip Start Timestamp')
        curr_time = self.final_time

        while curr_time >= self.begin_time:
            # clac the reward (current number of requests in each zone)
            pickup_count = np.zeros(78, dtype=np.int16)
            dropoff_count = np.zeros(78, dtype=np.int16)
            curr_df = g_time.get_group(curr_time.strftime('%m/%d/%Y %H:%M'))
            curr_state_t = curr_time.strftime('%m/%d/%Y %H:%M').split(' ')[1]

            row = 0
            while row < len(curr_df['Pickup Community Area']):
                pickup_count[curr_df['Pickup Community Area'].iloc[row]] += 1
                dropoff_count[curr_df['Dropoff Community Area'].iloc[row]] += 1
                row += 1
            # update the state value
            print('The current time: ', curr_state_t)
            self.pickup_table[curr_state_t] = pickup_count
            self.dropoff_table[curr_state_t] = dropoff_count

            print(curr_df.groupby('Pickup Community Area').size())  # print for compare
            print(curr_df.groupby('Dropoff Community Area').size())
            curr_time = curr_time - self.delta_time

    def handleTransitionTable(self, zone_id):
        print('Count from zone_id to the other zones.')
        self.__initilize_table()

        df = self.__readCSV(curr_date)
        g_time = df.groupby('Trip Start Timestamp')
        curr_time = self.final_time

        while curr_time >= self.begin_time:
            # clac the reward (current number of requests in each zone)
            dropoff_count = np.zeros(78, dtype=np.int16)
            curr_df = g_time.get_group(curr_time.strftime('%m/%d/%Y %H:%M'))
            curr_state_t = curr_time.strftime('%m/%d/%Y %H:%M').split(' ')[1]

            row = 0
            while row < len(curr_df['Pickup Community Area']):
                if curr_df['Pickup Community Area'].iloc[row] == zone_id:
                    dropoff_count[curr_df['Dropoff Community Area'].iloc[row]] += 1
                row += 1
            # update the state value
            print('The current time: ', curr_state_t)
            self.transition_table[curr_state_t] = dropoff_count

            print(self.transition_table[curr_state_t])
            curr_time = curr_time - self.delta_time



    def showCountWRTZones(self, table):
        print("Show Pickup Number Per Zone Along with time")
        for zone_id in range(1,78):
            curr_time = self.begin_time
            list=[]
            while curr_time <= self.final_time:
                curr_state_t = curr_time.strftime('%m/%d/%Y %H:%M').split(' ')[1]
                list.append(table[curr_state_t][zone_id])
                curr_time = curr_time + self.delta_time
            plt.plot(list)
            plt.title("Zone ID: "+str(zone_id))
            plt.xticks(range(0,97,4))
            #plt.savefig('../Figures/zone_{}.jpg'.format(zone_id), dpi=300)
            plt.show()
            plt.close()

v= Visualization()
v.handleRequestCount()
v.showCountWRTZones(v.pickup_table)
#v.handleTransitionTable(28)
#v.showCountWRTZones(v.transition_table)