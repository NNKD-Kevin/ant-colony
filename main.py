import pygame
import random
import math
import os

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((1500, 850))
pygame.display.set_caption("Ant Colony")
stage='collecting'
clock=pygame.time.Clock()

basic_font=pygame.font.Font('assets/font.ttf', 50)
farmground=pygame.image.load('assets/farmground.png').convert()
farmground=pygame.transform.scale(farmground,(1500,850))

def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))
green=(0,255,0)
red=(255,0,0)
grey=(127,127,127)
black=(0,0,0)
week=1
day=0


#Collecting Stage
class WorkerAnt:
    def __init__(self,x,y):
        self.x=x
        self.y=y
        self.target_x=x
        self.target_y=y
        self.img='assets/ant.png'
        self.direction='right'
        self.speed=200
        self.is_moving=False
        self.carrying=None
        images_path='assets/carpenter-ant'
        self.images=[pygame.transform.rotate(pygame.transform.scale(pygame.image.load(f"{images_path}/{f}").convert_alpha(), (24*2,19*2)),-90) for f in os.listdir(images_path) if f.endswith(".png")]  
        self.img=pygame.image.load(self.img).convert_alpha()
        self.img=pygame.transform.scale(self.img,(24*2,19*2))
        self.rect=pygame.Rect(x-24,y-19,24*2,19*2)
        self.animation_timer=0
        self.animation_speed=0.02
        self.frame_index=0
        self.angle=0.0
        self.img=self.images[self.frame_index]
    def draw(self,screen):
        screen.blit(self.img, (self.x-24, self.y-19))
    def update(self):
        self.rect=pygame.Rect(self.x-24,self.y-19,24*2,19*2)
    def move_towards(self,dt):
        dx=self.target_x-self.x
        self.direction='right' if dx>0 else 'left'
        dy=self.target_y-self.y
        distance=math.hypot(dx,dy)
        if distance<=self.speed*dt:
            self.x=self.target_x
            self.y=self.target_y
            self.is_moving=False
            return
        else:
            self.is_moving=True
            self.x+=dx/distance*self.speed*dt
            self.y+=dy/distance*self.speed*dt
        target_angle=math.degrees(math.atan2(dy,dx))
        delta=(target_angle-self.angle+180)%360-180
        self.angle += max(-3, min(3, delta))
        self.angle%=360
        frame=self.images[self.frame_index%len(self.images)]
        self.img=pygame.transform.rotate(frame, -self.angle)

class Food:
    def __init__(self,x,y,gacha):
        self.x=x
        self.y=y
        self.count=0
        if gacha<50:
            self.type='bread'
        elif gacha>=50 and gacha<91:
            self.type='apple'
        elif gacha>=91:
            self.type='mosquito'
        if self.type=='bread':
            images_path='assets/food/bread'
            self.images=[pygame.transform.scale(pygame.image.load(f"{images_path}/{f}").convert_alpha(), (32*8, 20*8)) for f in os.listdir(images_path) if f.endswith(".png")]
            self.rect=pygame.Rect(x,y,32*8,20*8)
            self.crumb=pygame.transform.scale(pygame.image.load('assets/food/breadcrumb.png').convert_alpha(), (5*12,5*12))
        if self.type=='apple':
            images_path='assets/food/apple'
            self.images=[pygame.transform.scale(pygame.image.load(f"{images_path}/{f}").convert_alpha(), (20*8, 19*8)) for f in os.listdir(images_path) if f.endswith(".png")]
            self.rect=pygame.Rect(x,y,20*8,19*8)
            self.crumb=pygame.transform.scale(pygame.image.load('assets/food/apple-crumb.png').convert_alpha(), (5*12,5*12))
        if self.type=='mosquito':
            images_path='assets/food/dead-mosquito'
            self.images=[pygame.transform.scale(pygame.image.load(f"{images_path}/{f}").convert_alpha(), (59*2, 42*2)) for f in os.listdir(images_path) if f.endswith(".png")]
            self.crumb=pygame.transform.scale(pygame.image.load('assets/food/dead-mosquito-crumb.png').convert_alpha(), (5*6,5*6))
        self.img=self.images[self.count]
    def draw(self,screen):
        screen.blit(self.img, (self.x-16*8, self.y-10*8))
    def update(self):
        self.rect=pygame.Rect(self.x,self.y,32*8,20*8)
