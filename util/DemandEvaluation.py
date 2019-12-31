import pandas as pd
import datetime
import numpy as np
import json
from src.Graph.Map import AdjList_Chicago
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
pd.set_option('display.max_columns', 20)


class DemandEvaluation:
    Gamma = 0.6

    def __init__(self, start, end):
        self.__start_date = start
        self.__end_date = end
        self.__delta_time = datetime.timedelta(minutes=15)
        self.__state_value = {}

    #Intitialize state_value_table(state is time&zone, value is the demand evaluation)
    def __initilize(self):
        print('Initialize the State Value Table.')
        begin_time = datetime.datetime(2016, 4, 11, hour=0, minute=0)   #year, month and day is not important here
        final_time = datetime.datetime(2016, 4, 11, hour=23, minute=45) #year, month and day is not important here
        curr_time = final_time  # 2016-04-01 23:45:00
        while curr_time >= begin_time:
            curr_state_t = curr_time.strftime('%m/%d/%Y %H:%M').split(' ')[1]  #e.g. 23:45 (string type)
            self.__state_value[curr_state_t] =  np.zeros(78, dtype=np.float64)
            curr_time = curr_time-self.__delta_time
        #print(state_value_table)
        #print(len(state_value_table))  # should be 96

    def __readCSV(self, curr_date):
        df = pd.read_csv("C:/Users/a02231961/PycharmProjects/Ph.D.-Research-Project-2/data/Chicago_April_11_2016.csv")
        df['Trip Start Timestamp'] = df['Trip Start Timestamp'].astype('datetime64[ns]') #e.g. 4/4/2016 0:00===> 2016-04-04 00:00:00
        df['Trip Total'] = df['Trip Total'].str.replace(',', '').astype('float64') #e.g. 1,200===>1200.0
        return df

    def handleStateValueTable(self):
        print('Handle the State Value Table.')
        curr_date = self.__start_date
        number_of_day = 0
        self.__initilize()
        while curr_date <= self.__end_date:
            #read file and convert datatype
            number_of_day+=1

            df = self.__readCSV(curr_date)

            #group by timestamp
            g_time=df.groupby('Trip Start Timestamp')

            #start time and end time in a date
            date_start_time = datetime.datetime(2016, 4, curr_date, 0, 0)
            date_end_time = datetime.datetime(2016, 4, curr_date, 23, 45)
            print('The date: ', date_start_time.date)

            #calculate state value in a day
            curr_time = date_end_time
            prev_state_t = None
            while curr_time >= date_start_time:
                #clac the reward (current number of requests in each zone)
                pickup_count = np.zeros(78, dtype=np.int16)
                curr_df = g_time.get_group(curr_time.strftime('%m/%d/%Y %H:%M'))
                curr_state_t = curr_time.strftime('%m/%d/%Y %H:%M').split(' ')[1]
                row = 0
                while row < len(curr_df['Pickup Community Area']):
                    pickup_count[curr_df['Pickup Community Area'].iloc[row]]+=1
                    row+=1
                #update the state value
                print('The current time: ', curr_state_t)
                if prev_state_t == None:
                    self.__state_value[curr_state_t] = self.__state_value[curr_state_t] + \
                                                           (1/number_of_day)*(pickup_count - self.__state_value[curr_state_t])
                else:
                    self.__state_value[curr_state_t] = self.__state_value[curr_state_t] + \
                                                           (1/number_of_day)*(pickup_count + DemandEvaluation.Gamma * self.__state_value[prev_state_t] - self.__state_value[curr_state_t])
                print(curr_df.groupby('Pickup Community Area').size())  # print for compare
                print(self.__state_value[curr_state_t])
                prev_state_t = curr_state_t
                curr_time = curr_time - self.__delta_time
            curr_date = curr_date + 1

    def saveSateValueTable(self):
        print('Save the State Value Table.')
        begin_time = datetime.datetime(2016, 4, 11, hour=0, minute=0)   #year, month and day is not important here
        final_time = datetime.datetime(2016, 4, 11, hour=23, minute=45) #year, month and day is not important here
        curr_time = final_time
        while curr_time >= begin_time:
            curr_state_t = curr_time.strftime('%m/%d/%Y %H:%M').split(' ')[1]
            self.__state_value[curr_state_t] =  self.__state_value[curr_state_t].tolist() #convert value in table for storing
            curr_time = curr_time-self.__delta_time
        with open('../data/data1.json', 'w') as fp:
            json.dump(self.__state_value, fp)

    def loadStateValueTable(self):
        print('Load the State Value Table.')
        with open('../data/data.json') as fr:
            self.__state_value = json.load(fr)

    def drawBarChart(self):
        begin_time = datetime.datetime(2016, 4, 11, 0, 0)   #year, month and day is not important here
        final_time = datetime.datetime(2016, 4, 11, 23, 45) #year, month and day is not important here
        curr_time_figure = final_time
        plt.figure(1)
        while curr_time_figure >= begin_time:
            curr_state_t = curr_time_figure.strftime('%m/%d/%Y %H:%M').split(' ')[1]
            plt.subplot(211)
            plt.bar(range(78), self.__state_value[curr_state_t])
            plt.title(curr_state_t)
            plt.subplot(212)
            plt.xlabel("Zone ID")
            plt.show()
            curr_time_figure = curr_time_figure - self.__delta_time

    def drawSurfaceFigure(self):
        base = datetime.datetime(2000, 1, 1)
        time = np.array([(base + datetime.timedelta(minutes=15*i)).strftime('%H:%M') for i in range(96)])
        time_idx = range(96)
        zone = range(1,78)

        zone_len = len(zone)
        time_len = len(time)

        zone, time_idx = np.meshgrid(zone, time_idx)
        #print(zone)
        #print(time_idx)
        V1=[]
        for i in range(time_len):
            row1=[]
            for j in range(zone_len):
                a1= self.__state_value[time[time_idx[i]][j]][zone[i][j]]
                row1.append(a1)
            V1.append(row1)
        V1=np.array(V1)
        fig = plt.figure()
        #ax = Axes3D(fig)

        # ===============
        #  First subplot
        # ===============
        ax = fig.add_subplot(1, 2, 1, projection='3d')
        ax.plot_surface(zone, time_idx, V1, cmap=cm.coolwarm,)
        #fig.colorbar(surf, shrink=0.5, aspect=5)
        ax.set_ylabel('Time')
        ax.set_xlabel('Zone')


        plt.show()


demand = DemandEvaluation(11,11)
demand.handleStateValueTable()
demand.saveSateValueTable()
demand.drawSurfaceFigure()
