#Simulation
FILENAME_R = "C:/Users/a02231961/PycharmProjects/Ph.D.-Research-Project-2/data/Chicago_rider_test.csv"
FILENAME_D = "C:/Users/a02231961/PycharmProjects/Ph.D.-Research-Project-2/data/Chicago_driver_test.csv"
SIMULATION_CYCLE = 3  #every 3 minutes in one cycle
SIMULATION_CYCLE_START = 0
SIMULATION_CYCLE_END = 100
RIDER_ROW_START = 0
RIDER_ROW_END = 29#13404
SHOWN_INTERVAL = 10

BUSIEST_ZONE = 1000
BUSIER_ZONE = 600
BUSY_ZONE = 200
COMMON_ZONE = 50


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
SAT_PRICE = 1.5
SAT_TIME = 0.8
PATIENCE = 7

#Driver Para
VEHICLE_CAPACITY = 4
IDLE = 'idle'
INSERVICE ='inservice'
COST_PER_CYCLE = 0.3 * SIMULATION_CYCLE
PICKUP="pickup"
DROPOFF="dropoff"




