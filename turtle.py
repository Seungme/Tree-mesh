from math import *

import numpy as np


class Turtle:

    def __init__(self):
        self.basis = np.array([[1,0,0], [0,1,0], [0,0,1]])
        self.coord = np.array([0,0,0])
        self.pen = True
        self.width = 1
        self.stack = []
        self.path = []

    def move(self, distance):
        new_coord = self.coord + self.basis[0] * distance
        if self.pen == True:
            path.append([self.coord, new_coord])
        self.coord = new_coord

    def turn(self, angle):
        radian = math.radians(angle)
        x = (cos(radian) * self.basis[0]) + (sin(radian) * self.basis[1])
        y = (-sin(radian) * self.basis[0]) + (cos(radian) * self.basis[1])
        self.basis[0] = x
        self.basis[1] = y

    def pitch(self, angle):
        radian = math.radians(angle)
        x = (cos(radian) * self.basis[0]) + (-sin(radian) * self.basis[2])
        z = (sin(radian) * self.basis[0]) + (cos(radian) * self.basis[2])
        self.basis[0] = x
        self.basis[2] = z

    def roll(self, angle):
        radian = math.radians(angle)
        y = (cos(radian) * self.basis[1]) + (sin(radian) * self.basis[2])
        z = (-sin(radian) * self.basis[1]) + (cos(radian) * self.basis[2])
        self.basis[1] = y
        self.basis[2] = z

    def save(self):
        self.stack.append(self)

    def restore(self):
        self = self.stack.pop()
