import pygame
import random
import math
import os

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((1500, 850))
pygame.display.set_caption("Ant Colony")
stage='nest'
clock=pygame.time.Clock()
cursor_img=pygame.image.load('assets/worker-ant/pixil-frame-0.png').convert_alpha()
cursor_img=pygame.transform.rotate(pygame.transform.scale(cursor_img,(19,24)),45)
button_font=pygame.font.Font('assets/font.ttf', 40)
ui_font=pygame.font.Font('assets/font.ttf', 70)
hatch_font=pygame.font.Font('assets/font.ttf', 20)
text_font=pygame.font.Font('assets/font.ttf', 15)

farmground=pygame.image.load('assets/farmground.png').convert()
battleground=pygame.image.load('assets/battleground.png').convert()
nest_background=pygame.image.load('assets/nest.png').convert()
farmground=pygame.transform.scale(farmground,(1500,850))
battleground=pygame.transform.scale(battleground,(1500,850))
nest_background=pygame.transform.scale(nest_background,(1500,850))
food_icon=pygame.image.load('assets/food/food-icon.png').convert_alpha()
food_icon=pygame.transform.scale(food_icon,(100,100))
stamina_icon=pygame.image.load('assets/stamina-icon.png').convert_alpha()
stamina_icon=pygame.transform.scale(stamina_icon,(100,100))



black_screen=pygame.Surface((1500,850),pygame.SRCALPHA)
darkness=0

def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))
green=(0,255,0)
red=(255,0,0)
grey=(127,127,127)
black=(0,0,0)





class Button:
    def __init__(self, x, y, function):
        self.x=x
        self.y=y
        self.function=function
        self.rect=pygame.Rect(x,y,210,100)
        self.active_color=(255,127,0)
        self.passive_color=(150,75,0)
        self.color=self.passive_color
        self.border_color=(0,0,0)
    def draw(self,screen):
        if self.function!='collection':
            pygame.draw.rect(screen,self.color,self.rect)
            if self.function=='hatch':
                text='Hatch'
            if self.function=='storage':
                text='Barrack'
            if self.function=='sleep':
                text='Sleep'
            text_surface= button_font.render(text, True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=self.rect.center)
            screen.blit(text_surface, text_rect)
            pygame.draw.rect(screen,button.border_color,button.rect,width=2)
        else:
            text='Collect'
            if not collected:
                pygame.draw.rect(screen,self.color,self.rect)
                text_surface= button_font.render(text, True, (255, 255, 255))
                text_rect = text_surface.get_rect(center=self.rect.center)
                screen.blit(text_surface, text_rect)
                pygame.draw.rect(screen,button.border_color,button.rect,width=2)
class ReturnButton:
    def __init__(self, x, y):
        self.x=x
        self.y=y
        self.passive_img=pygame.image.load('assets/return-button.png').convert_alpha()
        self.active_img=pygame.image.load('assets/return-button-active.png').convert_alpha()
        self.passive_img=pygame.transform.scale(self.passive_img,(100,100))
        self.active_img=pygame.transform.scale(self.active_img,(100,100))
        self.img=self.passive_img
        self.rect=pygame.Rect(x,y,100,100)
    def draw(self,screen):
        screen.blit(self.img,(self.x,self.y))
        self.rect=pygame.Rect(self.x,self.y,100,100)
class HatchButton:
    def __init__(self, x, y,type):
        self.x=x
        self.y=y
        self.type=type
        self.rect=pygame.Rect(x,y,250,50)
        self.active_color=(155,155,100)
        self.passive_color=(255,255,200)
        self.color=self.passive_color
        self.border_color=(0,0,0)
    def draw(self,screen):
        pygame.draw.rect(screen,self.color,self.rect)
        pygame.draw.rect(screen,self.border_color,self.rect,width=2)
        text_surface= hatch_font.render(self.type, True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)
class InfoButton:
    def __init__(self, x, y,type):
        self.x=x
        self.y=y
        self.type=type
        self.img=pygame.image.load('assets/info-icon.png').convert_alpha()
        self.img=pygame.transform.scale(self.img,(30,30))
        self.rect=pygame.Rect(x,y,30,30)
        if self.type=='scout':
            self.info='Increase the daiy amount of food by 1'
            self.cost='Cost: 5 calories'
        if self.type=='worker':
            self.info='Increase the number of workers by 1'
            self.cost='Cost: 5 calories'
        if self.type=='soldier':
            self.info='Add a soldier of the type below to your army'
            self.cost='Cost: 5 calories + special ingredient for special ants'
        self.hovered=False
    def draw(self,screen):
        screen.blit(self.img,(self.x,self.y))
        self.rect=pygame.Rect(self.x,self.y,30,30)

