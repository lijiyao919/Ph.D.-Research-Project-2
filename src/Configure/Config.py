#Util For generate
REQ_DATE = 12
REQ_NUM = 62019
FILENAME_Chicago = "C:/Users/a02231961/PycharmProjects/Ph.D.-Research-Project-2/data/Chicago_April_" + str(REQ_DATE) + "_2016.csv"
POPULARITY_SCORE_FILE = 'C:/Users/a02231961/PycharmProjects/Ph.D.-Research-Project-2/data/data_2.json'
BEGIN_TIME = 0
END_TIME = 479

#Simulation
FILENAME_D = "C:/Users/a02231961/PycharmProjects/Ph.D.-Research-Project-2/data/Chicago_d_116.csv"
FILENAME_R = "C:/Users/a02231961/PycharmProjects/Ph.D.-Research-Project-2/data/Chicago_r_4_" + str(REQ_DATE) + "_2016.csv"
SAVE_PATH = "C:/Users/a02231961/PycharmProjects/Ph.D.-Research-Project-2/fig/p_{}.jpg"
SIMULATION_CYCLE = 3  #every 3 minutes in one cycle
SIMULATION_CYCLE_START = 220
SIMULATION_CYCLE_END = 491
RIDER_ROW_START = 18255 #16250 #11AM
RIDER_ROW_END = 62019 #57172 # 23:45PM
SHOWN_INTERVAL = 10
BENERJEE_W_1 = True


#Rider Para
WAITING = "waiting"
SERVING  = "serving"
FINISHED = "finished"
CANCEL = "cancel"

DETOUR_WEIGH = 0.2
DISCOUNT_1 = 1
DISCOUNT_2 = 1
DISCOUNT_3 = 1
DISCOUNT_4 = 1

DIR_THRESHOLD = 30
SAT_PRICE = 1
PATIENCE = 7

#Driver Para
VEHICLE_CAPACITY = 4
IDLE = 'idle'
INSERVICE ='inservice'
COST_PER_CYCLE = 2
PICKUP="pickup"
DROPOFF="dropoff"



