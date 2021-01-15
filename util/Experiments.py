import matplotlib.pyplot as plt
import numpy as np


driver_num = np.array([116, 166, 216, 266, 316])

#serving rate
'''serving_rate=[20, 30, 40, 50, 60, 70, 80, 90, 100]
serving_rate_str=('20', '30', '40', '50', '60', '70', '80', '90', '100')
banerjee_w_1= [21, 31, 38, 43, 48]
#banerjee_w_1_pool = [36, 49, 58, 65, 70]
#banerjee_w_learn_pool = [38, 54, 65, 73, 78]
banerjee_w_learn_pool_idle =[43, 60, 71, 81, 87]
banerjee_w_learn_pool_idle_learn = [48, 64, 82, 93, 98]'''

#driver utilization
'''utilization=[60, 70, 80, 90, 95]
utilization_str=('60', '70', '80', '90', '95')
banerjee_w_1= [86, 83, 78, 73, 68]
#banerjee_w_1_pool = [78, 73, 67, 59, 53]
#banerjee_w_learn_pool = [79, 79, 72, 66, 59]
banerjee_w_learn_pool_idle =[90, 87, 79, 72, 64]
banerjee_w_learn_pool_idle_learn = [94, 90, 87, 80, 71]'''

#driver profit
'''profit=[200, 300, 400, 500, 600, 700, 800, 900, 1000, 1100]
profit_str=('200', '300', '400', '500', '600', '700', '800', '900', '1000', '1100')
banerjee_w_1= [244, 260, 275, 267, 256]
#banerjee_w_1_pool = [728, 768, 738, 665, 602]
#banerjee_w_learn_pool = [780, 886, 812, 749, 676]
banerjee_w_learn_pool_idle =[917, 974, 850, 770, 690]
banerjee_w_learn_pool_idle_learn = [1127, 1054, 1014, 879, 727]'''

#platform revenue
'''revenue=[20000, 40000, 60000, 80000, 100000, 120000, 140000, 160000]
revenue_str=('20K', '40K', '60K', '80K', '100K', '120K', '140K', '160K')
banerjee_w_1= np.array([842.61, 859.95, 861.75, 818.38, 776.87])*0.3*driver_num
#banerjee_w_1_pool = np.array([1592.42, 1620.29, 1534.34, 1380.65, 1250.76])*0.3*driver_num
#banerjee_w_learn_pool = np.array([1680.04, 1834.25, 1676.67, 1546.63, 1402.58])*0.3*driver_num
banerjee_w_learn_pool_idle =np.array([1976.09, 2038.54, 1819.99, 1682.49, 1523.09])*0.3*driver_num
banerjee_w_learn_pool_idle_learn = np.array([2316.41, 2197, 2137, 1929, 1679])*0.3*driver_num'''

#rider call time
call=[1, 1.5, 2, 2.5, 3, 3.5]
call_str=( '1', '1.5', '2', '2.5', '3', '3.5')
banerjee_w_1= [3.48, 3, 2.7, 2.4, 2.2]
banerjee_w_1_pool = [2.88, 2.5, 1.98, 1.5, 1.4]
banerjee_w_learn_pool = [2.84, 2.34, 1.95, 1.5, 1.1]
banerjee_w_learn_pool_idle =[2.8, 2.2, 1.8, 1.4, 1]
banerjee_w_learn_pool_idle_learn = [3, 2.2, 1.8, 1.2, 0.6]

#driver revenue
'''revenue=[800, 1000, 1200, 1400, 1600, 1800, 2000]
revenue_str=('800', '1000', '1200', '1400', '1600', '1800', '2000')
banerjee_w_1= [842.61, 859.95, 861.75, 818.38, 776.87]
banerjee_w_1_pool = [1592.42, 1620.29, 1534.34, 1380.65, 1250.76]
banerjee_w_learn_pool = [1680.04, 1834.25, 1676.67, 1546.63, 1402.58]
banerjee_w_learn_pool_idle =[1976.09, 2038.54, 1819.99, 1682.49, 1523.09]
banerjee_w_learn_pool_idle_learn = [2030.41, 2089.88, 1996.61, 1894.9, 1677.12]'''

#driver_effort
'''effort=[140, 160, 180, 200, 220, 240]
effort_str=('140', '160', '180', '200', '220', '240')
banerjee_w_1= [173, 170, 164, 153, 144]
banerjee_w_1_pool = [193, 183, 168, 151, 137]
banerjee_w_learn_pool = [198, 199, 182, 167, 152]
banerjee_w_learn_pool_idle =[234, 228, 212, 204, 188]
banerjee_w_learn_pool_idle_learn = [240, 239, 238, 235, 225]'''


