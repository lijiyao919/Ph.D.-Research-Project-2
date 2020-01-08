#Simulation
FILENAME_R = "C:/Users/a02231961/PycharmProjects/Ph.D.-Research-Project-2/data/Chicago_April_11_2016.csv"
FILENAME_D = "C:/Users/a02231961/PycharmProjects/Ph.D.-Research-Project-2/data/Chicago_d.csv"
SIMULATION_CYCLE = 3  #every 3 minutes in one cycle
SIMULATION_CYCLE_START = 220 #11AM
SIMULATION_CYCLE_END = 491
RIDER_ROW_START = 16250
RIDER_ROW_END = 57172 # 23:45PM
SHOWN_INTERVAL = 10
BENERJEE = False

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
COST_PER_CYCLE = 0.1 * SIMULATION_CYCLE
PICKUP="pickup"
DROPOFF="dropoff"




