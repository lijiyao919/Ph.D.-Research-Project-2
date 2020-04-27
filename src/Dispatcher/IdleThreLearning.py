import random
import json
import numpy as np
import os.path
from src.Configure.Config import *

class IdleThreLearning:
    def __init__(self):
        self.Q = {}
        self.Act_last = []
        self.ThreValue = [0, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5]
        self.last_time = SIMULATION_CYCLE_START

        for i in range(0,78):
            self.Act_last.append(0)

        if os.path.exists(Q_TABLE_PATH):
            self.load()
        else:
            print("Initialize Q Table")
            for time in range(SIMULATION_CYCLE_START, SIMULATION_CYCLE_END):
                for loc in range(1, 78):
                    s=(time,loc)
                    self.Q[s]=np.zeros(len(self.ThreValue))



    def selectThreValue(self, S):
        if random.uniform(0, 1) < EPSILON:
            self.Act_last[S[1]] = random.randint(0, len(self.ThreValue) - 1)
        else:
            self.Act_last[S[1]] = np.argmax(self.Q[S])
        return self.ThreValue[self.Act_last[S[1]]]


    def estimate_last_QLearning(self, R, curr_time):
        if curr_time > SIMULATION_CYCLE_START:
            print(R)
            for loc in range(1, 78):
                S_last=(self.last_time, loc)
                S=(curr_time,loc)
                self.Q[S_last][self.Act_last[S[1]]] = self.Q[S_last][self.Act_last[S[1]]] + ALPHA * (R + GAMMA * np.max(self.Q[S]) - self.Q[S_last][self.Act_last[S[1]]])
                print(str(S_last) + ': ' + str(self.Q[S_last]))
            self.last_time = curr_time
        if curr_time == SIMULATION_CYCLE_END-1:
            self.save()

    def save(self):
        data = [{'key': k, 'value': v.tolist()} for k, v in self.Q.items()]
        # print('save:', data)
        with open(Q_TABLE_PATH, 'w') as fp:
            json.dump(data, fp)
        print('Save Done!')

    def load(self):
        print('Loading......')
        with open(Q_TABLE_PATH, 'r') as fp:
            data = json.load(fp)
        for elem in data:
            S = tuple(elem['key'])
            self.Q[S] = np.array(elem['value'])



