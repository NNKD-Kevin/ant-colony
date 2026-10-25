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

basic_font=pygame.font.Font('assets/font.ttf', 70)
farmground=pygame.image.load('assets/farmground.png').convert()
battleground=pygame.image.load('assets/battleground.png').convert()
farmground=pygame.transform.scale(farmground,(1500,850))
battleground=pygame.transform.scale(battleground,(1500,850))
food_icon=pygame.image.load('assets/food/food-icon.png').convert_alpha()
food_icon=pygame.transform.scale(food_icon,(100,100))
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
        if gacha<40:
            self.type='bread'
        elif 40<=gacha<50:
            self.type='chips'
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

#Comvat Stage
class SoldierAnt:
    def __init__(self,x,y,type):
        self.x=x
        self.y=y
        self.target_x=x
        self.target_y=y
        images_path='assets/carpenter-ant'
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
            self.hp=10
            self.maxhp=10
            self.dmg=2
            self.range=0
            self.attack_speed=1
            self.attack_timer=0
        elif self.type=='wood':
            self.hp=5
            self.maxhp=5
            self.range=200
            self.dmg=0
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
            self.img='assets/grasshopper.jpg'
            self.img=pygame.image.load(self.img).convert_alpha()
            self.img=pygame.transform.scale(self.img,(450,300))
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
            
            self.attack_animation_speed=0.05    #khúc này thêm tạm để chạy đc con grasshopper
            self.attack_duration=0.6

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
        if self.x<(34*5): 
            self.x=34*5     #chỉnh sau này tùy theo size boss
        if self.y<(54*10):
            self.y=54*10
        if self.x>(1500-34*5): 
            self.x=1500-34*5     #chỉnh sau này tùy theo size boss
        if self.y<(850-54*20):
            self.y=850-54*20
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
        if distance<=3000*dt:
            self.x=self.target_x
            self.y=self.target_y
            self.is_moving=False
            return
        else:
            self.is_moving=True
            self.x+=dx/distance*3000*dt
            self.y+=dy/distance*3000*dt
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
        
        
timeline=pygame.Rect(150,50,1200,30)


        
#Collecting Stage
slashes=[]
foods=[]
nest=Nest(100,50)
player=WorkerAnt(100,50)
food_spawn_timer=0
vitamin=0
running=True

#Combat Stage
mantis=Enemy(200,200,'mantis')
grasshopper=Enemy(1000,400,'grasshopper')
spider=Enemy(1000,400,'spider')
bosses=[mantis]
soldiers=[]
ant_spawn_timer=0
acids=[]
choosecombat=False

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
            choosecombat=True
        if keys[pygame.K_0]:
            day+=0.5
        if keys[pygame.K_3]:
            stage='combat2'
            choosecombat=True  



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
            choosecombat=True
            stage='combat'
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
                ant_spawn_timer=4
                soldiers.append(SoldierAnt(1500,850,'black'))
                soldiers.append(SoldierAnt(1500,850,'wood'))
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
                        if soldier.type=='black':                
                            soldier.attack_timer+=dt
                            if soldier.attack_timer>=soldier.attack_speed:
                                bosses[0].hp-=soldier.dmg
                                soldier.attack_timer=0
                        elif soldier.type=='wood':
                            if soldier.rect.colliderect(bosses[0].rect):
                                soldier.target_x=bosses[0].x-255-random.uniform(0,soldier.range)
                                soldier.target_y=bosses[0].y-255-random.uniform(0,soldier.range)
                            soldier.attack_timer+=dt
                            if soldier.attack_timer>=soldier.attack_speed:
                                dy=bosses[0].y-soldier.y
                                dx=bosses[0].x-soldier.x
                                acids.append(Acid(soldier.x,soldier.y,math.degrees(math.atan2(dy,dx))))
                                soldier.attack_timer=0
        if bosses and bosses[0].hp<=0:
            try:
                bosses.remove(bosses[0])
            except ValueError:
                pass
            if stage=='combat':
                stage='combat2'
                choosecombat=True
        for acid in acids[:]:
            acid.update()
            if not bosses:
                break
            if not skill:
                if acid.rect.colliderect(bosses[0].rect):
                    bosses[0].hp-=acid.dmg
                    acids.remove(acid)
                if bosses[0].hp<=0:
                    try:
                        bosses.remove(bosses[0])
                    except ValueError:
                        pass
                    if stage=='combat':
                        stage='combat2'
                        choosecombat=True
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
                    boss.skill_grasshopper(dt)
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
                    if boss.x==boss.target_x and boss.y==boss.target_y:
                        skill=False
                        for s in soldiers[:]:
                            if s.rect.colliderect(boss.rect):
                                s.hp-=boss.dmg*5
                                           
                    
                
            
            










    #RENDER HANDLING
    if stage=='nest':
        screen.fill((255, 255, 255))
        pygame.draw.rect(screen,(255,200,0),timeline)
        for i in range(0,1201,200):
            pygame.draw.rect(screen,(255,255,0),(pygame.Rect(150+i,50,50,50)))
        pygame.draw.rect(screen,(255,0,0),(pygame.Rect(150+day%7*200,50,50,50)))


    if stage=='collecting':
        screen.blit(farmground,(0,0))
        for food in foods:
            food.draw(screen)
        player.draw(screen)
        if player.carrying!=None:
            screen.blit(player.carrying.crumb,(player.x-15,player.y-15))
        
        if player.is_moving==True:
            player.animation_timer+=dt
            if player.animation_timer>player.animation_speed:
                player.animation_timer=0
                player.frame_index+=1
                player.img=player.images[player.frame_index%len(player.images)]
        pygame.draw.rect(screen,(240,219,211),(1250,20,220,120))
        pygame.draw.rect(screen,(0,0,0),(1250,20,220,120),width=5)
        screen.blit(food_icon,(1260,30))
        draw_text(str(vitamin),basic_font,(0,0,0),1370,30)


    if stage=='combat'or stage=='combat2':
        screen.blit(battleground,(0,0))
        
        for boss in bosses:
            if stage=='combat':
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
    pygame.display.update()


pygame.quit()
