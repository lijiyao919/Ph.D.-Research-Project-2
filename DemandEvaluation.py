import pandas as pd
import datetime
import numpy as np
import json
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
        self.__state_value_table = {}

    #Intitialize state_value_table(state is time&zone, value is the demand evaluation)
    def __initilize(self):
        print('Initialize the State Value Table.')
        begin_time = datetime.datetime(2016, 4, 1, hour=0, minute=0)   #year, month and day is not important here
        final_time = datetime.datetime(2016, 4, 1, hour=23, minute=45) #year, month and day is not important here
        curr_time = final_time  # 2016-04-01 23:45:00
        while curr_time >= begin_time:
            curr_state_t = curr_time.strftime('%m/%d/%Y %H:%M').split(' ')[1]  #e.g. 23:45 (string type)
            self.__state_value_table[curr_state_t] =  np.zeros(78, dtype=np.int16)
            curr_time = curr_time-self.__delta_time
        #print(state_value_table)
        #print(len(state_value_table))  # should be 96


    def __readCSVByDate(self, curr_date):
        df = pd.read_csv("./Train/Chicago_April_{}_2016.csv".format(curr_date))
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

            df = self.__readCSVByDate(curr_date)

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
                print(self.__state_value_table[curr_state_t][1])
                if prev_state_t is not None:
                    print(self.__state_value_table[prev_state_t][1])
                print(1/number_of_day)
                if prev_state_t == None:
                    self.__state_value_table[curr_state_t] = self.__state_value_table[curr_state_t] + \
                                                           (1/number_of_day)*(pickup_count - self.__state_value_table[curr_state_t])
                else:
                    self.__state_value_table[curr_state_t] = self.__state_value_table[curr_state_t] + \
                                                           (1/number_of_day)*(pickup_count + DemandEvaluation.Gamma * self.__state_value_table[prev_state_t] - self.__state_value_table[curr_state_t])
                print(curr_df.groupby('Pickup Community Area').size())  # print for compare
                print(self.__state_value_table[curr_state_t])
                prev_state_t = curr_state_t
                curr_time = curr_time - self.__delta_time
            curr_date = curr_date + 1


    def saveSateValueTable(self):
        print('Save the State Value Table.')
        begin_time = datetime.datetime(2016, 4, 1, hour=0, minute=0)   #year, month and day is not important here
        final_time = datetime.datetime(2016, 4, 1, hour=23, minute=45) #year, month and day is not important here
        curr_time = final_time
        while curr_time >= begin_time:
            curr_state_t = curr_time.strftime('%m/%d/%Y %H:%M').split(' ')[1]
            self.__state_value_table[curr_state_t] =  self.__state_value_table[curr_state_t].tolist() #convert value in table for storing
            curr_time = curr_time-self.__delta_time
        with open('./Data/data.json', 'w') as fp:
            json.dump(self.__state_value_table, fp)

    def loadStateValueTable(self):
        print('Load the State Value Table.')
        with open('./Data/data.json') as fr:
            self.__state_value_table = json.load(fr)

    def drawBarChart(self):
        begin_time = datetime.datetime(2016, 4, 1, 0, 0)   #year, month and day is not important here
        final_time = datetime.datetime(2016, 4, 1, 23, 45) #year, month and day is not important here
        curr_time_figure = final_time
        while curr_time_figure >= begin_time:
            curr_state_t = curr_time_figure.strftime('%m/%d/%Y %H:%M').split(' ')[1]
            plt.bar(range(78), self.__state_value_table[curr_state_t])
            plt.xlim(1,78)
            plt.xticks(range(1, 78, 2))
            plt.xlabel('Zones')
            plt.ylabel('State Value')
            plt.title(curr_state_t)
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
        V=[]
        for i in range(time_len):
            row=[]
            for j in range(zone_len):
                a= self.__state_value_table[time[time_idx[i]][j]][zone[i][j]]
                row.append(a)
            V.append(row)
        V=np.array(V)
        fig = plt.figure()
        ax = Axes3D(fig)
        surf=ax.plot_surface(zone, time_idx, V, cmap=cm.coolwarm,)
        #fig.colorbar(surf, shrink=0.5, aspect=5)
        ax.set_ylabel('Time')
        ax.set_xlabel('Zone')
        plt.show()


demand = DemandEvaluation(4,4)
demand.handleStateValueTable()
demand.saveSateValueTable()
demand.drawSurfaceFigure()







