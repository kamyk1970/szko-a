class Punkt:
    def __init__(self,x,y):
        self.x = x
        self.y = y
    def __add__(self,other):
        return Punkt(self.x+other.x,self.y+other.y)
    def __str__(self):
        return f"Punkt {self.x}" f" i punkt {self.y}"
    def __mul__(self,other):
        return Punkt(self.x*other.x,self.y*other.y)
    def __div__(self,other):
        return Punkt(self.x/other.x,self.y/other.y)
    def __sub__(self,other):
        return Punkt(self.x-other.x,self.y-other.y)
    
punkt1 = Punkt(0,1)
punkt2 = Punkt(6,6)
punkt3 = punkt1 + punkt2
print(punkt1)
punkt1.__mul__(punkt2)
punkt1.__div__(punkt2)
punkt1.__sub__(punkt2)