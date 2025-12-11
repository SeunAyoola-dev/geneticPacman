import pygame
from pygame.locals import *
from vectors import Vector2
from constants import *
import math
from entity import Entity

class Pacman(Entity):
    def __init__(self, node):
        super().__init__(node)
        self.name = 'Genetic Pacman'
        self.color = YELLOW
        self.direction = LEFT
                
    
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

    def eatPellet(self, pelletList):
        for pellet in pelletList: 
            d = self.position - pellet.position
            d = d.length()
            r = math.sqrt(pellet.radius**2 + self.collideRadius**2)
            if d < r: 
                return pellet 
        return None
    
    def collideGhost(self, ghost):
        return self.collideCheck(ghost)

    def collideCheck(self, other):
        d = self.position - other.position
        dSquared = d.magnitudeSquared()
        rSquared = (self.collideRadius + other.collideRadius)**2
        if dSquared <= rSquared:
            return True
        return False
            
    
    