import pygame
from pygame.locals import *
from vectors import Vector2
from constants import *
from entity import Entity
from modes import ModeController

class Ghost(Entity):
    def __init__(self, node, pacman = None, blinky = None):
        super().__init__(node)
        self.name = GHOST
        self.points = 200 
        self.goal = Vector2()
        self.directionMethod = self.goalDirection
        self.pacman = pacman 
        self.mode = ModeController(self)
        self.blinky = blinky
        self.homeNode = node 
    
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
            
class Blinky(Ghost):
    def __init__(self, node, pacman, blinky=None):
        super().__init__(node, pacman, blinky)
        self.name = BLINKY
        self.color = RED
        
class Pinky(Ghost):
    def __init__(self, node, pacman, blinky):
        super().__init__(node, pacman, blinky)
        self.name = PINKY
        self.color = PINK
        
    def scatter(self):
        self.goal = Vector2(TITLEWIDTH*NCOLS, 0)
        
    def chase(self):
        self.goal = self.pacman.position + self.pacman.directions[self.pacman.direction] * TITLEWIDTH * 4
        
class Inky(Ghost):
    def __init__(self, node, pacman, blinky):
        super().__init__(node, pacman, blinky)
        self.name = INKY
        self.color = CYAN
        
    def scatter(self):
        self.goal = Vector2(TITLEWIDTH*NCOLS, TITLEHEIGHT*NROWS)
        
    def chase(self):
        firstPos = self.pacman.position + self.pacman.directions[self.pacman.direction] * TITLEWIDTH * 2
        secondPos = (firstPos - self.blinky.position) * 2

class Clyde(Ghost):
    def __init__(self, node, pacman, blinky):
        super().__init__(node, pacman, blinky)
        self.name = CLYDE
        self.color = ORANGE
        
    def scatter(self):
        self.goal = Vector2(0, TITLEHEIGHT*NROWS)
        
    def chase(self):
        d = self.position - self.pacman.position
        d = d.magnitudeSquared()
        if d <= (TITLEWIDTH * 8)**2:
            self.scatter()
        else:
            self.goal = self.pacman.position + self.pacman.directions[self.pacman.direction] * TITLEWIDTH * 4
            
class GhostGroup(object):
    def __init__(self, node, pacman):
        self.blinky = Blinky(node, pacman)
        self.pinky = Pinky(node, pacman, self.blinky)
        self.inky = Inky(node, pacman, self.blinky)
        self.clyde = Clyde(node, pacman, self.blinky)
        self.ghosts = [self.blinky, self.pinky, self.inky, self.clyde]
        
    def __iter__(self):
        return iter(self.ghosts)
    
    def update(self, dt):
        for ghost in self:
            ghost.update(dt)
    
    def startFright(self):
        for ghost in self:
            ghost.startFright()
        self.resetPoints()
        
    def setSpawnNode(self, node):
        for ghost in self:
            ghost.setSpawnNode(node)
    
    def updatePoints(self):
        for ghost in self:
            ghost.points *= 2
            
    def resetPoints(self):
        for ghost in self:
            ghost.points = 200
            
    def reset(self):
        for ghost in self: 
            ghost.reset()
            
    def hide(self):
        for ghost in self:
            ghost.visible = False
            
    def show(self):
        for ghost in self:
            ghost.visible = True

    def render(self, screen):
        for ghost in self:
            ghost.render(screen)