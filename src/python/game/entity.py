import pygame 
from pygame.locals import *
from vectors import Vector2
from constants import *
from random import randint

class Entity(object):
    def __init__(self, node):
        self.name = None
        self.directions = {STOP:Vector2(0,0), UP:Vector2(0,-1), DOWN:Vector2(0,1), LEFT:Vector2(-1,0), RIGHT:Vector2(1,0)}
        self.direction = STOP
        self.node = node
        self.setSpeed(100)
        self.radius = 10
        self.collideRadius = self.radius / 2
        self.color = WHITE
        self.setPosition()
        self.target = node 
        self.visible = True
        self.disablePortal = False 
        self.goal = None 
        self.directionMethod = self.goalDirection
    
    def setSpeed(self, speed):
        self.speed = speed * TITLEWIDTH/16 # speed relative to the size of the maze
    
    def setPosition(self):
        self.position = self.node.position.copy()
        
    def validDirection(self, direction): 
        if direction is not STOP: 
            if self.node.neighbors[direction] is not None: 
                return True
        return False
    
    def getNewTarget(self, direction): 
        if self.validDirection(direction): 
            return self.node.neighbors[direction]
        return self.node
    
    def overshotTarget(self):
        if self.target is not None: 
            vec1 = self.target.position - self.node.position # vector from node to target
            vec2 = self.position - self.node.position # vector from node to self
            node2Target = vec1.length()
            node2Self = vec2.length()
            return node2Self >= node2Target
        return False
    
    def reverseDirection(self):
        self.direction *= -1
        temp = self.node
        self.node = self.target
        self.target = temp
        
    def oppositeDirection(self, direction):
        if direction is not STOP: 
            if direction == self.direction * -1: 
                return True
        return False
    
    def render(self, screen): 
        p = self.position.asInt()
        pygame.draw.circle(screen, self.color, p, self.radius)
        
    
    def validDirections(self):
        directions = [] 
        for key in self.directions.keys():
            if self.validDirection(key):
               if key != self.direction * -1:
                   directions.append(key)
        if len(directions) == 0:
            directions.append(self.direction * -1) # go the opposite way if no other options
        return directions 
    
    def randomDirection(self, directions):
        return directions[randint(0, len(directions)-1)]
                
    def update(self, dt):
        self.position += self.directions[self.direction] * self.speed * dt
        
        if self.overshotTarget():
            self.node = self.target 
            directions = self.validDirections()
            direction = self.directionMethod(directions) 
            if not self.disablePortal:
                if self.node.neighbors[PORTAL] is not None: 
                    self.node = self.node.neighbors[PORTAL]
            self.target = self.getNewTarget(direction)
            if self.target is not self.node: 
                self.direction = direction # go in the new random direction
            else:
                self.target = self.getNewTarget(self.direction) # try to go in the same direction
            self.setPosition()
    
    def goalDirection(self, directions):
        distances = []
        for direction in directions: 
            vec = self.node.position + self.directions[direction] * TITLEWIDTH - self.goal
            distances.append(vec.length())
        index = distances.index(min(distances))
        return directions[index]