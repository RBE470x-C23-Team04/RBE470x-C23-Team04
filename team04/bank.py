class Bank():
    def __init__(self):
        self.we = .3
        self.wma = -.5
        self.wmb = -.5
        self.wb = -.3
        self.wx = -.2
    
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

bank1 = Bank()
    



   
