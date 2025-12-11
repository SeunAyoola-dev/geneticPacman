import pygame
from pygame.locals import * 
from constants import * 
from pacman import Pacman
from nodes import NodeGroup
from pellets import PelletGroup
from ghosts import GhostGroup
from fruit import Fruit

class GameController(object): 
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(SCREENSIZE)
        self.background = None
        self.clock = pygame.time.Clock()
        self.fruit = None
        self.lives = 5
        
    def restartGame(self):
        self.lives = 5
        self.level = 0
        self.pause.paused = True
        self.fruit = None
        self.startGame()
    
    def setBackground(self):
        self.background = pygame.surface.Surface(SCREENSIZE).convert()
        self.background.fill(BLACK)
        
    def startGame(self):
        self.setBackground()
        self.nodes = NodeGroup('src/python/maze/mazetest.txt')
        self.pellets = PelletGroup('src/python/maze/mazetest.txt')
        self.nodes.setPortalPair((0,17),(27,17))
        homekey = self.nodes.createHomeNodes(11.5, 14)
        self.nodes.connectHomeNodes(homekey, (12,14), LEFT)
        self.nodes.connectHomeNodes(homekey, (15,14), RIGHT)
        self.pacman = Pacman(self.nodes.getNodeFromTiles(15, 26))
        self.ghosts = GhostGroup(self.nodes.getStartPoint(), self.pacman)
        self.ghosts.blinky.setSpawnNode(self.nodes.getNodeFromTiles(2+11.5, 0+14))
        self.ghosts.pinky.setSpawnNode(self.nodes.getNodeFromTiles(2+11.5, 3+14))
        self.ghosts.inky.setSpawnNode(self.nodes.getNodeFromTiles(0+11.5, 3+14))
        self.ghosts.clyde.setSpawnNode(self.nodes.getNodeFromTiles(4+11.5, 3+14))
        self.ghosts.setSpawnNode(self.nodes.getNodeFromTiles(2+11.5, 3+14))


        
    def update(self):
        dt = self.clock.tick(30) / 1000.0
        self.pacman.update(dt)
        self.pellets.update(dt)
        self.ghosts.update(dt)
        if self.fruit is not None:
            self.fruit.update(dt)
        self.checkGhostEvents()
        self.checkEvents()
        self.checkPelletEvents()
        self.checkFruitEvents()
        self.render()
        
    def checkEvents(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
    
    def render(self):
        self.screen.blit(self.background, (0,0))
        self.nodes.render(self.screen)
        self.pellets.render(self.screen)
        if self.fruit is not None:
            self.fruit.render(self.screen)
        self.pacman.render(self.screen)
        self.ghosts.render(self.screen)
        pygame.display.update()
        
    def checkPelletEvents(self):
        pellet = self.pacman.eatPellet(self.pellets.pelletList)
        if pellet is not None:
            self.pellets.numEaten += 1
            self.pellets.pelletList.remove(pellet)
            if pellet.name == POWERPELLET:
                print("Power Pellet Eaten!")
                self.ghosts.startFright()
                
    def checkGhostEvents(self):
        for ghost in self.ghosts:
            if self.pacman.collideGhost(ghost):
                if ghost.mode.current is FREIGHT:
                    ghost.startSpawn()
                    
    def checkFruitEvents(self):
        if self.pellets.numEaten == 30 or self.pellets.numEaten == 70:
            if self.fruit is None:
                self.fruit = Fruit(self.nodes.getNodeFromTiles(9, 20)) 
        if self.fruit is not None:
            if self.pacman.collideCheck(self.fruit):
                print("Fruit Eaten!")
                self.fruit = None
            elif self.fruit.destroy:
                self.fruit = None
               
if __name__ == "__main__":
    game = GameController()
    game.startGame()
    
    while True:
        game.update()