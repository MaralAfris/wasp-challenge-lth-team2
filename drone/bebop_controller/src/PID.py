from copy import deepcopy
import numpy

from PIDParameters import *


class PID(object):


    def __init__(self):
        p = PIDParameters()
        p.Beta = 1.0
        p.H = 0.05
        p.integratorOn = False
        p.K = 0.25 # start 0.1 # used to be 0.20
        p.N = 10
        p.Td = 0.0 # start 0.1
        p.Ti = 30 # used to be 10
        p.Tr = 30 # used to be 10
        self.p = deepcopy(p)

        self.I = 0.0 
        self.D = 0.0 
        self.v = 0.0 
        self.e = 0.0 
        self.y = 0.0 
        self.yold = 0.0
        self.ad = self.p.Td / (self.p.Td + self.p.N*self.p.H)
        self.bd = self.p.K * self.ad * self.p.N


    def calculate_output(self, y, yref):
        self.y = deepcopy(y)
        self.yref = deepcopy(yref)
        self.e = yref - y
        self.D = self.ad*self.D - self.bd * (y - self.yold)
        self.v = self.p.K*(self.p.Beta*yref - y) + self.I + self.D
        return deepcopy(self.v)

    def update_state(self, u):
        if self.p.integratorOn:
            self.I = self.I + (self.p.K*self.p.H/self.p.Ti)*self.e + (self.p.H/self.p.Tr)*(self.u - self.v)
        else:
            self.I = 0.0
        self.yold = self.y


    def set_parameters(self, param):
        self.p = deepcopy(param)
        self.ad = self.p.Td / (self.p.Td + self.p.N*self.p.H)
        self.bd = self.p.K * self.ad * self.p.N
        if not self.p.integratorOn:
            self.I = 0.0

    def reset(self):
        self.I = 0.0
        self.D = 0.0
        self.yold = 0.0

    def get_parameters(self):
        return deepcopy(self.p)
                