class Nest:
    def __init__(self,x,y):
        self.x=x
        self.y=y
        self.rect=pygame.Rect(x,y,100,100)
    def draw(self,screen):
        pygame.draw.rect(screen,green,self.rect)

#Comvat Stage
class SoldierAnt:
    def __init__(self,x,y,type):
        self.x=x
        self.y=y
        self.target_x=x
        self.target_y=y
        images_path='assets/carpenter-ant'
        self.images=[pygame.transform.rotate(pygame.transform.scale(pygame.image.load(f"{images_path}/{f}").convert_alpha(), (24*2,19*2)),-90) for f in os.listdir(images_path) if f.endswith(".png")]   
        self.angle=0.0
        self.img=self.images[0]
        self.animation_timer=0
        self.animation_speed=0.02
        self.frame_index=0
        self.rect=pygame.Rect(x-24,y-19,24*2,19*2)
        self.speed=200
        self.type=type
        self.is_moving=False
        self.healthbar=pygame.Rect(x-24,y-30,48,5)
        if self.type=='black':
            self.hp=10
            self.maxhp=10
            self.dmg=2
            self.range=0
            self.attack_speed=1
            self.attack_timer=0
        elif self.type=='wood':
            self.hp=5
            self.maxhp=5
            self.range=500
            self.dmg=0
            self.range=50
            self.attack_speed=1
            self.attack_timer=0
        self.rangerect=pygame.Rect(self.x-24-self.range/2,self.y-19-self.range/2,48+self.range,38+self.range)
    def draw(self,screen):
        screen.blit(self.img, (self.x-24, self.y-19))
    def update(self):
        self.rect=pygame.Rect(self.x-24,self.y-19,48,38)
    def updaterange(self):
        self.rangerect=pygame.Rect(self.x-24-self.range/2,self.y-19-self.range/2,48+self.range,38+self.range)
    def move_towards(self,dt):
        dx=self.target_x-self.x
        self.direction='right' if dx>0 else 'left'
        dy=self.target_y-self.y
        distance=math.hypot(dx,dy)
        if distance<=self.speed*dt:
            self.x=self.target_x
            self.y=self.target_y
            self.is_moving=False
            return
        else:
            self.is_moving=True
            self.x+=dx/distance*self.speed*dt
            self.y+=dy/distance*self.speed*dt
        if self.x<24:
            self.x=24           #chỉnh tùy size, tạm chx cần
        if self.y<19:
            self.y=19
        target_angle=math.degrees(math.atan2(dy,dx))
        delta=(target_angle-self.angle+180)%360-180
        self.angle += max(-3, min(3, delta))
        self.angle%=360
        frame=self.images[self.frame_index%len(self.images)]
        self.img=pygame.transform.rotate(frame, -self.angle)
    def hbupdate(self):
        self.losthealthbar=pygame.Rect(self.x-24,self.y-30,48,5)
        self.healthbar=pygame.Rect(self.x-24,self.y-30,48*self.hp/self.maxhp,5)
    def hb(self,sreen):
        pygame.draw.rect(screen,red,self.losthealthbar)
        pygame.draw.rect(screen,green,self.healthbar)
class Acid:
    def __init__(self,x,y,angle):
        self.direction = angle
        self.x=x
        self.y=y
        self.rect=pygame.Rect(self.x,self.y,10,10)
        self.speed=100
        self.dmg=2
    def draw(self,screen):
        pygame.draw.rect(screen,green,self.rect)
    def update(self):
        self.rect=pygame.Rect(self.x,self.y,10,10)
    def move(self,dt):
        self.x+=dt*self.speed*math.cos(self.direction/180*math.pi)
        self.y+=dt*self.speed*math.sin(self.direction/180*math.pi)
