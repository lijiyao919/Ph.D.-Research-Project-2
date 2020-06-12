import random
import json
import numpy as np
from src.Configure.Config import *
from src.Logger.Logger import Logger
import logging

class IdleMoveLearner:
    Q = {}
    timestamp = -1

    def __init__(self):
        self.last_state = None
        self.act = None
        self.__logger = Logger('IdleMoveLearner')
        self.__logger.setLevel(logging.DEBUG)

    def convert(self, S):
        zone_differ = round(float(S[2]), 2)
        state = (S[0], S[1], zone_differ)
        # print(state)
        return state

    def checkQ(self, S):
        state = self.convert(S)
        if state not in IdleMoveLearner.Q:
            IdleMoveLearner.Q[state] = np.array([0.0, 0.0])


    def selectAction(self, S):
        S=self.convert(S)
        if random.uniform(0, 1) < EPSILON or S not in IdleMoveLearner.Q:
            self.act = random.choice([0, 1])
            self.__logger.info(IdleMoveLearner.timestamp, "selectAction", None, None, "Select action randomly")
        else:
            self.act = np.argmax(IdleMoveLearner.Q[S])
            self.__logger.info(IdleMoveLearner.timestamp, "selectAction", None, None, "Select action from Q table")
        return self.act

    def runQLearning(self, R, curr_time, curr_loc, curr_diff):
        if self.last_state is not None and self.act is not None and self.last_state[0] == IdleMoveLearner.timestamp-1:
            S=(curr_time, curr_loc, curr_diff)
            S=self.convert(S)
            self.checkQ(S)
            if R is None:
                if self.act == 0:
                    R=-1
                else:
                    if IdleMoveLearner.timestamp >= 480:
                        R=-200
                    else:
                        R=-2
            IdleMoveLearner.Q[self.last_state][self.act] = IdleMoveLearner.Q[self.last_state][self.act] \
                                                           + ALPHA * (R + GAMMA * np.max(IdleMoveLearner.Q[S]) - IdleMoveLearner.Q[self.last_state][self.act])
            self.last_state = S
            self.__logger.info(IdleMoveLearner.timestamp, "runQLearning", None, None, "Leaning Q table")
        else:
            self.last_state = self.convert((curr_time, curr_loc, curr_diff))
            self.checkQ(self.last_state)

    @staticmethod
    def save():
        data = [{'key': k, 'value': v.tolist()} for k, v in IdleMoveLearner.Q.items()]
        #print('save:', data)
        with open(Q_TABLE_PATH, 'w') as fp:
            json.dump(data, fp, cls=MyEncoder)
        print('Save Done!')

    @staticmethod
    def load():
        print('Loading......')
        with open(Q_TABLE_PATH, 'r') as fp:
            data = json.load(fp)
        for elem in data:
            S = tuple(elem['key'])
            IdleMoveLearner.Q[S] = np.array(elem['value'])


class MyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        else:
            return super(MyEncoder, self).default(obj)



