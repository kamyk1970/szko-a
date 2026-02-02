class Punkt:
    def __init__(self,x,y):
        self.x=x
        self.y=y
    def add(self,other):
        return Punkt(self.x+other.x,self.y+other.y)
    def string(self,other):
        return f'Punkt {self} i punkt {other}'
    def mul(self,other):
        return Punkt(self.x*other.x,self.y*other.y)
    def div(self,other):
        return Punkt(self.x/other.x,self.y/other.y)
    
punkt1 = Punkt(0,1)
punkt2 = Punkt(6,6)