class Cocoon:
    def __init__(self,x,y,type):
        self.x=x
        self.y=y
        self.type=type
        self.rect=pygame.Rect(x,y,8*7,18*7)
        if self.type==1:self.img=pygame.image.load('assets/cocoon-1.png').convert_alpha()
        if self.type==2:self.img=pygame.image.load('assets/cocoon-2.png').convert_alpha()
        if self.type==3:self.img=pygame.image.load('assets/cocoon-3.png').convert_alpha()
        self.img=pygame.transform.scale(self.img,(8*10,18*10))
    def draw(self,screen):
        screen.blit(self.img,(self.x,self.y))
        self.rect=pygame.Rect(self.x,self.y,8*10,18*10)
class Icon:
    def __init__(self,x,y,type):
        self.x=x
        self.y=y
        self.type=type
        if self.type=='leaf':self.img,self.count=pygame.image.load('assets/icons/leaf.png').convert_alpha(),leaf
        if self.type=='honey':self.img,self.count=pygame.image.load('assets/icons/honey.png').convert_alpha(),honey
        if self.type=='seed':self.img,self.count=pygame.image.load('assets/icons/seed.png').convert_alpha(),apple_seed
        if self.type=='blood':self.img,self.count=pygame.image.load('assets/icons/blood.png').convert_alpha(),blood
        if self.type=='wheat':self.img,self.count=pygame.image.load('assets/icons/wheat.png').convert_alpha(),wheat
        if self.type=='salt':self.img,self.count=pygame.image.load('assets/icons/salt.png').convert_alpha(),salt
        self.img=pygame.transform.scale(self.img,(50,50))
        
    def draw(self,screen):
        self.rect=pygame.Rect(self.x,self.y,120,50)
        pygame.draw.rect(screen,(255,255,255),self.rect)
        screen.blit(self.img,(self.x,self.y))
        draw_text(str(self.count),text_font,(0,0,0),self.x+60,self.y+10)
    def update(self,leaf,honey,apple_seed,blood,wheat,salt):
        if self.type=='leaf':self.count=leaf
        if self.type=='honey':self.count=honey
        if self.type=='seed':self.count=apple_seed
        if self.type=='blood':self.count=blood
        if self.type=='wheat':self.count=wheat
        if self.type=='salt':self.count=salt
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
        images_path='assets/worker-ant'
        self.images=[pygame.transform.rotate(pygame.transform.scale(pygame.image.load(f"{images_path}/{f}").convert_alpha(), (19*2,24*2)),-90) for f in os.listdir(images_path) if f.endswith(".png")]  

        self.rect=pygame.Rect(x-19,y-24,19*2,24*2)
        self.animation_timer=0
        self.animation_speed=0.02
        self.frame_index=0
        self.angle=0.0
        self.img=self.images[self.frame_index]
    def draw(self,screen):
        screen.blit(self.img, (self.x-19, self.y-24))
    def update(self):
        self.rect=pygame.Rect(self.x-19,self.y-24,19*2,24*2)
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
        if gacha<5:self.type='chips'
        elif 5<=gacha<20:self.type='apple'
        elif 20<=gacha<35:self.type='honeycomb'
        elif 35<=gacha<50:self.type='leaf'
        elif 50<=gacha<65:self.type='mosquito'
        elif 65<=gacha<=100:self.type='bread'
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
        if self.type=='chips':
            images_path='assets/food/chips'
            self.images=[pygame.transform.scale(pygame.image.load(f"{images_path}/{f}").convert_alpha(), (35*6, 22*6)) for f in os.listdir(images_path) if f.endswith(".png")]
            self.rect=pygame.Rect(x,y,35*6,22*6)
            self.crumb=pygame.transform.scale(pygame.image.load('assets/food/chips-crumb.png').convert_alpha(), (5*10,5*10  ))
        if self.type=='mosquito':
            images_path='assets/food/dead-mosquito'
            self.images=[pygame.transform.scale(pygame.image.load(f"{images_path}/{f}").convert_alpha(), (59*2, 42*2)) for f in os.listdir(images_path) if f.endswith(".png")]
            self.crumb=pygame.transform.scale(pygame.image.load('assets/food/dead-mosquito-crumb.png').convert_alpha(), (5*6,5*6))
            self.rect=pygame.Rect(x,y,59*2,42*2)
        if self.type=='honeycomb':
            images_path='assets/food/honeycomb'
            self.images=[pygame.transform.scale(pygame.image.load(f"{images_path}/{f}").convert_alpha(), (30*7, 31*7)) for f in os.listdir(images_path) if f.endswith(".png")]
            self.rect=pygame.Rect(x,y,30*7,31*7)
            self.crumb=pygame.transform.scale(pygame.image.load('assets/food/honey-crumb.png').convert_alpha(), (11*6,14*6))
        if self.type=='leaf':
            images_path='assets/food/leaf'
            self.images=[pygame.transform.scale(pygame.image.load(f"{images_path}/{f}").convert_alpha(), (23*15, 16*15)) for f in os.listdir(images_path) if f.endswith(".png")]
            self.rect=pygame.Rect(x,y,23*10,16*10)
            self.crumb=pygame.transform.scale(pygame.image.load('assets/food/leaf-crumb.png').convert_alpha(), (5*10,5*10))
        self.img=self.images[self.count]
        self.width=self.rect.width
        self.height=self.rect.height
    def draw(self,screen):
        screen.blit(self.img, (self.x-0.5*self.width, self.y-0.5*self.height))
    def update(self):
        self.rect=pygame.Rect(self.x-0.5*self.width,self.y-0.5*self.height,self.width,self.height)
