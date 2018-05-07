add_library('sound')
#import os, time, math
#path = os.getcwd()
#print path

def get_distance(a, b):
    """Helper function to calculate distance between 2 points"""
    return math.sqrt((a[0]-b[0])**2 + (a[1]-b[1])**2)

class Game:
    def __init__ (self):
        self.w = 1280
        self.h = 720
        self.bgImg = loadImage('background.png')
        #self.rocketimg = loadImage('Rocket.png')
        
        
    def display(self):
        image(self.bgImg, 0,0,1280,720)
        textSize (18)
        fill (255)
        text('Score: ' , 100, 20)
        
class Asteroids:
    def __init__ (self,x,y,r,l):
        self.x = x 
        self.y = y 
        self.r = r
        self.vx = 0 
        self.vy = 0 
        self.angle = 0 
        self.l = l 
        
    def display(self):
     
        a = loadImage('Asteroid.png')
        image(a,self.vx-self.r,self.vy-self.r, 2*self.r, 2*self.r)

game = Game()
#Asteroids = Asteroids(0,900,25, 500)
def setup():
    size(game.w,game.h)
    
def draw():
    game.display()
    #Asteroids.display()
