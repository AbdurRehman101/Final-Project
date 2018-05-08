import pygame,sys,random,math,time

pygame.init()
background = pygame.Color(85,50,253)
fontColor = pygame.Color(0,162,232)
display = pygame.display.set_mode((1280,720))   #display size
ShootSound = pygame.mixer.Sound('shooting.WAV')
ShipSound = pygame.mixer.Sound('thrust.ogg')
ExplosionSound = pygame.mixer.Sound('explod.WAV')
pygame.mixer.music.load('trektheme.ogg')

def distance(x,y):
    return math.sqrt((x[0]-y[0])**2+(x[1]-y[1])**2)

class Images:
    def __init__(self, center, size, radius,moving = False):
        self.center = center
        self.size = size
        self.radius = radius
        self.moving = moving
    def Center(self):
        return self.center
    def Size(self):
        return self.size
    def Radius(self):
        return self.radius
    def Moving(self):
        return self.moving

 #This class controls ship's rotation,moves,shooting
class Ship:
	def __init__(self, position, velocity, angle, image,info):
		self.position = [pos[0],pos[1]]
		self.velocity = [vel[0],vel[1]]
		self.angle = angle
		self.image = image
		self.move = False
		self.changeAngle = 0 
		self.radius = info.Radius()
		self.forward = []

lass Asteroids:
    def __init__(self, position, velocity, angle, changeAngle, image, info, HitsNeeded = None ):
    	self.position = [pos[0],pos[1]]
    	self.velocity = [vel[0],vel[1]]
        self.angle = angle
        self.changeAngle = changeAngle
        self.image = image
        self.image_center = info.Center()
        self.image_size = info.Size()
        self.radius = info.Radius()
        self.HitsNeeded = needs
        self.moving = info.Moving()
    def collide(self,other_object):
        if distance(self.position, other_object.Position()) <= self.radius + other_object.Radius():
            return True
        else:
            return False


    
    def Position(self):
        return [int(self.position[0]), int(self.position[1])]

    def Radius(self): #Returns the Radius of the rock.
        return self.radius

    def Draw(self, canvas):

    	canvas.blit(RotateImage(self.image, self.angle), (int(self.position[0] - self.radius), int(self.position[1] - self.radius)))

def RotateImage(image, angle): #Captured the image in a rectangle and then rotating the rectangle. 
    orig_rect = image.get_rect()
    rot_image = pygame.transform.rotate(image, angle)
    rot_rect = orig_rect.copy()
    rot_rect.center = rot_image.get_rect().center
    rot_image = rot_image.subsurface(rot_rect).copy()
    return rot_image

def AngleCalculate(ang):
    return [math.cos(ang), -math.sin(ang)]


BackgroBackgroundImg = pygame.image.load('background.png')
BackgroundImg2= pygame.image.load('background2.png')
BackgroundImg3= pygame.image.load('background3.jpg')
ShipImg = pygame.image.load("ship.png")
ShipInfo = Images([45,45], [90,90],45)
ExplosionImg = pygame.image.load('explosion1.png')
ExplosionInfo = Images([64,64], [128,128], 64, True)
Rocket_1 = pygame.image.load('AsteroidLarge.png')
Rocket_1_Info = Images([25,25], [51,51],25)