class Nest:
    def __init__(self,x,y):
        self.x=x
        self.y=y
        self.rect=pygame.Rect(x,y,100,100)
    def draw(self,screen):
        pygame.draw.rect(screen,green,self.rect)

#Combat Stage
class SoldierAnt:
    def __init__(self,x,y,type,hpbuff,dmgbuff):
        self.x=x
        self.y=y
        self.target_x=x
        self.target_y=y
        if type=='black':images_path='assets/black-ant-walking'
        if type=='wood':images_path='assets/wood-ant-walking'
        if type=='dracula':images_path='assets/dracula-ant-walking'
        if type=='fireant':images_path='assets/fire-ant-walking'
        if type=='leafcutter':images_path='assets/leafcutter-ant-walking'        
        self.images=[pygame.transform.rotate(pygame.transform.scale(pygame.image.load(f"{images_path}/{f}").convert_alpha(), (19*2,24*2)),-90) for f in os.listdir(images_path) if f.endswith(".png")]   
        self.angle=0.0
        self.img=self.images[0]
        self.animation_timer=0
        self.animation_speed=0.02
        self.frame_index=0
        self.rect=pygame.Rect(x-19,y-24,19*2,24*2)
        self.speed=200
        self.type=type
        self.is_moving=False
        self.healthbar=pygame.Rect(x-19,y-30,38,5)
        if self.type=='black':
            self.hp=10+hpbuff-dmgbuff
            self.maxhp=10+hpbuff-dmgbuff
            self.dmg=2+dmgbuff
            self.range=0
            self.attack_speed=1
            self.attack_timer=0
        elif self.type=='wood':
            self.hp=5+hpbuff-dmgbuff
            self.maxhp=5+hpbuff-dmgbuff
            self.range=200
            self.dmg=2+dmgbuff
            self.attack_speed=3
            self.attack_timer=0
        elif self.type=='dracula':
            self.hp=10+hpbuff-dmgbuff
            self.maxhp=10+hpbuff-dmgbuff
            self.range=0
            self.dmg=2+dmgbuff
            self.attack_speed=1
            self.attack_timer=0
        elif self.type=='fireant':
            self.hp=15+hpbuff-dmgbuff
            self.maxhp=15+hpbuff-dmgbuff
            self.range=0
            self.dmg=0+dmgbuff
            self.attack_speed=2
            self.attack_timer=0
        elif self.type=='leafcutter':
            self.hp=15+hpbuff-dmgbuff
            self.maxhp=15+hpbuff-dmgbuff
            self.range=0
            self.dmg=2+dmgbuff
            self.attack_speed=1
            self.attack_timer=0    
        self.rangerect=pygame.Rect(self.x-19-self.range/2,self.y-24-self.range/2,38+self.range,48+self.range)
    def draw(self,screen):
        screen.blit(self.img, (self.x-19, self.y-24))
    def update(self):
        self.rect=pygame.Rect(self.x-19,self.y-24,38,48)
    def updaterange(self):
        self.rangerect=pygame.Rect(self.x-19-self.range/2,self.y-24-self.range/2,38+self.range,48+self.range)
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
        if self.x<(19+10):
            self.x=19+10           #chỉnh tùy size, tạm chx cần
        if self.y<(24+10):
            self.y=24+10
        if self.x>(1500-19-10):
            self.x=1500-19-10         #chỉnh tùy size
        if self.y>(850-24-10):
            self.y=850-24-10
        target_angle=math.degrees(math.atan2(dy,dx))
        delta=(target_angle-self.angle+180)%360-180
        self.angle += max(-4, min(4, delta))
        self.angle%=360
        frame=self.images[self.frame_index%len(self.images)]
        self.img=pygame.transform.rotate(frame, -self.angle)
    def hbupdate(self):
        self.losthealthbar=pygame.Rect(self.x-19,self.y-30,38,5)
        self.healthbar=pygame.Rect(self.x-19,self.y-30,38*self.hp/self.maxhp,5)
    def hb(self):
        pygame.draw.rect(screen,red,self.losthealthbar)
        pygame.draw.rect(screen,green,self.healthbar)
