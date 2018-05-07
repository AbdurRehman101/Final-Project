add_library('sound')

import os

path = os.getcwd()
print path

class Game:
    def __init__(self):
        self.w=1280
        self.h=720
    
        
        self.bgImgs=[]
        self.x=0
        self.rocks=[]
        self.paused = False
        
    def createGame(self):
        
        self.bgImgs.append(loadImage(path+'/resources/background'+'.png'))
        
        for i in range(5):
            self.rocks.append(Rocks(100*(i+1),50,35,path+"/resources/AsteroidLarge.png"))
        
        self.ship = Player(50,50,39,path+"/resources/ShipRed.png",1)
        
     

    def display(self):
    
                
        image(self.bgImgs[0],0,0,self.w-self.x,self.h,self.x,0,self.w,self.h)
        image(self.bgImgs[0],self.w-self.x-1,0,self.x,self.h,0,0,self.x,self.h)
           # cnt+=1
            
        #stroke(255)
        #line(0,self.g,self.w,self.g)
        
        for r in self.rocks:
            r.display()
            
 
        self.ship.display()


         
class Player():
    def __init__(self,x,y,r,imgName,F):
        self.x=x
        self.y=y
        self.r=r
        self.w=self.r*2
        self.h=self.r*2
        self.vx=0
        self.vy=0

        self.dir=1
        self.img = loadImage(imgName)
        #Creature.__init__(self,x,y,r,g,imgName,F)
        
        self.keyHandler={LEFT:False,RIGHT:False,UP:False,DOWN:False}
    def display(self):
        self.update()
        
        #if self.vx != 0:
        #   self.f = (self.f+0.1)%self.F
            
        stroke(0,255,0)
        noFill()
        #ellipse(self.x-game.x,self.y,self.r*2,self.r*2)
        stroke(255,0,0)
        
        image(self.img,self.x-self.r-game.x,self.y-self.r,self.w,self.h,int(0+1)*self.w,0,int(0)*self.w,self.h)
    
    
    def update(self):
        
        
        if self.keyHandler[LEFT] and self.x - 40 >= 0:
            self.vx = -2
            self.dir = 1
            self.x+=self.vx
             
        elif self.keyHandler[RIGHT] and self.x +40 <= game.w:
            self.vx = 2
            self.dir = -1
            
            self.x+=self.vx
            if self.x + 40 == game.w:
                self.vx = 0
        elif self.keyHandler[DOWN]:
            self.vy = 2
            self.dir = 1
            self.y+=self.vy
        elif self.keyHandler[UP]:
            self.vy = -2
            self.dir = -1
            self.y+=self.vy
        else:
            self.vx = 0
            
        
        
        if self.x == game.w:
            self.vx = 0

 

class Rocks():
    def __init__(self,x,y,r,imgName):
        self.x=x
        self.y=y
        self.r=r
        self.w=self.r*2
        self.h=self.r*2
        self.vx=0
        self.vy=0
        #Creature.__init__(self,x,y,r,g,imgName,F)
        self.theta = 0
        self.img = loadImage(imgName)
        self.dir=1
        
    def update(self):
        if self.y<350:
            self.theta=(self.theta+2.0)%360
            #self.r=0.16
            self.vx=self.x+self.w*cos(radians(self.theta)) + 100
            self.vy=self.y+self.w*sin(radians(self.theta)) +100
        else:
            self.theta=(self.theta+2.0)%360
            #self.r=0.16
            self.vx=self.x+self.w*sin(self.theta) +100
            self.vy=self.y+self.w*cos(self.theta) +100
        
        
        
    def display(self):
        self.update()
        
        #if self.vx != 0:
         #   self.f = (self.f+0.1)%self.F
            
        stroke(0,255,0)
        noFill()
        ellipse(self.x-game.x,self.y,self.r*2,self.r*2)
        stroke(255,0,0)
         
        #image(self.img,self.x-self.r-game.x,self.y-self.r,self.w,self.h,int(0+1)*self.w,0,int(0)*self.w,self.h)
        image (self.img,self.vx-self.r,self.vy-self.r, 1*self.r, 1*self.r)

game = Game()

def setup():
    size(game.w,game.h)
    background(0)
    game.createGame()
    
def draw():

        
    background(0)
    game.display()
    

        
    
def keyPressed():
    print (keyCode)
    game.ship.keyHandler[keyCode]=True
    
    

def keyReleased():
    game.ship.keyHandler[keyCode]=False
