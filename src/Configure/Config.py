#Simulation
FILENAME_D = "C:/Users/a02231961/PycharmProjects/Ph.D.-Research-Project-2/data/Chicago_d.csv"
FILENAME_R = "C:/Users/a02231961/PycharmProjects/Ph.D.-Research-Project-2/data/Chicago_r.csv"
SAVE_PATH = "C:/Users/a02231961/PycharmProjects/Ph.D.-Research-Project-2/fig/p_{}.jpg"
SIMULATION_CYCLE = 3  #every 3 minutes in one cycle
SIMULATION_CYCLE_START = 220
SIMULATION_CYCLE_END = 491
RIDER_ROW_START = 16250 #11AM
RIDER_ROW_END = 57172 # 23:45PM
SHOWN_INTERVAL = 490 #10
BENERJEE_W_1 = False


#Rider Para
WAITING = "waiting"
SERVING  = "serving"
FINISHED = "finished"
CANCEL = "cancel"

DETOUR_WEIGH = 0.05
DISCOUNT_1 = 0.96
DISCOUNT_2 = 0.93
DISCOUNT_3 = 0.9
DISCOUNT_4 = 0.87

DIR_THRESHOLD = 30
SAT_PRICE = 1
PATIENCE = 7

#Driver Para
VEHICLE_CAPACITY = 4
IDLE = 'idle'
INSERVICE ='inservice'
COST_PER_CYCLE = 1.8
PICKUP="pickup"
DROPOFF="dropoff"
#IDLE_MOVE_THRE_LEARN = True

#Util
FILENAME_Chicago = "C:/Users/a02231961/PycharmProjects/Ph.D.-Research-Project-2/data/Chicago_April_11_2016.csv"
BEGIN_TIME = 0
END_TIME = 479
SMOOTH_RATOR = 0.5
BASE_ZONE = 32

#Learning
EPSILON= 0.1#0.03
GAMMA = 0.9
ALPHA = 0.1
Q_TABLE_PATH = '../data/qtable.json'