class Acid:
    def __init__(self,x,y,angle,dmg):
        self.direction = angle
        self.x=x
        self.y=y
        self.rect=pygame.Rect(self.x,self.y,10,10)
        self.img=pygame.image.load('assets/acid.png').convert_alpha()
        self.speed=100
        self.dmg=dmg
    def draw(self,screen):
        screen.blit(self.img, (self.x,self.y))
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
        self.type=type
        if type=='mantis':
            walking_path='assets/mantis-walking'
            attack1_path='assets/mantis-attack-1'
            self.walks=[pygame.transform.rotate(pygame.transform.scale(pygame.image.load(f"{walking_path}/{f}").convert_alpha(), (34*10,54*10)),-90) for f in os.listdir(walking_path) if f.endswith(".png")]
            self.attacks1=[pygame.transform.rotate(pygame.transform.scale(pygame.image.load(f"{attack1_path}/{f}").convert_alpha(), (34*10,54*10)),-90) for f in os.listdir(attack1_path) if f.endswith(".png")]
            self.rect=pygame.Rect(x-34*5,y-54*5,250,200)   
            self.speed=100
            self.hp=500
            self.maxhp=500
            self.dmg=5
            self.range=100
            self.attack_speed=1
            self.attack_timer=0
            self.animation_timer=0
            self.animation_speed=0.1
            self.attack_animation_speed=0.05
            self.attack_animation_timer=0
            self.attack_duration=0.6
            self.attack_hit=False
            self.attack_target=None
            self.attack_timer=0
            self.frame_index=0
            self.img=self.walks[self.frame_index]
            self.skill_duration=5
            self.skill_activate=0
            
            
            #cái quyết định tọa độ khung và vị trí khung để random chạm cho con kiến, tạm để không, sau này cần scale
            
        elif type=='grasshopper':
            walks_path='assets/grasshopper-walking'
            attacks_path='assets/grasshopper-attack-1'
            self.walks=[pygame.transform.rotate(pygame.transform.scale(pygame.image.load(f"{walks_path}/{f}").convert_alpha(), (34*10,54*10)),-90) for f in os.listdir(walks_path) if f.endswith(".png")]
            self.attacks1=[pygame.transform.rotate(pygame.transform.scale(pygame.image.load(f"{attacks_path}/{f}").convert_alpha(), (34*10,54*10)),-90) for f in os.listdir(attacks_path) if f.endswith(".png")]
            self.img=self.walks[0]
            self.rect=pygame.Rect(x-225,y-150,450,300)
            self.speed=200
            self.hp=250
            self.maxhp=250
            self.dmg=3
            self.range=100
            self.attack_speed=1
            self.attack_timer=0
            self.skill_duration=5
            self.skill_activate=0
            
            self.animation_timer=0
            self.animation_speed=0.1
            self.attack_animation_speed=0.05
            self.attack_animation_timer=0
            self.attack_duration=0.6
            self.attack_hit=False
            self.attack_target=None
            self.attack_timer=0
            self.frame_index=0
            self.img=self.walks[self.frame_index]

        self.angle=0.0
        self.is_moving=False
        self.is_attacking=False
        self.healthbar=pygame.Rect(x,y-50-150,450,5)
        self.losthealthbar=pygame.Rect(x,y-50-150,450,5)            
    def draw(self,screen):
        screen.blit(self.img, (self.x-225, self.y-150))
    def update(self):
        self.rect=pygame.Rect(self.x-34*5,self.y,350,250)
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
        if self.x<(250): 
            self.x=250     #chỉnh sau này tùy theo size boss
        if self.y<(200):
            self.y=200
        if self.x>(1500-200): 
            self.x=1500-200     #chỉnh sau này tùy theo size boss
        if self.y>(850-200):
            self.y=850-200
        if self.type=='mantis':
            target_angle=math.degrees(math.atan2(dy,dx))
            delta=(target_angle-self.angle+180)%360-180
            self.angle += max(-1, min(1, delta))
            self.angle%=360
            frame=self.walks[self.frame_index%len(self.walks)]
            self.img=pygame.transform.rotate(frame, -self.angle)
    def skill_grasshopper(self,dt):
        dx=self.target_x-self.x
        dy=self.target_y-self.y
        distance=math.hypot(dx,dy)
        if distance<=1000*dt:
            self.x=self.target_x
            self.y=self.target_y
            self.is_moving=False
            return
        else:
            self.is_moving=True
            self.x+=dx/distance*1000*dt
            self.y+=dy/distance*1000*dt
    def hbupdate(self):
        self.losthealthbar=pygame.Rect(250,0,1000,30)
        self.healthbar=pygame.Rect(250,0,1000*self.hp/self.maxhp,30)
    def hb(self):
        pygame.draw.rect(screen,grey,self.losthealthbar)
        pygame.draw.rect(screen,red,self.healthbar)
        pygame.draw.rect(screen,black,self.losthealthbar,width=5)



class Slash:
    def _init_(self,x,y,angle):
        self.angle=angle
        self.x=x
        self.y=y
        self.rect=pygame.rect
    def draw(self):
        pygame.draw.arc(screen, (255, 255, 255), (100, 100, 200, 200), 0, math.pi, 2)
        
