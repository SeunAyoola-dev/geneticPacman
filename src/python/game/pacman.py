import pygame
from pygame.locals import *
from vectors import Vector2
from constants import *
import math

class Pacman(object): 
    def __init__(self, node):
        self.name = 'Genetic Pacman'
        self.directions = {STOP:Vector2(), UP:Vector2(0,-1), DOWN:Vector2(0,1), LEFT:Vector2(-1,0), RIGHT:Vector2(1,0)}
        self.direction = STOP
        self.speed = 100 * TITLEWIDTH/16 # speed relative to the size of the maze 
        self.radius = 10
        self.color = YELLOW
        self.node = node
        self.target = node
        self.collideRadius = self.radius / 2
        self.setPosition()
                
    def setPosition(self):
        self.position = self.node.position.copy()
    
    def update(self, dt): 
        self.position += self.directions[self.direction] * self.speed * dt
        direction = self.getValidKey()
        
        if self.overshotTarget(): 
            self.node = self.target
            if self.node.neighbors[PORTAL] is not None: 
                self.node = self.node.neighbors[PORTAL]
            self.target = self.getNewTarget(direction)
            
            if self.target is not self.node: 
                self.direction = direction
                
            else: 
                self.target = self.getNewTarget(self.direction)
                
            if self.target is self.node: 
                self.direction = STOP
                
            self.setPosition()
        
        else:
            if self.oppositeDirection(direction): 
                self.reverseDirection()
            
    
    def getValidKey(self):
        key_pressed = pygame.key.get_pressed()
        if key_pressed[K_UP]:
            return UP
        elif key_pressed[K_DOWN]:
            return DOWN
        elif key_pressed[K_LEFT]:
            return LEFT
        elif key_pressed[K_RIGHT]:
            return RIGHT
        return STOP
    
    def render(self, screen): 
        p = self.position.asInt()
        pygame.draw.circle(screen, self.color, p, self.radius)
        
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
    
    def eatPellet(self, pelletList):
        for pellet in pelletList: 
            d = self.position - pellet.position
            d = d.length()
            r = math.sqrt(pellet.radius**2 + self.collideRadius**2)
            if d < r: 
                return pellet 
        return None
            
    
    