class Enemy:
    def __init__(self,x,y,type):
        self.x=x
        self.y=y
        self.target_x=x
        self.target_y=y
        if type=='mantis':
            self.img='assets/mantis.png'
            self.img=pygame.image.load(self.img).convert_alpha()
            self.img=pygame.transform.scale(self.img,(450,300))
            self.rect=pygame.Rect(x-225,y-150,450,300)
            self.speed=100
            self.hp=250
            self.maxhp=250
            self.dmg=3
            self.range=100
            self.attack_speed=1
            self.attack_timer=0
        if type=='spider':
            pass
        self.healthbar=pygame.Rect(x,y-50-150,450,5)
        self.losthealthbar=pygame.Rect(x,y-50-150,450,5)
    def draw(self,screen):
        screen.blit(self.img, (self.x-225, self.y-150))
    def update(self):
        self.rect=pygame.Rect(self.x-225,self.y-150,450,300)
    def move_towards(self,dt):
        dx=self.target_x-self.x
        dy=self.target_y-self.y
        distance=math.hypot(dx,dy)
        if distance<=self.speed*dt:
            self.x=self.target_x
            self.y=self.target_y
            self.is_moving=False
            return
        else:
            self.is_moving=True
            self.x+=dx/distance*self.speed*dt
            self.y+=dy/distance*self.speed*dt
        if self.x<225: 
            self.x=225     #chỉnh sau này tùy theo size boss
        if self.y<150:
            self.y=150
    def hbupdate(self):
        self.losthealthbar=pygame.Rect(250,0,1000,30)
        self.healthbar=pygame.Rect(250,0,1000*self.hp/self.maxhp,30)
    def hb(self,sreen):
        pygame.draw.rect(screen,grey,self.losthealthbar)
        pygame.draw.rect(screen,red,self.healthbar)
        pygame.draw.rect(screen,black,self.losthealthbar,width=5)

timeline=pygame.Rect(150,50,1200,30)


        
#Collecting Stage

foods=[]
nest=Nest(100,50)
player=WorkerAnt(100,50)
food_spawn_timer=0
vitamin=0
running=True

#Combat Stage
mantis=Enemy(1000,400,'mantis')
mantis2=Enemy(1000,0,'mantis')
spider=Enemy(1000,400,'spider')
bosses=[mantis,mantis2]
soldiers=[SoldierAnt(0,0,'black')]
ant_spawn_timer=6
acids=[]

