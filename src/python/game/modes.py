from constants import * 

class MainMode(object):
    def __init__(self):
        self.timer = 0 
        self.time = 0
        self.mode = SCATTER
    
    def update(self, dt):
        self.timer += dt
        if self.timer >= self.time:
            if self.mode is SCATTER:
                self.chase() 
            elif self.mode is CHASE:
                self.scatter()
    
    def scatter(self):
        self.mode = SCATTER
        self.time = 7
        self.timer = 0
    
    def chase(self):
        self.mode = CHASE
        self.time = 20
        self.timer = 0
        

class ModeController(object):
    def __init__(self, entity):
        self.timer = 0
        self.time = None
        self.mainMode = MainMode()
        self.current = self.mainMode.mode 
        self.entity = entity
    
    def update(self, dt):
        self.mainMode.update(dt)
        if self.current is FREIGHT:
            self.timer += dt
            
            if self.timer >= self.time:
                self.time = None
                self.entity.normalMode()
                self.current = self.mainMode.mode
                
        elif self.current in [SCATTER, CHASE]:
            self.current = self.mainMode.mode
            
        if self.current is SPAWN:
            
            if self.entity.node == self.entity.spawnNode:
                self.entity.normalMode()
                self.current = self.mainMode.mode
    
    def setFrightMode(self):
        if self.current in [SCATTER, CHASE]: 
            self.current = FREIGHT
            self.time = 7
            self.timer = 0
        elif self.current is FREIGHT:
            self.timer = 0 # timer reset 
    
    def setSpawnMode(self):
        if self.current is FREIGHT:
            self.current = SPAWN