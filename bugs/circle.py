import math

class Circle(object):
    
    def __init__(self, center=(0.,0.), radius=1.):
        if radius < 0: 
            raise ValueError('radius must be >= 0')
        self.center = center
        self.radius = radius
        
    def area(self):
        return math.pi * self.radius**2
    
if __name__ == '__main__':
    
    c = Circle()
    print(c.center,c.radius) 
    print (c.area())
    c.radius = 2. 
    print (c.area())