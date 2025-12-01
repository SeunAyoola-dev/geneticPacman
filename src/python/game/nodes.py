import pygame 
from vectors import Vector2
from constants import *
import numpy as np

class Node(object):
    def __init__(self, x, y): 
        self.position = Vector2(x, y) 
        self.neighbors = {UP:None, DOWN:None, LEFT:None, RIGHT:None, PORTAL: None}
    
    def render(self, screen): 
        for n in self.neighbors.keys(): 
            if self.neighbors[n] is not None: 
                line_start = self.position.asTuple()
                line_end = self.neighbors[n].position.asTuple()
                pygame.draw.line(screen, WHITE, line_start, line_end, 4)
                pygame.draw.circle(screen, RED, self.position.asInt(), 12)

class NodeGroup(object):
    def __init__(self, level):
        self.level = level
        self.nodesTable = {}
        self.nodeSymbols = ['+']
        self.pathSymbols = ['.']
        data = self.readMazeFile(level)
        self.createNodeTable(data)
        self.connectHorironztalNodes(data)
        self.connectVerticalNodes(data)
        
    def render(self, screen):
        for node in self.nodesTable.values():
            node.render(screen)
            
    def readMazeFile(self, textfile):
        return np.loadtxt(textfile, dtype='<U1')
    
    def createNodeTable(self, data, xoffset = 0, yoffset = 0):
        for row in list(range(data.shape[0])):
            for col in list(range(data.shape[1])):
                if data[row][col] in self.nodeSymbols:
                    x, y = self.constructNodePosition(col + xoffset, row + yoffset)
                    self.nodesTable[(x, y)] = Node(x, y)
                    
    def connectHorironztalNodes(self, data, xoffset = 0, yoffset = 0):
        for row in list(range(data.shape[0])):
            key = None 
            for col in list(range(data.shape[1])):
                if data[row][col] in self.nodeSymbols:
                    if key is None:
                        key = self.constructNodePosition(col + xoffset, row + yoffset)
                    else:
                        otherkey = self.constructNodePosition(col + xoffset, row + yoffset)
                        self.nodesTable[key].neighbors[RIGHT] = self.nodesTable[otherkey]
                        self.nodesTable[otherkey].neighbors[LEFT] = self.nodesTable[key]
                        key = otherkey
                elif data[row][col] not in self.pathSymbols:
                    key = None
        
    def connectVerticalNodes(self, data, xoffset = 0, yoffset = 0):
        for col in list(range(data.shape[1])):
            key = None
            for row in list(range(data.shape[0])):
                if data[row][col] in self.nodeSymbols:
                    if key is None:
                        key = self.constructNodePosition(col + xoffset, row + yoffset)
                    else:
                        otherkey = self.constructNodePosition(col + xoffset, row + yoffset)
                        self.nodesTable[key].neighbors[DOWN] = self.nodesTable[otherkey]
                        self.nodesTable[otherkey].neighbors[UP] = self.nodesTable[key]
                        key = otherkey
                elif data[row][col] not in self.pathSymbols:
                    key = None
                    
    def constructNodePosition(self, x, y):
        return x * TITLEWIDTH, y * TITLEHEIGHT
    
    def getNodeFromPosition(self, x, y):
        if (x, y) in self.nodesTable.keys():
            return self.nodesTable[(x, y)]
        return None 
    
    def getNodeFromTiles(self, col, row):
        x = col * TITLEWIDTH
        y = row * TITLEHEIGHT
        if (x, y) in self.nodesTable.keys():
            return self.nodesTable[(x, y)]
        return None
    
    def getStartPoint(self):
        nodes = list(self.nodesTable.values())
        return nodes[0]