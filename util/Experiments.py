import matplotlib.pyplot as plt
import numpy as np


driver_num = np.array([116, 166, 216, 266, 316])

#serving rate
'''serving_rate=[20, 30, 40, 50, 60, 70, 80, 90]
serving_rate_str=('20', '30', '40', '50', '60', '70', '80', '90')
#banerjee_w_1= [21, 31, 38, 43, 48]
banerjee_w_1_pool = [34, 46, 54, 59, 63]
#banerjee_w_learn_pool = [38, 54, 65, 73, 78]
banerjee_w_learn_pool_idle =[39, 53, 62, 68, 76]
banerjee_w_learn_pool_idle_learn = [45, 58, 71, 82, 87]'''

#driver utilization
'''utilization=[50, 60, 70, 80, 90]
utilization_str=('50', '60', '70', '80', '90')
#banerjee_w_1= [86, 83, 78, 73, 68]
banerjee_w_1_pool = [73, 71, 65, 56, 50]
#banerjee_w_learn_pool = [79, 79, 72, 66, 59]
banerjee_w_learn_pool_idle =[83, 81, 73, 68, 58]
banerjee_w_learn_pool_idle_learn = [89, 85, 78, 71, 63]'''

#driver profit
profit=[200, 300, 400, 500, 600, 700, 800, 900, 1000, 1100]
profit_str=('200', '300', '400', '500', '600', '700', '800', '900', '1000', '1100')
#banerjee_w_1= [244, 260, 275, 267, 256]
banerjee_w_1_pool = [728, 768, 738, 665, 602]
#banerjee_w_learn_pool = [780, 886, 812, 749, 676]
banerjee_w_learn_pool_idle =[917, 974, 850, 770, 690]
banerjee_w_learn_pool_idle_learn = [1127, 1054, 1014, 879, 727]

#platform revenue
'''revenue=[20000, 40000, 60000, 80000, 100000, 120000, 140000, 160000]
revenue_str=('20K', '40K', '60K', '80K', '100K', '120K', '140K', '160K')
banerjee_w_1= np.array([842.61, 859.95, 861.75, 818.38, 776.87])*0.3*driver_num
#banerjee_w_1_pool = np.array([1592.42, 1620.29, 1534.34, 1380.65, 1250.76])*0.3*driver_num
#banerjee_w_learn_pool = np.array([1680.04, 1834.25, 1676.67, 1546.63, 1402.58])*0.3*driver_num
banerjee_w_learn_pool_idle =np.array([1976.09, 2038.54, 1819.99, 1682.49, 1523.09])*0.3*driver_num
banerjee_w_learn_pool_idle_learn = np.array([2316.41, 2197, 2137, 1929, 1679])*0.3*driver_num'''

#rider call time
'''call=[3, 3.5, 4, 4.5, 5, 5.5,6]
call_str=( '3.0', '3.5', '4.0', '4.5', '5.0', '5.5', '6.0')
banerjee_w_1= [5.88, 5.4, 5.1, 4.8, 4.6]
#banerjee_w_1_pool = [2.88, 2.5, 1.98, 1.5, 1.4]
#banerjee_w_learn_pool = [2.84, 2.34, 1.95, 1.5, 1.1]
banerjee_w_learn_pool_idle =[5.2, 4.6, 4.2, 3.8, 3.4]
banerjee_w_learn_pool_idle_learn = [5.4, 4.6, 4.4, 3.6, 3]'''

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
ax.plot(angle_num, pool_in_4, 'gp-', label='pool_fraction(4)')
ax.plot(angle_num, pool_in_3, 'b*-', label='pool_fraction(3)')
ax.plot(angle_num, pool_in_2, 'r^-', label='pool_fraction(2)')
ax.plot(angle_num, pool_in_1, 'ko-', label='pool_fraction(1)')
ax.set_xlabel(r"$\theta_{CTR}$", fontsize=frontsize)
ax.set_xticks(angle_num)
ax.set_xticklabels(('5', '10', '20', '30', '40'), fontsize=frontsize)
ax.set_yticks(pool_rate)
ax.set_yticklabels(pool_rate_str, fontsize=frontsize)
ax.set_ylabel('The Pool Fraction (%)', fontsize=frontsize)
ax.legend(prop={'size': 16})
plt.show()'''

#unserve rider
'''angle_num = [5, 10 ,20 ,30 ,40]
unserive=[6.31, 3.56, 2.66, 2.48, 2]
fig, ax = plt.subplots()
frontsize=20
ax.plot(angle_num, unserive, 'rp-')
ax.set_xlabel(r"$\theta_{CTR}$", fontsize=frontsize)
ax.set_xticks(angle_num)
ax.set_xticklabels(('5', '10', '20', '30', '40'), fontsize=frontsize)
ax.set_yticks((0, 1, 2, 3, 4, 5, 6, 7))
ax.set_yticklabels(('0', '1', '2', '3', '4', '5', '6', '7'), fontsize=frontsize)
ax.set_ylabel('Unserved Riders (%)', fontsize=frontsize)
plt.show()'''


# Extra trip and saved money
'''angle_num = [5, 10 ,20 ,30 ,40]
detour=[2, 2.2, 2.5, 2.8, 3]
detour_str=('2', '2.2', '2.5', '2.8', '3')
save=[2, 2.2, 2.5, 2.8, 3]
save_str=('2', '2.2', '2.5', '2.8', '3')

