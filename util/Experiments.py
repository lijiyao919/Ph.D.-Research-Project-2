import matplotlib.pyplot as plt
import numpy as np

frontsize=14
driver_num = [116, 166, 216, 266, 316]

#serving rate
'''serving_rate=[20, 30, 40, 50, 60, 70, 80, 90, 100]
serving_rate_str=('20', '30', '40', '50', '60', '70', '80', '90', '100')
banerjee_w_1= [21, 31, 38, 43, 48]
banerjee_w_1_pool = [36, 49, 58, 65, 70]
banerjee_w_learn_pool = [38, 54, 65, 74, 78]
banerjee_w_learn_pool_idle =[43, 60, 71, 81, 87]
banerjee_w_learn_pool_idle_learn = [45, 61, 79, 93, 98]'''

#driver revenue
'''revenue=[800, 1000, 1200, 1400, 1600, 1800, 2000, 2200, 2400]
revenue_str=('800', '1000', '1200', '1400', '1600', '1800', '2000', '2200', '2400')
banerjee_w_1= [981, 981, 972, 921, 874]
banerjee_w_1_pool = [1893, 1940, 1816, 1634, 1478]
banerjee_w_learn_pool = [1945, 2156, 1966, 1826, 1638]
banerjee_w_learn_pool_idle =[2334, 2421, 2182, 2000, 1822]
banerjee_w_learn_pool_idle_learn = [2389, 2496, 2381, 2298, 2075]'''

#driver_effort
'''effort=[140, 160, 180, 200, 220, 240]
effort_str=('140', '160', '180', '200', '220', '240')
banerjee_w_1= [173, 170, 164, 153, 144]
banerjee_w_1_pool = [194, 184, 168, 151, 137]
banerjee_w_learn_pool = [197, 199, 182, 168, 151]
banerjee_w_learn_pool_idle =[233, 228, 213, 204, 188]
banerjee_w_learn_pool_idle_learn = [240, 239, 238, 235, 225]'''

#driver profit
'''profit=[600, 800, 1000, 1200, 1400, 1600, 1800, 2000]
profit_str=('600', '800', '1000', '1200', '1400', '1600', '1800', '2000')
banerjee_w_1= [635, 639, 644, 615, 586]
banerjee_w_1_pool = [1505, 1572, 1480, 1331, 1203]
banerjee_w_learn_pool = [1551, 1758, 1603, 1489, 1335]
banerjee_w_learn_pool_idle =[1867, 1966, 1756, 1592, 1446]
banerjee_w_learn_pool_idle_learn = [1908, 2016, 1904, 1829, 1625]'''

#driver utilization
utilization=[50, 60, 70, 80, 90, 100]
utilization_str=('50', '60', '70', '80', '90', '100')
banerjee_w_1= [86, 83, 78, 73, 68]
banerjee_w_1_pool = [78, 74, 67, 59, 53]
banerjee_w_learn_pool = [79, 79, 72, 66, 59]
banerjee_w_learn_pool_idle =[90, 88, 79, 71, 64]
banerjee_w_learn_pool_idle_learn = [93, 90, 86, 80, 71]

#rider call time
'''call=[0.5, 1, 1.5, 2, 2.5, 3, 3.5]
call_str=('0.5', '1', '1.5', '2', '2.5', '3', '3.5')
banerjee_w_1= [3.48, 3, 2.7, 2.4, 2.2]
banerjee_w_1_pool = [2.88, 2.5, 1.98, 1.6, 1.4]
banerjee_w_learn_pool = [2.82, 2.34, 1.92, 1.5, 1.1]
banerjee_w_learn_pool_idle =[2.8, 2.2, 1.8, 1.4, 1]
banerjee_w_learn_pool_idle_learn = [2.8, 2.1, 1.8, 1.2, 0.54]'''

#rider detour time
'''detour=[0.5, 1, 1.5, 2, 2.5, 3, 3.5]
detour_str=('0.5', '1', '1.5', '2', '2.5', '3', '3.5')
banerjee_w_1= [2.55, 2.2, 2.0, 2.0, 2.0]
banerjee_w_1_pool = [2.7, 2.6, 2.6, 2.5, 2.5]
banerjee_w_learn_pool = [2.55, 2.5, 2.4, 2.4, 2.3]
banerjee_w_learn_pool_idle =[2.5, 2.55, 2.55, 2.5, 2.5]
banerjee_w_learn_pool_idle_learn = [2.5, 2.6, 2.5, 2.6, 2.8]'''

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

ax.set_yticks(call)
ax.set_yticklabels(call_str, fontsize=frontsize)
ax.set_ylabel('The Average Calling Time of Rider', fontsize=frontsize)
ax.legend(prop={'size': 11})
plt.show()




