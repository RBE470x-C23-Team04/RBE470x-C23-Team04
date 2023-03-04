### STORE WEIGHT VALUES FOR Q-LEARN

class Bank():
    def __init__(self):
        #5020
        self.we = .3    # weight for Exit
        self.wma = -.5  # weight for Monster A
        self.wmb = -.5  # weight for Monster B
        self.wb = -.3   # weight for Bomb
        self.wx = -.2   # weight for Explosion
        
        #5020
        # self.we = -10
        # self.wma = 100
        # self.wmb = -0.5
        # self.wb = 100
        # self.wx = 100




  
    
    def getWe(self):
        return self.we
    
    def getWma(self):
        return self.wma

    def getWb(self):
        return self.wb

    def getWx(self):
        return self.wx
    

    def setWe(self,value):
        self.we = value
    
    def setWma(self,value):
        self.wma = value

    def setWb(self,value):
        self.wb = value

    def setWx(self,value):
        self.wx = value

bank1 = Bank() # Create a bank object
    



   
