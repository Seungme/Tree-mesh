from math import *
from typing import NamedTuple

import numpy as np


class Path(NamedTuple):
    old_coord: list = []
    new_coord: list = []
    width: float = 0.0

class Turtle:

    def __init__(self):
        self.basis = np.array([[0.0,0.0,-1.0], [0.0,1.0,0.0], [1.0,0.0,0.0]])
        self.coord = np.array([0.0,0.0,0.0])
        self.pen = True
        self.width = 0.001
        self.stack = []
        self.path = []

    def set_pen(self, condition):
        self.pen = condition

    def set_width(self, width):
        self.width = width

    def move(self, distance):
        distance = float(distance)
        new_coord = self.coord + self.basis[0] * distance
        coord = new_coord.copy()
        if self.pen == True:
            path = Path(self.coord.tolist(), new_coord.tolist(), self.width)
            self.path.append(path)
        self.coord = new_coord

    def turn(self, angle):
        angle = float(angle)
        radian = radians(angle)
        x = (cos(radian) * self.basis[0]) + (sin(radian) * self.basis[1])
        y = (-sin(radian) * self.basis[0]) + (cos(radian) * self.basis[1])
        self.basis[0] = x
        self.basis[1] = y

    def pitch(self, angle):
        angle = float(angle)
        radian = radians(angle)
        x = (cos(radian) * self.basis[0]) + (-sin(radian) * self.basis[2])
        z = (sin(radian) * self.basis[0]) + (cos(radian) * self.basis[2])
        self.basis[0] = x
        self.basis[2] = z

    def roll(self, angle):
        angle = float(angle)
        radian = radians(angle)
        y = (cos(radian) * self.basis[1]) + (sin(radian) * self.basis[2])
        z = (-sin(radian) * self.basis[1]) + (cos(radian) * self.basis[2])
        self.basis[1] = y
        self.basis[2] = z

    def save(self):
        self.stack.append(self.basis.copy())
        self.stack.append(self.coord.copy())
        self.stack.append(self.width)

    def restore(self):
        self.width = self.stack.pop()
        self.coord = self.stack.pop()
        self.basis = self.stack.pop()
