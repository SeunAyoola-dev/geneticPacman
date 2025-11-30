import pygame
from pygame.locals import *
from vectors import Vector2
from constants import *

class Pacman(object): 
    def __init__(self):
        self.name = 'Genetic Pacman'
        self.position = Vector2(200, 400)
        self.directions = {STOP:Vector2(), UP:Vector2(0,-1), DOWN:Vector2(0,1), LEFT:Vector2(-1,0), RIGHT:Vector2(1,0)}
        self.direction = STOP
        self.speed = 100 * TITLEWIDTH/16 # speed relative to the size of the maze 
        self.radius = 10
        self.color = YELLOW
    
    def update(self, dt): 
        self.position += self.directions[self.direction] * self.speed * dt
        direction = self.getValidKey()
        self.direction = direction
    
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