#Nest Stage        
timeline=pygame.Rect(150,50,1200,30)
buttons=[Button(950,150,'collection'),Button(400,580,'hatch'),Button(400,280,'storage'),Button(1000,600,'sleep')]
hatch_buttons=[HatchButton(200,450,'worker ant'),HatchButton(600,450,'soldier ant'),HatchButton(1000,450,'scout ant'),HatchButton(600,515,'leafcutter ant'),HatchButton(600,580,'wood ant'),HatchButton(600,645,'fire ant'),HatchButton(600,710,'dracula ant')]
hatching=False
storaging=False
transition=False
transition_speed=100
menu_on=False
ant_price=5
menu=pygame.Rect(150,200,1200,600)
return_button_nest=ReturnButton(1220,220)
info_icons=[InfoButton(350,220,'worker'),InfoButton(750,220,'soldier'),InfoButton(1150,220,'scout')]
cocoons=[Cocoon(280,250,1),Cocoon(680,250,2),Cocoon(1080,250,3)]
notifications=[]
hatch_icons=[Icon(100,50,'leaf'),Icon(200,50,'honey'),Icon(300,50,'seed'),Icon(400,50,'blood')]
barrack_icons=[Icon(500,50,'wheat'),Icon(600,50,'salt')]
#Storage
blood=0
wheat=0
apple_seed=0
salt=0
honey=0
leaf=0



#Collecting Stage
max_foods=2
week=1
day=0
max_stamina=3
collected=False
stamina=3
slashes=[]
foods=[]
nest=Nest(100,50)
workers=[WorkerAnt(100,50)]
food_spawn_timer=0
calories=0
running=True

#Combat Stage
mantis=Enemy(0,0,'mantis')
grasshopper=Enemy(1000,400,'grasshopper')
bosses=[mantis]
soldiers=[]
ant_spawn_timer=0
acids=[]
choosecombat=False
burn=0
burnspeed=0.5
burn_timer=0