#Game Loop
while running:
    dt = clock.tick(60) / 1000
    #INPUT HANDLING
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if stage=='collecting':
            if event.type==pygame.MOUSEBUTTONDOWN:
                player.target_x=event.pos[0]
                player.target_y=event.pos[1]
        keys=pygame.key.get_pressed()
        if keys[pygame.K_1]:
            stage='collecting'
        if keys[pygame.K_2]:
            stage='combat'  
        if keys[pygame.K_0]:
            day+=0.5



    #LOGIC HANDLING
    if stage=='collecting':
        player.move_towards(dt)
        food_spawn_timer-=dt
        if food_spawn_timer<0:
            food_spawn_timer=15
            foods.append(Food(random.randint(400,1500),random.randint(100,850),random.randint(0,100))) 

        
        player.update()
        for food in foods:
            food.update()
            if player.rect.colliderect(food.rect) and player.carrying==None:
                if food.count<5:
                    food.count+=1
                    food.img=food.images[food.count]
                    player.carrying=food
        if player.rect.colliderect(nest.rect) and player.carrying:
            player.carrying=None
            vitamin+=1
        if vitamin>=10:
            stage='combat'
    if stage=='combat':
        if bosses:
            ant_spawn_timer-=dt
            if ant_spawn_timer<0:
                ant_spawn_timer=0.5
                soldiers.append(SoldierAnt(0,0,'black'))
                soldiers.append(SoldierAnt(0,0,'wood'))
        mantis.move_towards(dt)
        for soldier in soldiers:
            soldier.move_towards(dt)
            soldier.update()
        mantis.update()
        for soldier in soldiers:
            if not soldier.rangerect.colliderect(mantis.rect):
                soldier.target_x=mantis.x+random.uniform(-255,255)-soldier.range
                soldier.target_y=mantis.y+random.uniform(-150,150)-soldier.range    
            else:
                if soldier.type=='black':                
                    soldier.attack_timer+=dt
                    if soldier.attack_timer>=soldier.attack_speed:
                        mantis.hp-=soldier.dmg
                        soldier.attack_timer=0
                elif soldier.type=='wood':
                    if soldier.rect.colliderect(mantis.rect):
                        soldier.target_x=mantis.x-255-random.uniform(0,soldier.range)
                        soldier.target_y=mantis.y-255-random.uniform(0,soldier.range)
                    soldier.attack_timer+=dt
                    dy=soldier.target_y-soldier.y
                    dx=soldier.target_x-soldier.x
                    if soldier.attack_timer>=soldier.attack_speed:
                        acids.append(Acid(soldier.x,soldier.y,math.degrees(math.atan2(dy,dx))))
                        soldier.attack_timer=0
            if mantis.hp<=0:
                if bosses:
                    bosses.remove(mantis)
        for acid in acids:
            acid.update()
            if acid.rect.colliderect(mantis.rect):
                mantis.hp-=acid.dmg
                acids.remove(acid)
            if mantis.hp<=0:
                if bosses:
                    bosses.remove(mantis)
        mantis.update()
        nearest_soldier=None
        for soldier in soldiers:
            if nearest_soldier==None:
                nearest_soldier=soldier
            else:
                if math.hypot(soldier.x-mantis.x,soldier.y-mantis.y)<math.hypot(nearest_soldier.x-mantis.x,nearest_soldier.y-mantis.y):
                    nearest_soldier=soldier
                else:
                    if math.hypot(soldier.x-mantis.x,soldier.y-mantis.y)<math.hypot(nearest_soldier.x-mantis.x,nearest_soldier.y-mantis.y):
                        nearest_soldier=soldier
            if nearest_soldier!=None:
                mantis.target_x=nearest_soldier.x
                mantis.target_y=nearest_soldier.y
                if mantis.rect.colliderect(nearest_soldier.rect):
                    mantis.attack_timer+=dt
                    if mantis.attack_timer>=mantis.attack_speed:
                        nearest_soldier.hp-=mantis.dmg
                        if nearest_soldier.hp<=0:
                            soldiers.remove(nearest_soldier)
                        mantis.attack_timer=0








    #RENDER HANDLING
    if stage=='collecting':
        screen.blit(farmground,(0,0))
        for food in foods:
            food.draw(screen)
        player.draw(screen)
        if player.carrying!=None:
            screen.blit(player.carrying.crumb,(player.x-15,player.y-15))
        draw_text(str(vitamin),basic_font,(0,0,0),1000,0)
        if player.is_moving==True:
            player.animation_timer+=dt
            if player.animation_timer>player.animation_speed:
                player.animation_timer=0
                player.frame_index+=1
                player.img=player.images[player.frame_index%len(player.images)]
        pygame.draw.rect(screen,(255,200,0),timeline)
        for i in range(0,1201,200):
            pygame.draw.rect(screen,(255,255,0),(pygame.Rect(150+i,50,50,50)))
        pygame.draw.rect(screen,(255,0,0),(pygame.Rect(150+day%7*200,50,50,50)))

    if stage=='combat':
        screen.fill((255, 255, 255))
        mantis.draw(screen)
        mantis.hbupdate()
        mantis.hb(screen)
        for soldier in soldiers:
            soldier.draw(screen)
            soldier.hbupdate()
            soldier.hb(screen)
            soldier.updaterange()
            pygame.draw.rect(screen,red,soldier.rect,width=1)
        for acid in acids:
            acid.draw(screen)
            acid.update()
            acid.move(dt)

    pygame.display.update()


pygame.quit()