frontsize=15
wait=[2.1, 2.3, 2.5, 2.7, 2.9]
save=[2, 2.2, 2.7, 3.2, 3.3]
fig, ax = plt.subplots()
ax.plot(angle_num, wait, 'ko-', label='Extra Trip Time')
ax.set_xlabel(r"$\theta_{CTR}$", fontsize=frontsize)
ax.set_xticks(angle_num)
ax.set_xticklabels(('5', '10', '20', '30', '40'), fontsize=18)
ax.set_yticks(detour)
ax.set_yticklabels(detour_str, fontsize=18)
ax.set_ylabel('The Average Extra Trip Time of Rider (min)', fontsize=frontsize)
plt.show()

fig, ax2 = plt.subplots()
ax2.plot(angle_num, save, 'bd-',label='Saved Money')
ax2.set_xlabel(r"$\theta_{CTR}$", fontsize=frontsize)
ax2.set_xticks(angle_num)
ax2.set_xticklabels(('5', '10', '20', '30', '40'), fontsize=18)
ax2.set_yticks(save)
ax2.set_yticklabels(save_str, fontsize=18)
ax2.set_ylabel('The Average Saved Money of Rider ($)', fontsize=frontsize)
plt.show()'''

#lottery
'''labels = ['116', '166', '216', '266', '316']
lottery_noused = [22764, 15900, 8497, 3080, 1028]
lottery_used =   [21287, 14885, 7515, 2813, 967]
x = np.arange(len(labels))  # the label locations
y = np.arange(6)
width = 0.38  # the width of the bars

fig, ax = plt.subplots()
rects1 = ax.bar(x - width/2, lottery_noused, width, label='LS Not Used')
rects2 = ax.bar(x + width/2, lottery_used, width, label='LS Used')

# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_xlabel('The Number of Taxis', fontsize=frontsize)
ax.set_xticks(x)
ax.set_xticklabels(('116', '166', '216', '266', '316'), fontsize=18)

ax.set_ylabel('The Number of Unserved Riders', fontsize=frontsize)
ax.set_yticks([0, 5000, 10000, 15000, 20000, 25000])
ax.set_yticklabels(('0','5000', '10000', '15000', '20000', '25000'), fontsize=18)
ax.legend()

def autolabel(rects, pos='center'):
    """Attach a text label above each bar in *rects*, displaying its height."""
    for rect in rects:
        height = rect.get_height()
        ax.annotate('{}'.format(height),
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha=pos, va='bottom', fontsize=14)


autolabel(rects1)
autolabel(rects2, 'left')

fig.tight_layout()

plt.show()'''

#code for compare
frontsize=20
fig, ax = plt.subplots()
#ax.plot(driver_num, banerjee_w_1, 'cd-', label='SMW')
ax.plot(driver_num, banerjee_w_1_pool, 'gp-', label='SMW+CIP')
#ax.plot(driver_num, banerjee_w_learn_pool, 'b*-', label='ARDL+CP')
ax.plot(driver_num, banerjee_w_learn_pool_idle, 'ko-', label='Hybrid Solution')
ax.plot(driver_num, banerjee_w_learn_pool_idle_learn, 'ro-', label='T-Balance')
ax.set_xlabel('The Number of Taxis', fontsize=frontsize)
ax.set_xticks(driver_num)
ax.set_xticklabels(('116', '166', '216', '266', '316'), fontsize=frontsize)

ax.set_yticks(utilization)
ax.set_yticklabels(utilization_str, fontsize=frontsize)
ax.set_ylabel('The Taxi Utilization (%)', fontsize=16)
ax.legend(prop={'size': 12})
plt.show()