#Poolability
'''angle_num = [5, 10 ,20 ,30 ,40]
pool_rate=[10, 20, 30, 40, 50, 60]
pool_rate_str=('10', '20', '30', '40', '50', '60')
pool_in_4 = [26.5, 35,   47.4, 56.2, 61.3]
pool_in_3 = [13.2, 14.7, 14.2, 12.7, 11.5]
pool_in_2 = [22,   20.7, 17.4, 13.9, 12.1]
pool_in_1 = [38.4, 29.6, 21,   17.2, 15.1]
fig, ax = plt.subplots()
frontsize=20
ax.plot(angle_num, pool_in_4, 'gp-', label='Poolability at Level 4')
ax.plot(angle_num, pool_in_3, 'b*-', label='Poolability at Level 3')
ax.plot(angle_num, pool_in_2, 'r^-', label='Poolability at Level 2')
ax.plot(angle_num, pool_in_1, 'ko-', label='Poolability at Level 1')
ax.set_xlabel(r"$\theta_{CTR}$", fontsize=frontsize)
ax.set_xticks(angle_num)
ax.set_xticklabels(('5', '10', '20', '30', '40'), fontsize=frontsize)
ax.set_yticks(pool_rate)
ax.set_yticklabels(pool_rate_str, fontsize=frontsize)
ax.set_ylabel('The Poolability (%)', fontsize=frontsize)
ax.legend(prop={'size': 16})
plt.show()'''

# Extra trip and saved money
'''angle_num = [5, 10 ,20 ,30 ,40]
detour=[2, 2.2, 2.5, 2.8, 3]
detour_str=('2', '2.2', '2.5', '2.8', '3')
save=[2, 2.2, 2.5, 2.8, 3, 3.2]
save_str=('2', '2.2', '2.5', '2.8', '3', '3.2')'''

frontsize=15
'''wait=[2.1, 2.3, 2.5, 2.7, 2.9]
save=[2, 2.2, 2.7, 3.2, 3.3]
fig, ax = plt.subplots()
ax2 = ax.twinx()
ax.plot(angle_num, wait, 'ko-', label='Extra Trip Time')
ax2.plot(angle_num, save, 'bd-',label='Saved Money')
ax.set_xlabel(r"$\theta_{CTR}$", fontsize=frontsize)
ax.set_xticks(angle_num)
ax.set_xticklabels(('5', '10', '20', '30', '40'), fontsize=18)

ax.set_yticks(detour)
ax.set_yticklabels(detour_str, fontsize=18)
ax.set_ylabel('The Average Extra Trip Time of Rider (min)', fontsize=frontsize)
ax2.set_yticks(save)
ax2.set_yticklabels(save_str, fontsize=18)
ax2.set_ylabel('The Average Saved Money of Rider ($)', color='b', fontsize=frontsize)
ax.legend(prop={'size': 16}, loc='lower right')
ax2.legend(prop={'size': 16}, loc='upper left')
plt.show()'''

#lottery
'''multiplier_num = [0, 0.02, 0.04, 0.06, 0.08, 0.1]
lost_rate=[10, 20, 30, 40, 50, 60]
lost_rate_str=('10', '20', '30', '40', '50', '60')
driver_116 = [56, 53, 52, 52, 52, 52]
driver_166 = [39, 37, 37, 37, 36, 36]
driver_216 = [21, 19, 19, 19, 18, 18]
driver_266 = [8, 7, 7, 7, 7, 7]
driver_316 = [3, 2, 2, 2, 2, 2]
fig, ax = plt.subplots()
frontsize=20
ax.plot(multiplier_num, driver_316, 'ko-', label='driver#: 316')
ax.set_xlabel("multipiler", fontsize=frontsize)
ax.set_xticks(multiplier_num)
#ax.set_xticklabels(('0', '0.02', '0.04', '0.06', '0.08', '0.1'), fontsize=frontsize)
#ax.set_yticks(lost_rate)
#ax.set_yticklabels(lost_rate_str, fontsize=frontsize)
ax.set_ylabel('Lost Riders(%)', fontsize=frontsize)
ax.legend(prop={'size': 16})
plt.show()'''

#code for compare
frontsize=20
fig, ax = plt.subplots()
ax.plot(driver_num, banerjee_w_1, 'cd-', label='SMW')
#ax.plot(driver_num, banerjee_w_1_pool, 'gp-', label='SMW+CP')
#ax.plot(driver_num, banerjee_w_learn_pool, 'b*-', label='ARDL+CP')
ax.plot(driver_num, banerjee_w_learn_pool_idle, 'ko-', label='Hybrid Solution')
ax.plot(driver_num, banerjee_w_learn_pool_idle_learn, 'ro-', label='T-Balance')
ax.set_xlabel('The Number of Taxis', fontsize=frontsize)
ax.set_xticks(driver_num)
ax.set_xticklabels(('116', '166', '216', '266', '316'), fontsize=frontsize)

ax.set_yticks(call)
ax.set_yticklabels(call_str, fontsize=frontsize)
ax.set_ylabel('The Average Calling Time of Riders (min)', fontsize=16)
ax.legend(prop={'size': 12})
plt.show()












