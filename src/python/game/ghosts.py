import pygame
from pygame.locals import *
from vectors import Vector2
from constants import *
from entity import Entity
from modes import ModeController

class Ghost(Entity):
    def __init__(self, node, pacman = None):
        super().__init__(node)
        self.name = GHOST
        self.points = 200 
        self.goal = Vector2()
        self.directionMethod = self.goalDirection
        self.pacman = pacman 
        self.mode = ModeController(self)
    
    def update(self, dt):
        self.mode.update(dt)
        if self.mode.current is SCATTER:
            self.scatter()
        elif self.mode.current is CHASE:
            self.chase()
        Entity.update(self, dt)

    def scatter(self):
        self.goal = Vector2()

    def chase(self):
        self.goal = self.pacman.position

    def startFright(self):
        self.mode.setFrightMode()
        if self.mode.current is FREIGHT:
            self.setSpeed(50)
            self.directionMethod = self.randomDirection
    
    def normalMode(self):
        self.setSpeed(100)
        self.directionMethod = self.goalDirection

    def spawn(self):
        self.goal = self.spawnNode.position
        
    def setSpawnNode(self, node):
        self.spawnNode = node
    
    def startSpawn(self):
        self.mode.setSpawnMode()
        if self.mode.current is SPAWN:
            self.setSpeed(150)
            self.directionMethod = self.goalDirection
            self.spawn()