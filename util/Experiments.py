import matplotlib.pyplot as plt
import numpy as np

frontsize=14
driver_num = [116, 166, 216, 266, 316]

#serving rate
'''serving_rate=[0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
serving_rate_str=('0.2', '0.3', '0.4', '0.5', '0.6', '0.7', '0.8', '0.9', '1.0')
banerjee_w_1= [0.21, 0.31, 0.38, 0.43, 0.48]
banerjee_w_1_pool = [0.37, 0.49, 0.58, 0.65, 0.7]
banerjee_w_learn_pool = [0.38, 0.54, 0.65, 0.74, 0.79]
banerjee_w_learn_pool_idle =[0.43, 0.6, 0.71, 0.81, 0.87]
banerjee_w_learn_pool_idle_learn = [0.45, 0.61, 0.79, 0.93, 0.98]'''

#driver revenue
'''revenue=[800, 1000, 1200, 1400, 1600, 1800, 2000]
revenue_str=('800', '1000', '1200', '1400', '1600', '1800', '2000')
banerjee_w_1= [906, 910, 905, 858, 814]
banerjee_w_1_pool = [1635, 1654, 1556, 1402, 1261]
banerjee_w_learn_pool = [1712, 1848, 1687, 1567, 1414]
banerjee_w_learn_pool_idle =[2022, 2064, 1864, 1719, 1562]
banerjee_w_learn_pool_idle_learn = [2038, 2123, 2041, 1955, 1749]'''

#driver_effort
'''effort=[140, 160, 180, 200, 220, 240]
effort_str=('140', '160', '180', '200', '220', '240')
banerjee_w_1= [173, 170, 164, 153, 144]
banerjee_w_1_pool = [194, 183, 168, 151, 136]
banerjee_w_learn_pool = [198, 199, 182, 168, 152]
banerjee_w_learn_pool_idle =[235, 228, 213, 204, 188]
banerjee_w_learn_pool_idle_learn = [240, 239, 238, 235, 225]'''

#driver profit
'''profit=[600, 800, 1000, 1200, 1400, 1600]
profit_str=('600', '800', '1000', '1200', '1400', '1600')
banerjee_w_1= [594, 602, 609, 582, 554]
banerjee_w_1_pool = [1258, 1324, 1253, 1129, 1015]
banerjee_w_learn_pool = [1355, 1490, 1361, 1264, 1140]
banerjee_w_learn_pool_idle =[1600, 1653, 1480, 1351, 1223]
banerjee_w_learn_pool_idle_learn = [1606, 1692, 1611, 1531, 1342]'''

#rider call time
'''call=[0.5, 1, 1.5, 2, 2.5, 3, 3.5]
call_str=('0.5', '1', '1.5', '2', '2.5', '3', '3.5')
banerjee_w_1= [3.5, 3, 2.7, 2.4, 2.1]
banerjee_w_1_pool = [3, 2.7, 2.1, 1.8, 1.5]
banerjee_w_learn_pool = [3, 2.4, 2.1, 1.5, 1.2]
banerjee_w_learn_pool_idle =[3, 2.1, 1.8, 1.5, 0.9]
banerjee_w_learn_pool_idle_learn = [2.7, 2.1, 1.8, 1.2, 0.6]'''

#rider detour time
detour=[0.5, 1, 1.5, 2, 2.5, 3, 3.5]
detour_str=('0.5', '1', '1.5', '2', '2.5', '3', '3.5')
banerjee_w_1= [2.55, 2.2, 2.0, 2.0, 2.0]
banerjee_w_1_pool = [2.7, 2.6, 2.6, 2.5, 2.5]
banerjee_w_learn_pool = [2.55, 2.5, 2.4, 2.4, 2.3]
banerjee_w_learn_pool_idle =[2.5, 2.55, 2.55, 2.5, 2.5]
banerjee_w_learn_pool_idle_learn = [2.5, 2.6, 2.5, 2.6, 2.8]

#code
fig, ax = plt.subplots()
ax.plot(driver_num, banerjee_w_1, 'cd-', label='SMW')
ax.plot(driver_num, banerjee_w_1_pool, 'gp-', label='SMW+CP')
ax.plot(driver_num, banerjee_w_learn_pool, 'b*-', label='ARDL+CP')
ax.plot(driver_num, banerjee_w_learn_pool_idle, 'r^-', label='ARDL+CP+GIM')
ax.plot(driver_num, banerjee_w_learn_pool_idle_learn, 'ko-', label='ARDL+CP+LIM')
ax.set_xlabel('The Number of Taxi', fontsize=frontsize)
ax.set_xticks(driver_num)
ax.set_xticklabels(('116', '166', '216', '266', '316'), fontsize=frontsize)

ax.set_yticks(detour)
ax.set_yticklabels(detour_str, fontsize=frontsize)
ax.set_ylabel('The Average Detour Time of Rider', fontsize=frontsize)
ax.legend(prop={'size': 11})
plt.show()




