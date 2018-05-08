import pygame,sys,random,math,time

pygame.init()
background = pygame.Color(85,50,253)
fontColor = pygame.Color(0,162,232)
display = pygame.display.set_mode((1280,720))   #display size
buttonHover =  pygame.Color(0,90,50)
buttonColor=pygame.Color(36,38,123)
white = pygame.Color(255,255,255)
ShootSound = pygame.mixer.Sound('shooting.WAV')
ShipSound = pygame.mixer.Sound('thrust.ogg')
ShipCrash = pygame.mixer.Sound('explod.WAV')
ExplosionSound = ShipCrash
pygame.mixer.music.load('trektheme.ogg')
pygame.display.set_caption("Asteroids")

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
#global variables
count=0
score=0
level=1
limit=6
run=False

 #This class controls ship's rotation,moves,shooting
class Rocket:
    def __init__(self, pos, vel, angle, image,info):
        self.position = [pos[0]-45,pos[1]-45]
        self.velocity = [vel[0],vel[1]]
        self.move = False
        self.angle = angle
        self.changeAngle = 0
        self.image = image
        self.image_center = info.Center()
        self.image_size = info.Size()
        self.radius = info.Radius()
        self.forward = [0,0]
    
    def Shoot(self):
        global missile
        ShootSound.play()
        MissilePos = [self.position[0]+40 + self.radius * self.forward[0], self.position[1]+40 + self.radius * self.forward[1]]
        MissileVel = [self.velocity[0] + 6 * self.forward[0], self.velocity[1] + 6 * self.forward[1]]
        missile.add(SpaceElement(MissilePos, MissileVel, self.angle, 0, MissileImage, MissileInfo,None, ShootSound,None,'m'))
        
    def Move_Ship(self, move,direction=None):
        self.move = move
        self.direction = direction
        if self.move:
            ShipSound.play()
        else:
            ShipSound.stop()
    def Position(self):
        return (int(self.position[0] + self.radius), int(self.position[1] + self.radius))
    def Radius(self):
        return self.radius
    def Draw(self,canvas):
        canvas.blit(RotateImage(self.image, self.angle), self.position)
    def Update(self):
        acc = 0.5
        fric = acc / 20
        self.angle += self.changeAngle
        self.forward = AngleCalculate(math.radians(self.angle))
        if self.move and self.direction == 'up':
            self.velocity[0] += self.forward[0] * acc
            self.velocity[1] += self.forward[1] * acc
        if self.move and self.direction == 'down':
            self.velocity[0] -= self.forward[0] * acc
            self.velocity[1] -= self.forward[1] * acc
        self.velocity[0] *= (1 - fric)
        self.velocity[1] *= (1 - fric)
        self.position[0] = (self.position[0] + self.velocity[0]) % (1280 - self.radius)
        self.position[1] = (self.position[1] + self.velocity[1]) % (720 - self.radius)
        
    def Rotate(self, vel):
        self.changeAngle = vel

#This class controls behavior of all the rocks in the space
class SpaceElement:
    def __init__(self, pos, vel, angle, changeAngle, image, info,needs=None, sound = None,v=None,t=None):
        if sound:
            sound.play()
        self.velocity = [vel[0],vel[1]]
        self.angle = angle
        self.changeAngle = changeAngle
        self.image = image
        self.image_center = info.Center()
        self.image_size = info.Size()
        self.radius = info.Radius()
        self.moving = info.Moving()
        self.time = 3
        self.position = [pos[0]+self.radius,pos[1]+self.radius]
        self.needshoot = needs
        self.value=v
        self.type=t

    def collide(self,other_object):
        if distance(self.position, other_object.Position()) <= self.radius + other_object.Radius():
            return True
        else:
            return False
    def Position(self):
        return [int(self.position[0]), int(self.position[1])]
    def Radius(self):
        return self.radius
    def NeedShoot(self):
        return self.needshoot
    def DecreaseNeed(self):
        self.needshoot -= 1
    def RockValue(self):
        if self.value != None:
            return self.value
    def Draw(self, canvas):
     #   
        canvas.blit(RotateImage(self.image, self.angle), (int(self.position[0] - self.radius), int(self.position[1] - self.radius)))
    def Update(self):
        self.angle += self.changeAngle
        if 0 >= self.position[0] >= 1280 or 0 >= self.position[1] >= 720:
            return True
        elif self.type != 'm':
            self.position[0] = (self.position[0] + self.velocity[0])%1280
            self.position[1] = (self.position[1] + self.velocity[1])%720
        else:
            self.position[0] = (self.position[0] + self.velocity[0])
            self.position[1] = (self.position[1] + self.velocity[1])
        return False