#Game Loop
while running:
    dt = clock.tick(60) / 1000
    #INPUT HANDLING
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if stage=='collecting':
            if event.type==pygame.MOUSEBUTTONDOWN:
                for worker in workers:
                    worker.target_x=event.pos[0]+random.randint(-30,30)
                    worker.target_y=event.pos[1]+random.randint(-30,30)
        keys=pygame.key.get_pressed()
        if keys[pygame.K_1]:
            stage='collecting'
        if keys[pygame.K_2]:
            stage='combat'  
            choosecombat=True
        if keys[pygame.K_3]:
            stage='combat2'
            choosecombat=True
        mouse_pos=pygame.mouse.get_pos()

        #Nest Stage
        if stage=='nest':
            for button in buttons:
                if button.rect.collidepoint(mouse_pos) and menu_on==False:
                    button.color=button.active_color
                    button.border_color=(255,255,255)
                    if event.type==pygame.MOUSEBUTTONDOWN:
                        if button.function=='collection' and collected==False:
                            stage='collecting'
                            transition=True
                            darkness=255
                            for i in range(max_foods):
                                foods.append(Food(random.randint(400,1300),random.randint(100,750),random.randint(0,100)))
                        if button.function=='sleep' and not transition:
                            day+=1
                            stamina=max_stamina
                            collected=False
                            transition=True
                            darkness=255
                        if button.function=='storage' and not menu_on:
                            menu_on=True
                            storaging=True
                        if button.function=='hatch' and not menu_on:
                            menu_on=True
                            hatching=True
                else:
                    button.color=button.passive_color
                    button.border_color=(0,0,0)
            if menu_on:
                if event.type==pygame.MOUSEBUTTONDOWN:
                    if not menu.collidepoint(mouse_pos):
                        menu_on=False
                        storaging=False
                        hatching=False
                if return_button_nest.rect.collidepoint(mouse_pos):
                    return_button_nest.img=return_button_nest.active_img
                    if event.type==pygame.MOUSEBUTTONDOWN:
                        menu_on=False
                        storaging=False
                        hatching=False
                else:
                    return_button_nest.img=return_button_nest.passive_img
                if hatching:
                    for button in hatch_buttons:
                        if button.rect.collidepoint(mouse_pos):
                            button.color=button.active_color
                            button.border_color=(255,255,255)
                            if event.type==pygame.MOUSEBUTTONDOWN:
                                if button.type=='worker ant' and calories>=5:
                                    calories-=5
                                    workers.append(WorkerAnt(100,50))
                                if button.type=='scout ant' and calories>=5:
                                    calories-=5
                                    max_foods+=1
                                if button.type=='soldier ant' and calories>=5:
                                    calories-=5
                                    soldiers.append(SoldierAnt(1500,850,'black',wheat,salt))
                                if button.type=='leafcutter ant' and calories>=5 and leaf>0:
                                    calories-=5
                                    leaf-=1
                                    soldiers.append(SoldierAnt(1500,850,'leafcutter',wheat,salt))
                                if button.type=='wood ant' and calories>=5 and honey>0:
                                    calories-=5
                                    honey-=1
                                    soldiers.append(SoldierAnt(1500,850,'wood',wheat,salt))
                                if button.type=='fire ant' and calories>=5 and apple_seed>0:
                                    calories-=5
                                    apple-=1
                                    soldiers.append(SoldierAnt(1500,850,'fireant',wheat,salt))
                                if button.type=='dracula ant' and calories>=5 and blood_clot>0:
                                    calories-=5
                                    soldiers.append(SoldierAnt(1500,850,'dracula',wheat,salt))
                        else:
                            button.color=button.passive_color
                            button.border_color=(0,0,0)
                    for icon in info_icons:
                        if icon.rect.collidepoint(mouse_pos):
                            icon.hovered=True
                        else:
                            icon.hovered=False


    #LOGIC HANDLING
    if stage=='nest':
        pass
        if day==6:
            choosecombat=True
            stage='combat'
        if day==13:
            choosecombat=True
            stage='combat2'




    if stage=='collecting':
        for worker in workers:
            worker.move_towards(dt)
            worker.update()
            for food in foods:
                food.update()
                if worker.rect.colliderect(food.rect) and worker.carrying==None:
                    if food.count<5:
                        food.count+=1
                        food.img=food.images[food.count]
                        worker.carrying=food
                
            if worker.rect.colliderect(nest.rect) and worker.carrying:
                if worker.carrying.count==4:
                    if worker.carrying.type=='mosquito': blood+=1
                    if worker.carrying.type=='bread':wheat+=1
                    if worker.carrying.type=='apple':apple_seed+=1
                    if worker.carrying.type=='chips':salt+=1
                    if worker.carrying.type=='honeycomb':honey+=1
                    if worker.carrying.type=='leaf':leaf+=1
                worker.carrying=None
                calories+=2
                stamina-=1/len(workers)

            if stamina<=0:
                stage='nest'
                collected=True
                foods=[]
                transition=True
                darkness=255
        
    if stage=='combat' or stage=='combat2':
        if choosecombat:
            if stage=='combat':
                bosses.append(mantis)
                if len(bosses)>1:
                    bosses.pop(0)
            elif stage=='combat2':
                bosses.append(grasshopper)
                if len(bosses)>1:
                    bosses.pop(0)
            skill=False
            choosecombat=False
        if bosses:
            ant_spawn_timer-=dt
            if ant_spawn_timer<0:
                ant_spawn_timer=7
                soldiers.append(SoldierAnt(1500,850,'black',0,0))
                soldiers.append(SoldierAnt(1500,850,'wood',0,0))
                soldiers.append(SoldierAnt(1500,850,'dracula',0,0))
                soldiers.append(SoldierAnt(1500,850,'fireant',0,0))
                soldiers.append(SoldierAnt(1500,850,'leafcutter',0,0))
            if not bosses[0].is_attacking and not skill:
                bosses[0].move_towards(dt)
            elif not skill:
                bosses[0].is_moving=False
            for soldier in soldiers:
                soldier.move_towards(dt)
                soldier.update()
            bosses[0].update()
            if not skill:
                for soldier in soldiers:
                    if not soldier.rangerect.colliderect(bosses[0].rect):
                        soldier.target_x=bosses[0].x+random.uniform(-255,255)+soldier.range
                        soldier.target_y=bosses[0].y+random.uniform(-150,150)+soldier.range    
                    else:
                        if soldier.type=='wood':                
                            soldier.attack_timer+=dt
                            if soldier.rect.colliderect(bosses[0].rect):
                                soldier.target_x=bosses[0].x-255-random.uniform(0,soldier.range)
                                soldier.target_y=bosses[0].y-255-random.uniform(0,soldier.range)
                            soldier.attack_timer+=dt
                            if soldier.attack_timer>=soldier.attack_speed:
                                dy=bosses[0].y-soldier.y
                                dx=bosses[0].x-soldier.x
                                acids.append(Acid(soldier.x,soldier.y,math.degrees(math.atan2(dy,dx)),soldier.dmg))
                                soldier.attack_timer=0                            
                        else:
                            if soldier.attack_timer>=soldier.attack_speed:
                                soldier.attack_timer=0
                                if soldier.type=='fire ant':
                                    if burn<100:
                                        burn+=5
                                bosses[0].hp-=soldier.dmg
                                if soldier.type=='dracula':
                                    if soldier.health<soldier.healthmax:
                                        if soldier.health+soldier.dmg/2>soldier.healthmax:
                                            soldier.health=soldier.healthmax
                                        else:
                                            soldier.health+=soldier.dmg/2
        if burn>0:
            burn_timer+=dt
            if burn_timer>=burnspeed:
                bosses[0].hp-=1
                burn_timer=0
                                       
        if bosses and bosses[0].hp<=0:
            try:
                bosses.remove(bosses[0])
            except ValueError:
                pass
            if stage=='combat':
                stage='nest'
                for s in soldiers[:]:
                    s.hp=s.maxhp                
        for acid in acids[:]:
            acid.update()
            if not bosses:
                break
            if not skill:
                if acid.rect.colliderect(bosses[0].rect):
                    bosses[0].hp-=acid.dmg
                    acids.remove(acid)
                if bosses[0].hp<=0:
                    for soldier in soldiers:
                        soldier.hp=soldier.maxhp
                    try:
                        bosses.remove(bosses[0])
                    except ValueError:
                        pass
                    if stage=='combat':
                        stage='nest'
                        for s in soldiers[:]:
                            s.hp=s.maxhp
        if bosses and not skill:
            boss=bosses[0]
            for s in soldiers[:]:
                if s.hp<=0:
                    soldiers.remove(s)       #Clear dead soldiers first
            nearest_soldier=min(soldiers,key=lambda s:math.hypot(s.x-bosses[0].x,s.y-bosses[0].y),default=None)
            
                
            if nearest_soldier:
                bosses[0].target_x=nearest_soldier.x
                bosses[0].target_y=nearest_soldier.y
            if boss.is_attacking:
                boss.is_moving=False
                boss.attack_animation_timer+=dt                    
                if not boss.attack_hit and boss.attack_animation_timer>=boss.attack_animation_speed:
                    boss.attack_hit=True
                    target=boss.attack_target
                    if target is not None and target in soldiers:
                        target.hp-=boss.dmg
                        if target.hp <=0:
                            soldiers.remove(target)
                if boss.attack_animation_timer>=boss.attack_duration:
                    boss.is_attacking=False
                    boss.attack_timer=boss.attack_speed
                    boss.frame_index=0                                  #Reset back to walking after hitting
                    boss.attack_target=None
                    boss.skill_activate+=1
                    if boss.skill_activate>=boss.skill_duration:
                        startslash=True
                        skill=True
                        furthestsoldier=False
                        boss.skill_activate=0
                        chooseskill=random.randint(1,2)
                    
                    
            else:
                boss.attack_timer=max(0.0,boss.attack_timer-dt)     #Only counts when not attacking

                #Start a new attack
                if nearest_soldier and boss.attack_timer==0 and boss.rect.colliderect(nearest_soldier.rect):
                    boss.attack_target=nearest_soldier
                    boss.is_attacking=True
                    boss.attack_hit=False
                    boss.attack_animation_timer=0
        elif bosses and skill:              
            boss=bosses[0]                      
            for s in soldiers[:]:
                if s.hp<=0:
                    soldiers.remove(s)
            if boss.type=='mantis':
                skill=False
            elif boss.type=='grasshopper':
                if chooseskill==1:
                    if not furthestsoldier:
                        furthest_soldier=max(soldiers,key=lambda s:math.hypot(s.x-bosses[0].x,s.y-bosses[0].y),default=None)
                        furthestsoldier=True                   
                    if furthestsoldier:
                        bosses[0].target_x=furthest_soldier.x
                        bosses[0].target_y=furthest_soldier.y-150
                    boss.skill_grasshopper(dt*3)
                    if boss.x==boss.target_x and boss.y==boss.target_y:
                        skill=False
                        for s in soldiers[:]:
                            if s.rect.colliderect(boss.rect):
                                s.hp-=boss.dmg*5
                else:
                    crowd=0
                    if not furthestsoldier:
                        for s in soldiers[:]:
                            if s.x>boss.x:
                                crowd+=1
                            elif s.x<boss.x:
                                crowd-=1
                        if crowd<=0:
                            bosses[0].target_x=1500-34*5
                            bosses[0].target_y=boss.y
                        else:
                            bosses[0].target_x=34*5
                            bosses[0].target_y=boss.y
                    boss.skill_grasshopper(dt)
                    for s in soldiers[:]:
                            if s.rect.colliderect(boss.rect):
                                s.hp-=boss.dmg*5
                    if boss.x==boss.target_x and boss.y==boss.target_y:
                        skill=False

                                           
                    
                



    #RENDER HANDLING
    if stage=='nest':
        pygame.mouse.set_visible(False)
        screen.blit(nest_background,(0,0))
        pygame.draw.rect(screen,(255,200,0),timeline)
        for i in range(0,1201,200):
            pygame.draw.rect(screen,(255,255,0),(pygame.Rect(150+i,50,50,50)))
        pygame.draw.rect(screen,(255,0,0),(pygame.Rect(150+day%7*200,50,50,50)))
        draw_text(f'Day {day+1}',button_font,(0,0,0),150,5)
        for button in buttons:
            button.draw(screen)
        pygame.draw.rect(screen,(240,219,211),(50,120,220,120))
        pygame.draw.rect(screen,(0,0,0),(50,120,220,120),width=5)
        screen.blit(food_icon,(60,130))
        draw_text(str(calories),ui_font,(0,0,0),170,130)
        
        screen.blit(black_screen,(0,0))
        if menu_on:
            pygame.draw.rect(screen,(235,219,200),menu)
            pygame.draw.rect(screen,(0,0,0),menu,width=3)
            return_button_nest.draw(screen)
            pygame.draw.rect(screen,(240,219,211),(50,120,220,120))
            pygame.draw.rect(screen,(0,0,0),(50,120,220,120),width=5)
            if hatching:
                for button in hatch_buttons:
                    button.draw(screen)
                for icon in info_icons:
                    icon.draw(screen)
                for cocoon in cocoons:
                    cocoon.draw(screen)
                for icon in info_icons:
                    if icon.hovered:
                        x,y=icon.x,icon.y
                        w,h=550,100
                        if icon.type=='worker':w-=175
                        if icon.type=='scout':w-=150
                        if icon.type=='scout':x-=200
                        info_rect=pygame.Rect(x,y-150,w,h)
                        pygame.draw.rect(screen,(255,200,200),info_rect)
                        draw_text(icon.info,text_font,(0,0,0),x+10,y-130)
                        draw_text(icon.cost,text_font,(0,0,0),x+10,y-110)
                for icon in hatch_icons:
                    icon.update()
                    icon.draw(screen)
            if storaging:
                for icon in barrack_icons:
                    icon.update(leaf,honey,apple_seed,blood,wheat,salt)
                    icon.draw(screen)
            screen.blit(food_icon,(60,130))
            draw_text(str(calories),ui_font,(0,0,0),170,130)
        mouse_x,mouse_y=pygame.mouse.get_pos()
        screen.blit(cursor_img,(mouse_x,mouse_y))


    if stage=='collecting':
        pygame.mouse.set_visible(True)
        screen.blit(farmground,(0,0))
        for food in foods:
            food.draw(screen)
        for worker in workers:
            worker.draw(screen)
            if worker.carrying!=None:
                screen.blit(worker.carrying.crumb,(worker.x-15,worker.y-15))
            
            if worker.is_moving==True:
                worker.animation_timer+=dt
                if worker.animation_timer>worker.animation_speed:
                    worker.animation_timer=0
                    worker.frame_index+=1
                    worker.img=worker.images[worker.frame_index%len(worker.images)]
        pygame.draw.rect(screen,(240,219,211),(1250,20,220,120))
        pygame.draw.rect(screen,(0,0,0),(1250,20,220,120),width=5)
        screen.blit(stamina_icon,(1260,30))
        draw_text(str(math.ceil(stamina)),ui_font,(0,0,0),1370,30)
        
        screen.blit(black_screen,(0,0))


    if stage=='combat'or stage=='combat2':
        pygame.mouse.set_visible(True)
        screen.blit(battleground,(0,0))
        
        for boss in bosses:
            if stage=='combat' or stage=='combat2':
                walks=getattr(boss,'walks',[])
                attacks1=getattr(boss,'attacks1',[])
                if boss.is_attacking and attacks1:
                    progress=boss.attack_animation_timer/boss.attack_duration   #Boss attack animation
                    index=min(int(progress*len(attacks1)),len(attacks1)-1)
                    boss.img=pygame.transform.rotate(attacks1[index], -boss.angle)
                elif walks:
                #Boss walking animation 
                    if boss.is_moving:
                        boss.animation_timer+=dt
                        if boss.animation_timer>boss.animation_speed:
                            boss.animation_timer=0
                            boss.frame_index+=1
                            boss.img=pygame.transform.rotate(boss.walks[boss.frame_index%len(boss.walks)], -boss.angle)
            boss.draw(screen)
            boss.hbupdate()
            boss.hb()
            pygame.draw.rect(screen,(0,255,0),boss.rect,2)
        for soldier in soldiers:
            if soldier.is_moving==True:
                soldier.animation_timer+=dt
                if soldier.animation_timer>soldier.animation_speed:
                    soldier.animation_timer=0
                    soldier.frame_index+=1
                    soldier.img=pygame.transform.rotate(soldier.images[soldier.frame_index%len(soldier.images)], -soldier.angle)
            soldier.draw(screen)
            soldier.hbupdate()
            soldier.hb()
            soldier.updaterange()
        for acid in acids:
            acid.draw(screen)
            acid.update()
            acid.move(dt)
        for slash in slashes:
            slash.draw()
        screen.blit(black_screen,(0,0))
    #Global Rendering
    black_screen.fill((0,0,0,darkness))
    if menu_on:
        darkness=125
    elif transition:
        darkness-=transition_speed*dt
        if darkness<0:
            darkness=0
            transition=False
    else:
        darkness=0


        
    pygame.display.update()


pygame.quit()
