from math import *
from typing import NamedTuple

import numpy as np


class Path(NamedTuple):
    old_coord: list = []
    new_coord: list = []
    width: float = 0.0

class Turtle:

    def __init__(self, coord, basis):
        self.basis = basis #p.array([[0.0,0.0,1.0], [0.0,1.0,0.0], [1.0,0.0,0.0]])
        self.coord = coord #np.array([0.0,0.0,0.0])
        self.pen = True
        self.width = 0.001
        self.stack = []
        self.path = []
        self.current_polygone = []
        self.polygones = []
        self.polygone_stack = []
        self.lines = []
        self.leaf = []
        self.flower = []
        self.fruit = []

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

    def new_vertex(self):
        self.current_polygone.append(self.coord.tolist())

    def move_polygone(self, distance):
        distance = float(distance)
        new_coord = self.coord + self.basis[0] * distance
        line = [self.coord.tolist(), new_coord.tolist()]
        self.lines.append(line)
        self.coord = new_coord

    def save_polygone(self):
        self.polygone_stack.append(self.current_polygone.copy())
        self.current_polygone = []

    def restore_polygone(self):
        self.polygones.append(self.current_polygone)
        self.current_polygone = self.polygone_stack.pop()

    def save_leaf(self):
        self.leaf.append(self.coord);
        self.leaf.append(self.basis);

    def save_flower(self):
        self.flower.append(self.coord);
        self.flower.append(self.basis);

    def save_fruit(self):
        self.fruit.append(self.coord);
        self.fruit.append(self.basis);