def RotateImage(image, angle): #Captured the image in a rectangle and then rotating the rectangle. 
    orig_rect = image.get_rect()
    rot_image = pygame.transform.rotate(image, angle)
    rot_rect = orig_rect.copy()
    rot_rect.center = rot_image.get_rect().center
    rot_image = rot_image.subsurface(rot_rect).copy()
    return rot_image

def AngleCalculate(ang):
    return [math.cos(ang), -math.sin(ang)]

def Draw_Components(canvas):
    for r in rock:
        r.Draw(canvas)
        r.Update()   
    for m in list(missile):
        m.Draw(canvas)
        if m.Update():
            missile.remove(m)
    for e in explosion:
        e.Draw(canvas)

#It checks how much shoots are needed to despoil a rock
def CheckNeed(group):
    val=0
    for element in list(group):
        if element.NeedShoot() <=0:
            explosion.add(SpaceElement([element.Position()[0] - 4*element.radius,element.Position()[1] - 4*element.radius], [0,0], 0, 0, ExplosionImg,ExplosionInfo,None,ExplosionSound))
            val=element.RockValue()
            group.remove(element)
    return val

#It checks whether a rock hits the ship or not
def Check_Collision(elements,object):
    for e in list(elements):
        if e.collide(object):
            e.DecreaseNeed()
            return True      
    return False

#It checks whether a missile hits any rock or not
def Check_Missile_Hit(missile_group, rockect_group):
    counter = 0
    for element in list(missile_group):
        if Check_Collision(rockect_group,element):
            counter += 1
            missile_group.remove(element)
    return counter

#All the components added to the display and calculates scores and levels
def DrawBoard(canvas):
    global score,level,run,count
    canvas.blit(BackgroundImg,(0,0))
    canvas.blit(BackgroundImg2,(count*.3,0))
    canvas.blit(BackgroundImg2,(count*.3-1280,0))
    Asteroids.Draw(canvas)
    if run:
        Draw_Components(canvas)
        Asteroids.Update()
        if Check_Collision(rock,Asteroids):
            run=False
        Check_Missile_Hit(missile,rock)
        val=CheckNeed(rock)
        score += val
        if score>=50:
            level = 2
        if score>=100:
            level = 3
    else:
        GameOver()
    myfont1 = pygame.font.SysFont("comicsansms", 20)
    label1 = myfont1.render("Level : "+str(level), 1, (255,255,0))
    canvas.blit(label1, (50,20))

    myfont2 = pygame.font.SysFont("comicsansms", 20)
    label2 = myfont2.render("Score : "+str(score), 1, (255,255,0))
    canvas.blit(label2, (1150, 20))

def Rock():
        global level,limit
        if level == 2:
            limit=10
        elif level == 3:
            limit=15
        rock_image=Rock_1
        rock_info=Rock_1_Info
        needshoot=5
        value=0
        global rock,run
        if len(rock) < limit:
            while 1:
                random_pos1 = [random.randrange(0,1280), 0]
                random_pos2 = [random.randrange(0,1280), 720]
                random_pos3 = [0,random.randrange(0,720)]
                random_pos4 = [1280,random.randrange(0,1280), 720]
                r=random.randrange(1,4)
                if r==1:
                    rock_pos=random_pos1
                if r==2:
                    rock_pos=random_pos2
                if r==3:
                    rock_pos=random_pos3
                if r==4:
                    rock_pos=random_pos4
                break
            rand = random.randrange(1,3)
            if rand==1:
                rock_image=Rock_1
                rock_info=Rock_1_Info
                needshoot=5
                value=15
            if rand==2:
                rock_image=Rock_2
                rock_info=Rock_2_Info
                needshoot=3
                value=10
            elif rand == 3:
                rock_image=Rock_3
                rock_info=Rock_3_Info
                needshoot=1
                value=5
            rock_vel = [random.randrange(-3,3), random.randrange(-3,3)]
            rock_avel = random.randrange(-3,3)
            rock.add(SpaceElement(rock_pos, rock_vel, 0,rock_avel, rock_image, rock_info,needshoot,None,value))
