add_library('sound')
import os, time, math
path = os.getcwd()
print path

def distance(p, q):
    """Helper function to calculate distance between 2 points"""
    return math.sqrt((p[0]-q[0])**2 + (p[1]-q[1])**2)

class Game:
    def __init__ (self):
        self.w = 700
        self.h = 700
        self.score = 0
        self.lives = 3
        self.stage = 1
        
        self.asteroids =[]
        self.asteroids.append(Asteroids(0,900,25, 500))
        self.asteroids.append(Asteroids(900,200,25, 500))
        
        self.skyImg = loadImage('background.png')
        self.lifeImg = loadImage('Rocket.png')
        self.gameover = False
        #self.gameoverImg = loadImage('gameover.png')
        
    def update(self):
        for i in range(len(self.asteroids)):
            a = self.asteroids.pop(0)
            bulletCollision = False
            rocketCollision = False
            bullet = None
            for b in rocket.bullets:
                if sqrt((b.x -a.vx)**2 + (b.y - a.vy)**2) <= b.r + a.r: #wrong, needs ranges
                    bulletCollision = True

                    rocket.bullets.remove(b)
                    self.score +=10
            if sqrt((rocket.x -a.vx)**2 + (rocket.y - a.vy)**2) <= rocket.r + a.r:
                rocketCollision = True
                self.lives -= 1
                if self.lives>0:
                    rocket.__init__(350,350,20)
                
            if bulletCollision or rocketCollision:
                collision.trigger()
            else:
                self.asteroids.append(a)
                

    def display(self):
        image(self.skyImg, 0, 0)
        integer = 0
        self.update()
        for a in self.asteroids:
            a.display()
        print self.lives,self.score
        textSize (18)
        fill (255)
        text('Score: ' + str(self.score), 650, 20)
        text('Lives: ',40,20)
        for life in range(1,self.lives+1):
            image(self.lifeImg,life*60,5,30,20)
        if self.lives == 0:
            #image(self.gameoverImg,0,0,700,700)
            textSize (26)
            fill (0)
            text('Final Score: ' + str(self.score), 700, 400)
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
        self.update()
        a = loadImage(Asteroid.png)
        image (a,self.vx-self.r,self.vy-self.r, 2*self.r, 2*self.r)
        
        
    def update (self):
        if self.y<350:
            self.theta=(self.theta+0.06)%360
            #self.r=0.16
            self.vx=self.x+self.l*cos(radians(self.theta))
            self.vy=self.y+self.l*sin(radians(self.theta))
        else:
            self.theta=(self.theta+0.06)%360
            #self.r=0.16
            self.vx=self.x+self.l*sin(self.theta)  
            self.vy=self.y+self.l*cos(self.theta)
    
class Bullet:
    
    def __init__(self,x,y,r,theta):
        self.x = x
        self.y = y
        self.r = r
        self.theta = theta
        self.d = 0
    
        
    def update(self):
        self.x += 20*sin(radians(self.theta))
        
        self.y -= 20*cos(radians(self.theta))
        self.d += sqrt((10*cos(radians(self.theta)))**2 +  (10*sin(radians(self.theta)))**2 ) 
        
    def display(self):
        self.update()
        stroke(0)
        fill(300-self.d,0,0)
        ellipse(self.x,self.y, self.r, self.r)
class Rocket:
    
    def __init__(self, x,y,r):
        self.x = x
        self.y = y
        self.r = r
        self.rx = self.x
        self.ry =self.y- self.r
        self.theta = 0
        self.vx = 0
        self.vy = 0
        self.dir = 0
        self.Keys={ UP:False, LEFT:False, RIGHT:False}
        self.decx= 0
        self.decy =0
        self.bullets=[]
        
        
    def addBullet(self):
        self.bullets.append(Bullet(self.x,self.y,10,self.theta))
        
    def display (self):
        self.update()
        #ellipse(self.x ,self.y,2*self.r,2*self.r) 
        image (loadImage('Rocket' +'.png'),self.x-self.r,self.y-self.r,2*self.r,2*self.r)
        stroke(255,0,0)
    
#       line (self.x,self.y,self.x +300*sin(radians(self.theta)), self.y -300*cos(radians(self.theta)))
        for i in range(len(self.bullets)):
            b = self.bullets.pop(0)
            b.display()
            if b.d < 300:
                self.bullets.append(b)
        #display bullets
                
    def update(self):
        #rockets bullet update
        if self.x > game.w:
            self.x = 0
        elif self.x <0:
            self.x = game.w
        if self.y <0:
            self.y = game.h
        elif self.y > game.h:
            self.y =0
        
        if self.Keys[RIGHT]:
            self.theta=(self.theta+45)%360
            
        elif self.Keys[LEFT]:
            self.theta=(self.theta-45)%360
      
        if self.decx > 0:
            self.decx-=0.5
        elif self.decx < 0:
            self.decx+=0.5
        if self.decy > 0:
            self.decy-=0.5
        elif self.decy < 0:
            self.decy+=0.5
            
        if self.Keys[UP]:
            if (self.theta == 0):
                self.vy = -15
            elif (self.theta == 45):
                self.vx = 10
                self.vy = -10
            elif (self.theta == 90):
                self.vx = 15
            elif (self.theta == 135):
                self.vx = 10
                self.vy = 10
            elif (self.theta == 180):
                self.vy = 15
            elif (self.theta == 225):
                self.vx = -10
                self.vy = 10
            elif (self.theta == 270):
                self.vx = -15
            elif (self.theta == 315):
                self.vx = -10
                self.vy = -10
        else:
            
            self.vy = 0
            self.vx = 0
            
        self.x += self.vx + self.decx
        self.y += self.vy + self.decy
        
game = Game()
rocket = Rocket(350,350,20)
def setup():
    size(game.w,game.h)
    
    background(0)

def draw():
    if game.lives == 0:
        #image(game.gameoverImg,0,0,700,700)
        textSize (26)
        fill (0)
        text('Final Score: ' + str(game.score), 300, 400)
    elif game.stage == 1:
        textAlign(CENTER)
        textSize(18)
        fill(0)
        text('ASTEROIDS', 200, 450)
        text('Controls', 200, 490)
        text('UP key: Thrust', 200, 510)
        text('LEFT & RIGHT key: Steer', 200, 530)
        text('SPACE key: Shoot', 200, 550)        
        
        text('Press enter/return to start the game', 200, 600)
        
        if key == ENTER:
            game.stage = 2
        
    elif game.stage == 2:
        game.display()   
        rocket.display()de

def keyPressed ():
    
    if game.stage == 2:
        if keyCode in [UP,LEFT,RIGHT]:
            rocket.Keys[keyCode] = True
        if keyCode == 32:
            rocket.addBullet()
    
def keyReleased ():
    rocket.Keys[keyCode] = False
    decDict = { 0:[0,-14], 45:[10,-10], 90:[14,0], 135:[10,10], 180:[0,14], 225:[-10,10], 270:[-10,0],315:[-10,-10]}
    if keyCode == UP:
        rocket.decx = decDict[rocket.theta][0]
        rocket.decy = decDict[rocket.theta][1]


    #game.display()
