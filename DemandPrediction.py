import pandas as pd
import datetime
import numpy as np
import json
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm

Gamma=0
start_date = 4
end_date = 4
delta_time = datetime.timedelta(minutes = 15)
pd.set_option('display.max_columns', 20)
N = 0

#Intitialize state value table(state is time&zone, value is the demand prediction)
print('Initialize the state value table.')
state_value_table = {}
final_time_initial = datetime.datetime(2016, 4, 4, 23, 45)
begin_time_initial = datetime.datetime(2016, 4, 4, 0, 0)
curr_time_initial = final_time_initial
while curr_time_initial >= begin_time_initial:
    curr_time_initial_str = curr_time_initial.strftime('%m/%d/%Y %H:%M')
    curr_hour_min_initial_str = curr_time_initial_str.split(' ')[1]
    state_value_table[curr_hour_min_initial_str] =  np.zeros(78, dtype=np.int16)
    curr_time_initial = curr_time_initial-delta_time
#print(state_value_table)
#print(len(state_value_table))

curr_date = start_date
while curr_date <= end_date:
    #read file and convert datatype
    N+=1
    df = pd.read_csv("./Train/Chicago_April_{}_2016.csv".format(curr_date))
    df['Trip Start Timestamp'] = df['Trip Start Timestamp'].astype('datetime64[ns]')
    df['Trip Total'] = df['Trip Total'].str.replace(',', '').astype('float64')

    #group by timestamp
    g_time=df.groupby('Trip Start Timestamp')

    #start time and end time in a day
    date_start_time = datetime.datetime(2016, 4, curr_date, 0, 0)
    date_end_time = datetime.datetime(2016, 4, curr_date, 23, 45)
    print('The date: ', date_start_time.date)

    #calculate state value in a day
    curr_time = date_end_time
    prev_hour_min_str = None
    while curr_time >= date_start_time:
        #clac the reward (current number of requests in each zone)
        pick_count_curr = np.zeros(78, dtype=np.int16)
        curr_time_str = curr_time.strftime('%m/%d/%Y %H:%M')
        print(curr_time_str)
        df_curr_time = g_time.get_group(curr_time_str)
        print(df_curr_time.groupby('Pickup Community Area').size())
        curr_hour_min_str = curr_time_str.split(' ')[1]
        row = 0
        while row < len(df_curr_time['Pickup Community Area']):
            pick_count_curr[df_curr_time['Pickup Community Area'].iloc[row]]+=1
            row+=1
        #update the state value
        print('The current time: ', curr_hour_min_str)
        if prev_hour_min_str == None:
            state_value_table[curr_hour_min_str] = state_value_table[curr_hour_min_str] + \
                                                   (1/N)*(pick_count_curr - state_value_table[curr_hour_min_str])
        else:
            state_value_table[curr_hour_min_str] = state_value_table[curr_hour_min_str] + \
                                                   (1/N)*(pick_count_curr + Gamma * state_value_table[prev_hour_min_str]-state_value_table[curr_hour_min_str])
        prev_hour_min_str = curr_hour_min_str
        curr_time = curr_time - delta_time
        print(state_value_table[curr_hour_min_str])
    curr_date = curr_date + 1

#convert value in table for storing
final_time_convert = datetime.datetime(2016, 4, 4, 23, 45)
begin_time_convert = datetime.datetime(2016, 4, 4, 0, 0)
curr_time_convert = final_time_convert
while curr_time_convert >= begin_time_convert:
    curr_time_convert_str = curr_time_convert.strftime('%m/%d/%Y %H:%M')
    curr_hour_min_convert_str = curr_time_convert_str.split(' ')[1]
    state_value_table[curr_hour_min_convert_str] =  state_value_table[curr_hour_min_convert_str].tolist()
    curr_time_convert = curr_time_convert-delta_time

#Store state value table
print('Store data into Json')
with open('./Data/data.json', 'w') as fp:
    json.dump(state_value_table, fp)

#read state value table
with open('./Data/data.json') as fr:
    state_value_table = json.load(fr)

#bar chart
'''final_time_figure = datetime.datetime(2016, 4, 4, 23, 45)
begin_time_figure = datetime.datetime(2016, 4, 4, 0, 0)
curr_time_figure = final_time_figure
while curr_time_figure >= begin_time_figure:
    curr_time_figure_str = curr_time_figure.strftime('%m/%d/%Y %H:%M')
    curr_hour_min_figure_str = curr_time_figure_str.split(' ')[1]
    plt.bar(range(78), state_value_table[curr_hour_min_figure_str])
    plt.xlim(1,78)
    plt.xticks(range(1, 78, 2))
    plt.xlabel('Zones')
    plt.ylabel('State Value')
    plt.title(curr_hour_min_figure_str)
    plt.show()
    curr_time_figure = curr_time_figure - delta_time'''

#Surface figure
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
        a= state_value_table[time[time_idx[i]][j]][zone[i][j]]
        row.append(a)
    V.append(row)
V=np.array(V)
fig = plt.figure()
ax = Axes3D(fig)
surf=ax.plot_surface(zone, time_idx, V, cmap=cm.coolwarm,)
fig.colorbar(surf, shrink=0.5, aspect=5)
ax.set_ylabel('Time')
ax.set_xlabel('Zone')
plt.show()