def Counter():
    global count
    
    if count <= 1280:
        count += 1
        if count % 60 == 0:
            Rock()
    else:
        count = 0


BackgroundImg = pygame.image.load('background.png')
BackgroundImg2= pygame.image.load('background2.png')
BackgroundImg3= pygame.image.load('background3.jpg')
ShipImg = pygame.image.load("ship.png")
ShipInfo = Images([45,45], [90,90],45)
ExplosionImg = pygame.image.load('explosion1.png')
ExplosionInfo = Images([64,64], [128,128], 64, True)
Rock_1 = pygame.image.load('AsteroidLarge.png')
Rock_1_Info = Images([25,25], [51,51],25)
Rock_2 = pygame.image.load('AsteroidMedium.png')
Rock_2_Info = Images([19,19], [38,38],19)
Rock_3 = pygame.image.load('AsteroidSmall.png')
Rock_3_Info = Images([13,13], [26,26],13)
MissileImage = pygame.image.load('shoot.png')
MissileInfo = Images([5,5], [10,10], 5)

Asteroids = Rocket([640,360], [0,0], 0, ShipImg,ShipInfo)
#empty lists that will contain all the rocks,missiles and exploded rocks
rock = set([])
missile = set([])
explosion =set([])
def Intro():
    namefont = pygame.font.SysFont("arial",100)
    nametext = namefont.render("Asteroids",True,white)
    display.blit(BackgroundImg3,(0,0))
    display.blit(nametext,(500,50))
    display.blit(ShipImg,(550,300))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        Button("Exit",450,450,100,60,QuitGame)
        Button("Start Game",650,450,150,60,NewGame)
        pygame.display.update()
        #clock.tick(15)

#This function contains button's behaviors
def Button(name,x,y,h,w,action=None):
    pos = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x<pos[0]<x+h and y<pos[1]<y+w:
        pygame.draw.rect(display,buttonHover,[x,y,h,w])
        if click[0]==1 and action!=None:
            action()
    else:
        pygame.draw.rect(display,buttonColor,[x,y,h,w])
    font = pygame.font.SysFont("comicsansms",20)
    text = font.render(name,True,white)
    display.blit(text,(x+15,y+15))

#function for Quit Game
def QuitGame():
    pygame.quit()
    sys.exit()

#Game starts from here
def NewGame():
    global run, level, score, rock, missile, Asteroids,count
    pygame.mixer.music.play()
    run = True
    level = 1
    score,count = 0,0
    rock = set([])
    missile = set([])
    explosion =set([])
    while True:
        DrawBoard(display)
        Counter()
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                angle = 10
                if event.key == pygame.K_LEFT:
                    Asteroids.Rotate(angle)
                if event.key == pygame.K_RIGHT:
                    Asteroids.Rotate(-angle)
                if event.key == pygame.K_UP:
                    Asteroids.Move_Ship(True,'up')
                if event.key == pygame.K_DOWN:
                    Asteroids.Move_Ship(True,'down')
                if event.key == pygame.K_SPACE:
                    Asteroids.Shoot()
            elif event.type == pygame.KEYUP:
                Asteroids.Rotate(0)
                Asteroids.Move_Ship(False)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                Asteroids.Shoot()
            elif event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()   
        pygame.display.update()
        #clock.tick(60)

#function for Game Over window
def GameOver():
    global score
    ShipSound.stop()
    ShipCrash.play()
    font = pygame.font.SysFont("comicsansms",80)
    text = font.render("Game Over",True,white)
    scoreText = font.render("Your Score : "+str(score),True,white)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        display.blit(text,(460,150))
        display.blit(scoreText,(400,300))
        Button("Quit",450,450,80,60,QuitGame)
        Button("Play Again",650,450,150,60,NewGame)
        pygame.display.update()
        #clock.tick(15)
Intro()
pygame.quit()
sys.exit()
