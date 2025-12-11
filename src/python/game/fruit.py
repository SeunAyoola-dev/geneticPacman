import pygame 
from entity import Entity 
from constants import * 

class Fruit(Entity):
    def __init__(self, node):
        super().__init__(node)
        self.name = FRUIT
        self.color = GREEN
        self.lifespan = 5
        self.timer = 0
        self.destroy = False
        self.points = 100
        self.setBetweenNodes(RIGHT)
        
    def setBetweenNodes(self, direction):
            if self.node.neighbors[direction] is not None:
                self.target = self.node.neighbors[direction]
                self.position = (self.node.position + self.target.position) / 2.0

