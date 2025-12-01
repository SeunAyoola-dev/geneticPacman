import pygame
from vectors import Vector2
from constants import *
import numpy as np

class Pellet(object): 
    def __init__(self, row, column):
        self.name = PELLET
        self.position = Vector2(column * TITLEWIDTH, row * TITLEHEIGHT)
        self.color = WHITE
        self.radius = int(4 * TITLEWIDTH / 16)
        self.collideRadius = int(4 * TITLEWIDTH / 16)
        self.points = 10
        self.visible = True
    
    def render(self, screen): 
        if self.visible: 
            p = self.position.asInt()
            pygame.draw.circle(screen, self.color, p, self.radius)
            
            
class PowerPellet(Pellet):
    def __init__(self, row, column):
        super().__init__(row, column)
        self.name = POWERPELLET
        self.radius = int(8 * TITLEWIDTH / 16)
        self.collideRadius = int(8 * TITLEWIDTH / 16)
        self.points = 50
        self.flashTime = 0.2
        self.timer = 0 
    
    def update(self, dt):
        self.timer += dt
        if self.timer >= self.flashTime:
            self.visible = not self.visible
            self.timer = 0
    
class PelletGroup(object):
    def __init__(self, pelletData):
        self.pelletList = []
        self.powerPelletList = []
        self.createPellets(pelletData)
        self.numEaten = 0
        # self.pelletSymbols = ['.', '+']
        # self.powerPelletSymbols = ['P', 'p']
        
    def render(self, screen):
        for pellet in self.pelletList:
            pellet.render(screen)
    
    def update(self, dt):
        for pp in self.powerPelletList:
            pp.update(dt)
    
    def isEmpty(self):
        return len(self.pelletList) == 0
        
    def readPelletFile(self, textfile):
        return np.loadtxt(textfile, dtype='<U1')
    
    def createPellets(self, pelletData):
        data = self.readPelletFile(pelletData)
        for row in range(data.shape[0]): 
            for col in range(data.shape[1]):
                if data[row][col] in ['.', '+']: 
                    self.pelletList.append(Pellet(row, col))
                elif data[row][col] in ['P', 'p']:
                    powerP = PowerPellet(row, col)
                    self.powerPelletList.append(powerP)
                    self.pelletList.append(powerP)