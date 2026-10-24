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
        self.img=pygame.image.load(self.img).convert_alpha()
        self.img=pygame.transform.scale(self.img,(75,50))
        self.rect=pygame.Rect(x,y,75,50)
    def draw(self,screen):
        screen.blit(self.img, (self.x, self.y))
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
    def __init__(self,x,y):
        self.x=x
        self.y=y

player=WorkerAnt(0,400)
foods=[]
nest=Nest(0,0)
food_spawn_timer=0
vitamin=0
running=True




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





    #RENDER HANDLING
    screen.fill((255, 255, 255))
    nest.draw(screen)
    for food in foods:
        food.draw(screen)
    player.draw(screen)
    if player.carrying!=None:
        pygame.draw.rect(screen,player.carrying.color,(player.x,player.y-25,50,50))
    draw_text(str(vitamin),basic_font,(0,0,0),1000,0)
    pygame.display.update()

pygame.quit()
