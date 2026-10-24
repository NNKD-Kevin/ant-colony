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

def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))


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
        self.images=[pygame.transform.scale(pygame.image.load(f"{images_path}/{f}").convert_alpha(), (19*2,24*2)) for f in os.listdir(images_path) if f.endswith(".png")]
        
        self.img=pygame.image.load(self.img).convert_alpha()
        self.img=pygame.transform.scale(self.img,(75,50))
        self.rect=pygame.Rect(x,y,75,50)
        self.animation_timer=0
        self.animation_speed=0.02
        self.frame_index=0
        self.img=self.images[self.frame_index]
    def draw(self,screen):
        screen.blit(self.img, (self.x-37.5, self.y-25))
    def update(self):
        self.rect=pygame.Rect(self.x,self.y,50,50)
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
class Food:
    def __init__(self,x,y,color):
        self.x=x
        self.y=y
        self.count=4
        self.color=color
        self.rect=pygame.Rect(x,y,50,50)
    def draw(self,screen):
        pygame.draw.rect(screen,self.color,self.rect)
    def update(self):
        self.rect=pygame.Rect(self.x,self.y,self.count*50,100)
class Nest:
    def __init__(self,x,y):
        self.x=x
        self.y=y
        self.rect=pygame.Rect(x,y,100,100)
    def draw(self,screen):
        pygame.draw.rect(screen,(0,255,0),self.rect)

#Comvat Stage
class SoldierAnt:
    def __init__(self,x,y,type):
        self.x=x
        self.y=y
        self.target_x=x
        self.target_y=y
        self.img='assets/ant.png'
        self.img=pygame.image.load(self.img).convert_alpha()
        self.img=pygame.transform.scale(self.img,(75,50))
        self.rect=pygame.Rect(x,y,75,50)
        self.speed=200
        self.type=type
        self.is_moving=False
        if self.type=='black':
            self.hp=10
            self.dmg=2
            self.range=50
            self.attack_speed=1
            self.attack_timer=0
    def draw(self,screen):
        screen.blit(self.img, (self.x, self.y))
    def update(self):
        self.rect=pygame.Rect(self.x,self.y,75,50)
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
            self.rect=pygame.Rect(x,y,450,300)
            self.speed=100
            self.hp=250
            self.dmg=3
            self.range=100
            self.attack_speed=1
            self.attack_timer=0
    def draw(self,screen):
        screen.blit(self.img, (self.x-225, self.y-150))
    def update(self):
        self.rect=pygame.Rect(self.x,self.y,150,100)
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
        
        
#Collecting Stage
player=WorkerAnt(0,400)
foods=[]
nest=Nest(0,0)
food_spawn_timer=0
vitamin=0
running=True

#Combat Stage
mantis=Enemy(1000,400,'mantis')
bosses=[mantis]
soldiers=[SoldierAnt(0,0,'black')]
ant_spawn_timer=6

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



    #LOGIC HANDLING
    if stage=='collecting':
        player.move_towards(dt)
        food_spawn_timer-=dt
        if food_spawn_timer<0:
            food_spawn_timer=15
            foods.append(Food(random.randint(0,1500),random.randint(0,850),(random.randint(0,255),random.randint(0,255),0))) 

        
        player.update()
        for food in foods:
            food.update()
            if player.rect.colliderect(food.rect) and player.carrying==None:
                food.count-=1
                player.carrying=food
                if food.count==0:
                    foods.remove(food)
        if player.rect.colliderect(nest.rect) and player.carrying:
            player.carrying=None
            vitamin+=1
    if stage=='combat':
        ant_spawn_timer-=dt
        if ant_spawn_timer<0:
            ant_spawn_timer=8
            soldiers.append(SoldierAnt(0,0,'black'))
        mantis.move_towards(dt)
        for soldier in soldiers:
            soldier.move_towards(dt)
        mantis.update()
        for soldier in soldiers:
            soldier.target_x=mantis.x
            soldier.target_y=mantis.y
            soldier.update()
            if mantis.rect.colliderect(soldier.rect):
                soldier.attack_timer+=dt
                if soldier.attack_timer>=soldier.attack_speed:
                    mantis.hp-=soldier.dmg
                    if mantis.hp<=0:
                        bosses.remove(mantis)
                    soldier.attack_timer=0

        mantis.update()
        nearest_soldier=None
        for soldier in soldiers:
            if nearest_soldier==None:
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
        screen.fill((255, 255, 255))
        nest.draw(screen)
        for food in foods:
            food.draw(screen)
        player.draw(screen)
        if player.carrying!=None:
            pygame.draw.rect(screen,player.carrying.color,(player.x,player.y-25,50,50))
        draw_text(str(vitamin),basic_font,(0,0,0),1000,0)
        if player.is_moving==True:
            player.animation_timer+=dt
            if player.animation_timer>player.animation_speed:
                player.animation_timer=0
                player.frame_index+=1
                player.img=player.images[player.frame_index%len(player.images)]
    if stage=='combat':
        screen.fill((255, 255, 255))
        for boss in bosses:
            boss.draw(screen)
        for soldier in soldiers:
            soldier.draw(screen)
        draw_text('Mantis_HP:'+(str(mantis.hp)),basic_font,(0,0,0),1000,0)

    pygame.display.update()


pygame.quit()
