import pygame
import random
import math
import os
import sys

os.environ['SDL_VIDEO_CENTERED'] = '1' 
def get_resource_path(relative_path):
    try:
        base_path=sys._MEIPASS
    except Exception:
        base_path=os.path.abspath(".")
    return os.path.join(base_path, relative_path)


pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((1500, 850))
is_fullscreen=False
pygame.display.set_caption("Ant Colony")
stage='start'
clock=pygame.time.Clock()
cursor_img=pygame.image.load(get_resource_path('assets/worker-ant/pixil-frame-0.png')).convert_alpha()
cursor_img=pygame.transform.rotate(pygame.transform.scale(cursor_img,(19,24)),45)
button_font=pygame.font.Font(get_resource_path('assets/font.ttf'), 40)
ui_font=pygame.font.Font(get_resource_path('assets/font.ttf'), 70)
hatch_font=pygame.font.Font(get_resource_path('assets/font.ttf'), 20)
text_font=pygame.font.Font(get_resource_path('assets/font.ttf'), 15)
logo=pygame.image.load(get_resource_path('assets/logo.png')).convert_alpha()
logo=pygame.transform.scale(logo,(45*20,23*20))
white_logo=pygame.image.load(get_resource_path('assets/white_logo.png')).convert_alpha()
white_logo=pygame.transform.scale(white_logo,(18*30,10*30))

start=pygame.image.load(get_resource_path('assets/title-bg.png')).convert()
start=pygame.transform.scale(start,(1500,850))
farmground=pygame.image.load(get_resource_path('assets/farmground.png')).convert()
battleground=pygame.image.load(get_resource_path('assets/battleground.png')).convert()
nest_background=pygame.image.load(get_resource_path('assets/nest.png')).convert()
farmground=pygame.transform.scale(farmground,(1500,850))
battleground=pygame.transform.scale(battleground,(1500,850))
nest_background=pygame.transform.scale(nest_background,(1500,850))
food_icon=pygame.image.load(get_resource_path('assets/food/food-icon.png')).convert_alpha()
food_icon=pygame.transform.scale(food_icon,(100,100))
stamina_icon=pygame.image.load(get_resource_path('assets/stamina-icon.png')).convert_alpha()
stamina_icon=pygame.transform.scale(stamina_icon,(100,100))

active_dialogue_index=0
active_chat_index=0



#Collect
leaf_icon=pygame.transform.scale(pygame.image.load(get_resource_path('assets/icons/leaf.png')).convert_alpha(),(75,75))
wheat_icon=pygame.transform.scale(pygame.image.load(get_resource_path('assets/icons/wheat.png')).convert_alpha(),(75,75))
apple_seed_icon=pygame.transform.scale(pygame.image.load(get_resource_path('assets/icons/seed.png')).convert_alpha(),(75,75))
salt_icon=pygame.transform.scale(pygame.image.load(get_resource_path('assets/icons/salt.png')).convert_alpha(),(75,75))
honey_icon=pygame.transform.scale(pygame.image.load(get_resource_path('assets/icons/honey.png')).convert_alpha(),(75,75))
blood_icon=pygame.transform.scale(pygame.image.load(get_resource_path('assets/icons/blood.png')).convert_alpha(),(75,75))

#Combat
black_icon=pygame.transform.rotate(pygame.transform.scale(pygame.image.load(get_resource_path('assets/icons/black.png')).convert_alpha(),(75,120)),-90)
leafcutter_icon=pygame.transform.rotate(pygame.transform.scale(pygame.image.load(get_resource_path('assets/icons/leafcutter.png')).convert_alpha(),(75,120)),-90)
wood_icon=pygame.transform.rotate(pygame.transform.scale(pygame.image.load(get_resource_path('assets/icons/wood.png')).convert_alpha(),(75,120)),-90)
fire_icon=pygame.transform.rotate(pygame.transform.scale(pygame.image.load(get_resource_path('assets/icons/fire.png')).convert_alpha(),(75,120)),-90)
dracula_icon=pygame.transform.rotate(pygame.transform.scale(pygame.image.load(get_resource_path('assets/icons/dracula.png')).convert_alpha(),(75,120)),-90)

#Storage
blood=0
wheat=0
apple_seed=0
salt=0
honey=0
leaf=0
hp_buff=0
power_buff=0
black_screen=pygame.Surface((1500,850),pygame.SRCALPHA)
darkness=0

def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))
green=(0,255,0)
red=(255,0,0)
grey=(127,127,127)
black=(0,0,0)



class TutorialAnt:
    def __init__(self,x,y):
        self.x=x
        self.y=y
        images_path=get_resource_path('assets/friendly-ant')
        self.imgs=[pygame.transform.flip(pygame.transform.scale(pygame.image.load(f"{images_path}/{f}").convert_alpha(), (27*6,27*6)),True,False) for f in os.listdir(images_path) if f.endswith(".png")]
        self.animation_speed=0.1
        self.animation_timer=0
        self.frame_index=0
        self.img=self.imgs[self.frame_index]
    def update(self,dt):
        if self.imgs:
            self.animation_timer+=dt
            if self.animation_timer>=self.animation_speed:
                self.animation_timer=0
                self.frame_index=(self.frame_index+1)%len(self.imgs)
                self.img=self.imgs[self.frame_index]
    def draw(self,screen):
        if self.img:
            screen.blit(self.img, (self.x, self.y))

class TutorialManager:
    def __init__(self):
        self.steps=[
            {'text':'Welcome to Tiny Colony! I am your guide!\n Click the box to hide this, or click anywhere to continue.',
             'target':'None',
             'condition':lambda:True,
             'completed':False,
             'is_intro':True   
            },
            {'text':'Our ant colony is hungry.\nThe first thing we diligent ants do in the morning is collecting foods.\n Click the Collect button.',
             'target':'collect_button',
             'condition':lambda:stage=='collecting',
             'completed':False
            },
            {'text':"Good! Now click on a piece of food on the ground to move your ant toward there.",
             'target':None,
             'condition':lambda:any (w.carrying for w in workers),
             'completed':False
            },
            {'text':"Now move your ant back to the nest. Worker ants can only carry one piece of food",
             'target':'nest',
             'condition':lambda:calories>0,
             'completed':False
            },
            {"text":"You gathered your first piece! Now keep collecting food until your stamina runs out.",
             'target':None,
             'condition':lambda:collected==True,
             'completed':False},
            {"text":"You can see the extra materials you collected here.\nEach type of food has a small chance to drop its special material.\nClick the Return button to go back to your nest.",
             'target':"return_button",
             'condition':lambda:stage=='nest',
             'completed':False},
            {"text":"Everyday you can only collect once.\n So we need more worker ants to collect more food for the colony.\n Click the Hatch button to hatch more ants.",
             'target':'hatch_button',
             'condition':lambda:hatching==True,
             'completed':False},
            {"text":"One worker ant is not enough to gather food for the entire colony.\n Let's recruit one more. It takes 5 food.\n Click the Worker Ant button to recruit a worker ant.",
            "target":"worker_button",
            "condition":lambda:len(workers)==2,
            "completed":False},
            {"text":"You can only collect food once a day. Our ants need to rest to work again.\n Click the Sleep button, this will skip a day.",
            "target":None,
            "condition":lambda:day==2,
            "completed":False},
            {"text":"Now keep collecting food everyday and grow your colony.\n Make sure to get your army ready before day 7.\n Our scout reported that a threat is approaching.",
             "target":None,
             "condition":lambda:stage=='collecting',
             "completed":False}]
        self.current_step=0
        self.is_waiting_to_advance=False
        self.pulse_timer=0
        self.is_hidden=False
        self.displayed_text=''
        self.char_index=0
        self.typing_speed=100
        self.typing_timer=0
        self.finished_talking=True
    def get_current_step(self):
        return self.steps[self.current_step]
    def check_progress(self):
        if self.char_index ==0 or self.displayed_text=='':
            self.displayed_text =''
            self.char_index=0
        step=self.get_current_step()

        if self.is_hidden and step["condition"]():
            self.is_hidden=False
        if step["condition"]() and not self.is_waiting_to_advance and not step.get("is_intro",False):
            self.is_waiting_to_advance=True
            if self.current_step<len(self.steps)-1:
                step["text"]="Great job! Click the anywhere to continue."
            else:
                step["text"]="That's the end of the tutorial. Now manage the colony to survive the weeks"
    def advance(self):
        if self.is_waiting_to_advance or self.get_current_step().get('is_intro'):
            self.current_step+=1
            self.is_waiting_to_advance=False
            self.char_index=0
            if self.current_step>=len(self.steps):
                return False
        return True
    def draw(self,screen):
        if self.is_hidden:
            return
        
        step=self.get_current_step()
        rect=(250,675,1200,150)
        pygame.draw.rect(screen,(255,255,255),rect)

        full_text = step['text']
        if self.char_index < len(full_text):
            self.finished_talking=False
            self.typing_timer += dt
            chars_to_add = int(self.typing_timer * self.typing_speed)
            if chars_to_add > 0:
                self.char_index = min(self.char_index + chars_to_add, len(full_text))
                self.typing_timer = 0
            self.displayed_text = full_text[:self.char_index]
        else:
            self.displayed_text = full_text
            self.finished_talking=True

        paragraphs=self.displayed_text.split('\n')
        lines=[]
        for paragraph in paragraphs:
            
            words=paragraph.split(' ')
            current_line=""
            for word in words:
                test_line=current_line+word+" "
                if text_font.size(test_line)[0]<1300:
                    current_line=test_line
                else:
                    lines.append(current_line)
                    current_line=word+" "
            lines.append(current_line)

        if not self.is_waiting_to_advance:
            draw_text('Click box to hide',hatch_font,(150,150,150),rect[0]+20,rect[1]+120)

        for i,line in enumerate(lines):
            draw_text(line,hatch_font,(0,0,0),rect[0]+20,rect[1]+20+i*30)

        if step["target"] and not self.is_waiting_to_advance:
            self.pulse_timer+=0.1
            pulse=int(10+5*math.sin(self.pulse_timer))

            target_rect=None
            if step['target']=='collect_button':
                for button in buttons:
                    if button.function=='collection':target_rect=button.rect
            elif step['target']=='nest':
                target_rect=nest.rect
            elif step['target']=='return_button':
                target_rect=return_button_collect.rect
            elif step['target']=='hatch_button':
                for button in buttons:
                    if button.function=='hatch':target_rect=button.rect
            elif step['target']=='worker_button':
                for button in hatch_buttons:
                    if button.type=='worker ant':target_rect=button.rect

            if target_rect:
                overlay=pygame.Surface((1500,850),pygame.SRCALPHA)
                overlay.fill((0,0,0,100))
                screen.blit(overlay,(0,0))

                pygame.draw.rect(screen,(255,0,0),target_rect.inflate(pulse*2,pulse*2),width=4)
tutorial_manager=TutorialManager()
tutorial_on=True




class Button:
    def __init__(self, x, y, function):
        self.x=x
        self.y=y
        self.function=function
        self.rect=pygame.Rect(x,y,210,100)
        self.passive=pygame.image.load(get_resource_path('assets/button.png')).convert_alpha()
        self.passive=pygame.transform.scale(self.passive,(250,100))
        self.active=pygame.image.load(get_resource_path('assets/button-active.png')).convert_alpha()
        self.active=pygame.transform.scale(self.active,(250,100))
        self.img=self.passive
    def draw(self,screen):
        if self.function!='collection':
            screen.blit(self.img, (self.x-20, self.y))
            if self.function=='hatch':
                text='Hatch'
            if self.function=='storage':
                text='Barrack'
            if self.function=='sleep':
                text='Sleep'
            text_surface= button_font.render(text, True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=self.rect.center)
            screen.blit(text_surface, text_rect)
        else:
            text='Collect'
            if not collected:
                screen.blit(self.img, (self.x-20, self.y))
                text_surface= button_font.render(text, True, (255, 255, 255))
                text_rect = text_surface.get_rect(center=self.rect.center)
                screen.blit(text_surface, text_rect)
class ReturnButton:
    def __init__(self, x, y):
        self.x=x
        self.y=y
        self.passive_img=pygame.image.load(get_resource_path('assets/return-button.png')).convert_alpha()
        self.active_img=pygame.image.load(get_resource_path('assets/return-button-active.png')).convert_alpha()
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
        if self.type in ['soldier10x','leafcutter10x','wood10x','fire10x','dracula10x']:
            self.rect=pygame.Rect(x,y,50,50)
    def draw(self,screen):
        
        pygame.draw.rect(screen,self.color,self.rect)
        pygame.draw.rect(screen,self.border_color,self.rect,width=2)
        text_surface= hatch_font.render(self.type, True, (0, 0, 0))
        if self.type in ['soldier10x','leafcutter10x','wood10x','fire10x','dracula10x']:
            text_surface= hatch_font.render('x10', True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)
class InfoButton:
    def __init__(self, x, y,type):
        self.x=x
        self.y=y
        self.type=type
        self.img=pygame.image.load(get_resource_path('assets/info-icon.png')).convert_alpha()
        self.img=pygame.transform.scale(self.img,(30,30))
        self.rect=pygame.Rect(x,y,30,30)
        if self.type=='scout':
            self.info='Increase the daily amount of food by 1'
            self.cost='Cost: 5 calories'
        if self.type=='worker':
            self.info='Increase the number of workers by 1'
            self.cost='Cost: 5 calories'
        if self.type=='soldier':
            self.info='Add a soldier of the type below to your army'
            self.cost='Cost: 3 calories + special ingredient for special ants\nLeafcutter Ant: 1 Leaf\nWood Ant: 1 Honey\nDracula Ant: 1 Blood\nFire Ant: 1 Apple Seed'
        if self.type=='wheat':
            self.info='Wheat'
            self.cost='Use 1 wheat to permanently increase Max HP of future ants by 1'
        if self.type=='salt':
            self.info='Salt'
            self.cost='Use 1 salt to permanently increase damage of future ants by 1\nHowever,decrease max HP by 1'
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
        if self.type==1:self.img=pygame.image.load(get_resource_path('assets/cocoon-1.png')).convert_alpha()
        if self.type==2:self.img=pygame.image.load(get_resource_path('assets/cocoon-2.png')).convert_alpha()
        if self.type==3:self.img=pygame.image.load(get_resource_path('assets/cocoon-3.png')).convert_alpha()
        self.img=pygame.transform.scale(self.img,(8*10,18*10))
    def draw(self,screen):
        screen.blit(self.img,(self.x,self.y))
        self.rect=pygame.Rect(self.x,self.y,8*10,18*10)
class Icon:
    def __init__(self,x,y,type,count):
        self.x=x
        self.y=y
        self.type=type
        if self.type=='leaf':self.img,self.count=pygame.image.load(get_resource_path('assets/icons/leaf.png')).convert_alpha(),count
        if self.type=='honey':self.img,self.count=pygame.image.load(get_resource_path('assets/icons/honey.png')).convert_alpha(),count
        if self.type=='seed':self.img,self.count=pygame.image.load(get_resource_path('assets/icons/seed.png')).convert_alpha(),count
        if self.type=='blood':self.img,self.count=pygame.image.load(get_resource_path('assets/icons/blood.png')).convert_alpha(),count
        if self.type=='wheat':self.img,self.count=pygame.image.load(get_resource_path('assets/icons/wheat.png')).convert_alpha(),count
        if self.type=='salt':self.img,self.count=pygame.image.load(get_resource_path('assets/icons/salt.png')).convert_alpha(),count
        self.img=pygame.transform.scale(self.img,(50,50))
        
    def draw(self,screen):
        
        self.rect=pygame.Rect(self.x,self.y,120,50)
        pygame.draw.rect(screen,(255,255,255),self.rect)
        screen.blit(self.img,(self.x,self.y))
        draw_text(str(math.ceil(self.count)),text_font,(0,0,0),self.x+60,self.y+10)
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
        images_path=get_resource_path('assets/worker-ant')
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

        if self.x<(19+10):
            self.x=19+10
        if self.y<(24+10):
            self.y=24+10
        if self.x>(1500-19-10):
            self.x=1500-19-10
        if self.y>(850-24-10):
            self.y=850-24-10
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
            images_path=get_resource_path('assets/food/bread')
            self.images=[pygame.transform.scale(pygame.image.load(f"{images_path}/{f}").convert_alpha(), (32*8, 20*8)) for f in os.listdir(images_path) if f.endswith(".png")]
            self.rect=pygame.Rect(x,y,32*8,20*8)
            self.crumb=pygame.transform.scale(pygame.image.load(get_resource_path('assets/food/breadcrumb.png')).convert_alpha(), (5*12,5*12))
        if self.type=='apple':
            images_path=get_resource_path('assets/food/apple')
            self.images=[pygame.transform.scale(pygame.image.load(f"{images_path}/{f}").convert_alpha(), (20*8, 19*8)) for f in os.listdir(images_path) if f.endswith(".png")]
            self.rect=pygame.Rect(x,y,20*8,19*8)
            self.crumb=pygame.transform.scale(pygame.image.load(get_resource_path('assets/food/apple-crumb.png')).convert_alpha(), (5*12,5*12))
        if self.type=='chips':
            images_path=get_resource_path('assets/food/chips')
            self.images=[pygame.transform.scale(pygame.image.load(f"{images_path}/{f}").convert_alpha(), (35*6, 22*6)) for f in os.listdir(images_path) if f.endswith(".png")]
            self.rect=pygame.Rect(x,y,35*6,22*6)
            self.crumb=pygame.transform.scale(pygame.image.load(get_resource_path('assets/food/chips-crumb.png')).convert_alpha(), (5*10,5*10))
        if self.type=='mosquito':
            images_path=get_resource_path('assets/food/dead-mosquito')
            self.images=[pygame.transform.scale(pygame.image.load(f"{images_path}/{f}").convert_alpha(), (59*2, 42*2)) for f in os.listdir(images_path) if f.endswith(".png")]
            self.crumb=pygame.transform.scale(pygame.image.load(get_resource_path('assets/food/dead-mosquito-crumb.png')).convert_alpha(), (5*6,5*6))
            self.rect=pygame.Rect(x,y,59*2,42*2)
        if self.type=='honeycomb':
            images_path=get_resource_path('assets/food/honeycomb')
            self.images=[pygame.transform.scale(pygame.image.load(f"{images_path}/{f}").convert_alpha(), (30*7, 31*7)) for f in os.listdir(images_path) if f.endswith(".png")]
            self.rect=pygame.Rect(x,y,30*7,31*7)
            self.crumb=pygame.transform.scale(pygame.image.load(get_resource_path('assets/food/honey-crumb.png')).convert_alpha(), (11*6,14*6))
        if self.type=='leaf':
            images_path=get_resource_path('assets/food/leaf')
            self.images=[pygame.transform.scale(pygame.image.load(f"{images_path}/{f}").convert_alpha(), (23*15, 16*15)) for f in os.listdir(images_path) if f.endswith(".png")]
            self.rect=pygame.Rect(x,y,23*10,16*10)
            self.crumb=pygame.transform.scale(pygame.image.load(get_resource_path('assets/food/leaf-crumb.png')).convert_alpha(), (5*10,5*10))
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
        self.rect=pygame.Rect(x,y,150,150)
    def draw(self,screen):
        pygame.draw.rect(screen,green,self.rect)

#Combat Stage
class SoldierAnt:
    def __init__(self,x,y,type,hpbuff,dmgbuff):
        self.x=x
        self.y=y
        self.target_x=x
        self.target_y=y
        if type=='black':walk_path,attack_path=get_resource_path('assets/black-ant-walking'),get_resource_path('assets/black-ant-attack')
        if type=='wood':walk_path,attack_path=get_resource_path('assets/wood-ant-walking'),get_resource_path('assets/wood-ant-attack')
        if type=='dracula':walk_path,attack_path=get_resource_path('assets/dracula-ant-walking'),get_resource_path('assets/dracula-ant-attack')
        if type=='fire':walk_path,attack_path=get_resource_path('assets/fire-ant-walking'),get_resource_path('assets/fire-ant-attack')
        if type=='leafcutter':walk_path,attack_path=get_resource_path('assets/leafcutter-ant-walking'),get_resource_path('assets/leafcutter-ant-attack')
        self.walks=[pygame.transform.rotate(pygame.transform.scale(pygame.image.load(f"{walk_path}/{f}").convert_alpha(), (19*2,24*2)),-90) for f in os.listdir(walk_path) if f.endswith(".png")]   
        self.attacks=[pygame.transform.rotate(pygame.transform.scale(pygame.image.load(f"{attack_path}/{f}").convert_alpha(), (19*2,24*2)),-90) for f in os.listdir(attack_path) if f.endswith(".png")]
        self.angle=0.0
        self.img=self.walks[0]
        self.animation_timer=0
        self.animation_speed=0.02
        self.frame_index=0
        self.rect=pygame.Rect(x-19,y-24,19*2,24*2)
        self.speed=200
        self.type=type
        self.is_moving=False

        self.is_attacking=False
        self.attack_animation_timer=0
        self.attack_animation_speed=0.05
        self.attack_duration=0.5
        self.attack_hit=False
        self.attack_timer=0

        self.healthbar=pygame.Rect(x-19,y-30,38,5)
        if self.type=='black':
            self.hp=10+hpbuff-dmgbuff
            self.maxhp=10+hpbuff-dmgbuff
            self.dmg=2+dmgbuff
            self.range=0
            self.attack_speed=1
        elif self.type=='wood':
            self.hp=5+hpbuff-dmgbuff
            self.maxhp=5+hpbuff-dmgbuff
            self.range=350
            self.dmg=2+dmgbuff
            self.attack_speed=3
        elif self.type=='dracula':
            self.hp=10+hpbuff-dmgbuff
            self.maxhp=10+hpbuff-dmgbuff
            self.range=0
            self.dmg=2+dmgbuff
            self.attack_speed=1
        elif self.type=='fire':
            self.hp=15+hpbuff-dmgbuff
            self.maxhp=15+hpbuff-dmgbuff
            self.range=0
            self.dmg=0+dmgbuff
            self.attack_speed=2
        elif self.type=='leafcutter':
            self.hp=15+hpbuff-dmgbuff
            self.maxhp=15+hpbuff-dmgbuff
            self.range=0
            self.dmg=2+dmgbuff
            self.attack_speed=1    
        self.rangerect=pygame.Rect(self.x-19-self.range/2,self.y-24-self.range/2,38+self.range,48+self.range)
        self.random_x=random.randint(150,1200)
        self.random_y=random.randint(300,700)
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
        frame=self.walks[self.frame_index%len(self.walks)]
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
        self.img=pygame.image.load(get_resource_path('assets/acid.png')).convert_alpha()
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
            walking_path=get_resource_path('assets/mantis-walking')
            attack1_path=get_resource_path('assets/mantis-attack-1')
            self.walks=[pygame.transform.rotate(pygame.transform.scale(pygame.image.load(f"{walking_path}/{f}").convert_alpha(), (34*10,54*10)),-90) for f in os.listdir(walking_path) if f.endswith(".png")]
            self.attacks1=[pygame.transform.rotate(pygame.transform.scale(pygame.image.load(f"{attack1_path}/{f}").convert_alpha(), (34*10,54*10)),-90) for f in os.listdir(attack1_path) if f.endswith(".png")]
            self.rect=pygame.Rect(x-34*5,y-54*5,250,200)   
            self.speed=100
            self.hp=1500
            self.maxhp=1500
            self.dmg=8
            self.range=100
            self.attack_speed=0.5
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
            walks_path=get_resource_path('assets/grasshopper-walking')
            attacks_path=get_resource_path('assets/grasshopper-attack-1')
            attacks_path2=get_resource_path('assets/grasshopper-attack-2')
            self.walks=[pygame.transform.rotate(pygame.transform.scale(pygame.image.load(f"{walks_path}/{f}").convert_alpha(), (34*10,54*10)),-90) for f in os.listdir(walks_path) if f.endswith(".png")]
            self.attacks1=[pygame.transform.rotate(pygame.transform.scale(pygame.image.load(f"{attacks_path}/{f}").convert_alpha(), (34*10,54*10)),-90) for f in os.listdir(attacks_path) if f.endswith(".png")]
            self.img=self.walks[0]
            self.rect=pygame.Rect(x-225,y-150,450,300)
            self.speed=200
            self.hp=3000
            self.maxhp=3000
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
        if self.type=='mantis':
            screen.blit(self.img, (self.x-225, self.y-150))
        else:
            screen.blit(self.img, (self.x-225, self.y-50))
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
            self.x=1500-200
        if self.type=='mantis':
            if self.y>850-500:
                self.y=850-500
        else:
            if self.y>(850-200):
                self.y=850-200
        if self.type=='mantis'or self.type=='grasshopper':
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

class Credit:
    def __init__(self,x,y,text,size):
        self.x=x
        self.y=y
        self.font=pygame.font.Font(get_resource_path('assets/font.ttf'), size)
        self.text=text
    def update(self,dt):
        self.y-=dt*150
        self.img=self.font.render(self.text, True, (255, 255, 255))
        screen.blit(self.img, (self.x, self.y))

credits=[Credit(250,1200,"YOU WIN!",200),
         Credit(450,1450,"Thanks for playing!",55),
         Credit(150,1650,"Created by:",55),
         Credit(650,1750,"Coders:",50),
         Credit(350,1850,"NNKD-Kevin",50),
         Credit(850,1850,"Philogamer",50),
         Credit(575,2050,"Main Artist:",50),
         Credit(600,2150,"VinceTran",50),
         Credit(600,2350,"Volunteer:",50),
         Credit(650,2450,"Gregory",50)
]
logo_y=950


#Nest Stage        
timeline=pygame.Rect(150,50,1200,30)
buttons=[Button(950,150,'collection'),Button(400,580,'hatch'),Button(400,280,'storage'),Button(1000,600,'sleep')]
hatch_buttons=[HatchButton(200,450,'worker ant'),HatchButton(600,450,'soldier ant'),HatchButton(1000,450,'scout ant'),HatchButton(600,515,'leafcutter ant'),HatchButton(600,580,'wood ant'),HatchButton(600,645,'fire ant'),HatchButton(600,710,'dracula ant'),
               HatchButton(875,450,'soldier10x'),HatchButton(875,515,'leafcutter10x'),HatchButton(875,580,'wood10x'),HatchButton(875,645,'fire10x'),HatchButton(875,710,'dracula10x')]
hatching=False
storaging=False
transition=False
transition_speed=100
menu_on=False
ant_price=5
menu=pygame.Rect(150,200,1200,600)
return_button_nest=ReturnButton(1220,220)
return_button_collect=ReturnButton(700,600)
return_button_combat=ReturnButton(700,600)
info_icons=[InfoButton(350,220,'worker'),InfoButton(750,220,'soldier'),InfoButton(1150,220,'scout')]
cocoons=[Cocoon(280,250,1),Cocoon(680,250,2),Cocoon(1080,250,3)]
notifications=[]
hatch_icons=[Icon(500,150,'leaf',leaf),Icon(600,150,'honey',honey),Icon(700,150,'seed',apple_seed),Icon(800,150,'blood',blood)]
barrack_icons=[Icon(500,150,'wheat',blood),Icon(600,150,'salt',blood)]
barrack_buttons=[HatchButton(400,250,'wheat'),HatchButton(700,250,'salt')]
barrack_info_icons=[InfoButton(370,220,'wheat'),InfoButton(950,220,'salt')]
tutorial_ant=TutorialAnt(50,650)
tutorial_on=True
won=False

#Collecting Stage
max_foods=2
week=1
day=0
max_stamina=3
collected=False
stamina=3
foods=[]
nest=Nest(50,50)
workers=[WorkerAnt(100,50)]
food_spawn_timer=0
calories=0
running=True
harvest=[]
dead_ants=[]
food_types=['bread','chips','leaf','honeycomb','apple','mosquito']
ant_types=['black','wood','dracula','fire','leafcutter']
ant_icons=[black_icon,leafcutter_icon,wood_icon,fire_icon,dracula_icon]
food_icons=[wheat_icon,salt_icon,leaf_icon,honey_icon,apple_seed_icon,blood_icon]
#Combat Stage
mantis=Enemy(0,0,'mantis')
grasshopper=Enemy(1000,400,'grasshopper')
bosses=[mantis]
soldiers=[SoldierAnt(1500,700,'black',0,0)]
ant_spawn_timer=0
acids=[]
choosecombat=False
burn=0
burnspeed=0.5
burn_timer=0
combat1_won=False
combat2_won=False
combat3_won=False
combat4_won=False
#Game Loop
while running:
    dt = clock.tick(60) / 1000
    #INPUT HANDLING
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_F11:
                is_fullscreen= not is_fullscreen
                if is_fullscreen:
                    screen = pygame.display.set_mode((1500, 850), pygame.FULLSCREEN|pygame.SCALED)
                else:
                    screen = pygame.display.set_mode((1500, 850))
        #Tutorial Click Handling
        if tutorial_on and event.type==pygame.MOUSEBUTTONDOWN:
            mouse_pos=pygame.mouse.get_pos()
            rect=(50,650,1400,150)
            show_rect=(1350,780,140,40)

            if tutorial_manager.is_hidden:
                if show_rect[0]<=mouse_pos[0] <= show_rect[0]+show_rect[2] and show_rect[1]<=mouse_pos[1] <= show_rect[1]+show_rect[3]:
                    tutorial_manager.is_hidden=False
                    continue
            else:
                if tutorial_manager.get_current_step().get('is_intro'):
                    tutorial_on=tutorial_manager.advance()
                    continue

                if (rect[0]<=mouse_pos[0] <= rect[0]+rect[2] and rect[1]<=mouse_pos[1] <= rect[1]+rect[3]):
                    if not tutorial_manager.is_waiting_to_advance:
                        tutorial_manager.is_hidden=True
                        continue
                if tutorial_manager.is_waiting_to_advance:
                    tutorial_on=tutorial_manager.advance()
                    continue



        keys=pygame.key.get_pressed()
        if stage=='start' or stage=='return':
            if keys[pygame.K_SPACE]:
                stage='nest'
                transition=True
                darkness=255
        
        
        mouse_pos=pygame.mouse.get_pos()          
        if stage=='collecting':
            if event.type==pygame.MOUSEBUTTONDOWN and collected==False:
                if nest.rect.collidepoint(event.pos):
                    for worker in workers:
                        worker.target_x=event.pos[0]+random.randint(-20,20)
                        worker.target_y=event.pos[1]+random.randint(-20,20)
                else:
                    n=len(workers)
                    radius=min((20*n),250)
                    for worker in workers:
                        worker.target_x=event.pos[0]+random.randint(-radius,radius)
                        worker.target_y=event.pos[1]+random.randint(-radius,radius)
            if collected:
                if keys[pygame.K_SPACE]:
                    for food in food_types:
                        harvest.append(food)
                if return_button_collect.rect.collidepoint(mouse_pos):
                    return_button_collect.img=return_button_collect.active_img
                    if event.type==pygame.MOUSEBUTTONDOWN:
                        harvest=[]
                        stage='nest'
                        transition=True
                        darkness=255
                else:
                    return_button_collect.img=return_button_collect.passive_img
        

        #Nest Stage
        if stage=='nest':
            for button in buttons:
                if button.rect.collidepoint(mouse_pos) and menu_on==False:
                    button.img=button.active
                    if event.type==pygame.MOUSEBUTTONDOWN:
                        if button.function=='collection' and collected==False:
                            stage='collecting'
                            transition=True
                            darkness=255
                            for i in range(max_foods):
                                foods.append(Food(random.randint(400,1300),random.randint(200,750),random.randint(0,100)))
                            for worker in workers:
                                worker.carrying=None
                        if button.function=='sleep':
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
                    button.img=button.passive
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
                                if button.type=='soldier ant' and calories>=3:
                                    calories-=3
                                    soldiers.append(SoldierAnt(1500,850,'black',wheat,salt))
                                if button.type=='leafcutter ant' and calories>=3 and leaf>0:
                                    calories-=3
                                    leaf-=1
                                    soldiers.append(SoldierAnt(1500,850,'leafcutter',wheat,salt))
                                if button.type=='wood ant' and calories>=3 and honey>0:
                                    calories-=3
                                    honey-=1
                                    soldiers.append(SoldierAnt(1500,850,'wood',wheat,salt))
                                if button.type=='fire ant' and calories>=3 and apple_seed>0:
                                    calories-=3
                                    apple_seed-=1
                                    soldiers.append(SoldierAnt(1500,850,'fire',wheat,salt))
                                if button.type=='dracula ant' and calories>=3 and blood>0:
                                    blood-=1
                                    calories-=3
                                    soldiers.append(SoldierAnt(1500,850,'dracula',wheat,salt))
                                if button.type=='soldier10x' and calories>=30:
                                    calories-=30
                                    for i in range(10):
                                        soldiers.append(SoldierAnt(1500,850,'black',wheat,salt))
                                if button.type=='leafcutter10x' and calories>=30 and leaf>=10:
                                    calories-=30
                                    for i in range(10):
                                        leaf-=1
                                        soldiers.append(SoldierAnt(1500,850,'leafcutter',wheat,salt))
                                if button.type=='wood10x' and calories>=30 and honey>=10:
                                    calories-=30
                                    for i in range(10):
                                        honey-=1
                                        soldiers.append(SoldierAnt(1500,850,'wood',wheat,salt))
                                if button.type=='fire10x' and calories>=30 and apple_seed>=10:
                                    calories-=30
                                    for i in range(10):
                                        apple_seed-=1
                                        soldiers.append(SoldierAnt(1500,850,'fire',wheat,salt))
                                if button.type=='dracula10x' and calories>=30 and blood>=10:
                                    calories-=30
                                    for i in range(10):
                                        blood-=1
                                        soldiers.append(SoldierAnt(1500,850,'dracula',wheat,salt))
                            
                        else:
                            button.color=button.passive_color
                            button.border_color=(0,0,0)
                    for icon in info_icons:
                        if icon.rect.collidepoint(mouse_pos):
                            icon.hovered=True
                        else:
                            icon.hovered=False
                if storaging:
                    for button in barrack_buttons:
                        if button.rect.collidepoint(mouse_pos):
                            button.border_color=(255,255,255)
                            button.color=button.active_color
                            if event.type==pygame.MOUSEBUTTONDOWN:
                                if button.type=='wheat' and wheat>0:
                                    wheat-=1
                                    hp_buff+=1
                                if button.type=='salt' and salt>0:
                                    salt-=1
                                    power_buff+=1
                        else:
                            button.border_color=(0,0,0)
                            button.color=button.passive_color
                    for icon in barrack_info_icons:
                        if icon.rect.collidepoint(mouse_pos):
                            icon.hovered=True
                        else:
                            icon.hovered=False
        mouse_pos=pygame.mouse.get_pos()
        if stage=='combat' and len(bosses)==0:
            if return_button_combat.rect.collidepoint(mouse_pos):
                return_button_combat.img=return_button_combat.active_img
                if event.type==pygame.MOUSEBUTTONDOWN:
                    stage='nest'
            else:
                return_button_combat.img=return_button_combat.passive_img

                    


    #LOGIC HANDLING
    if tutorial_on:
        tutorial_manager.check_progress()
        if not tutorial_manager.finished_talking and not tutorial_manager.is_hidden:
            tutorial_ant.update(dt)

    if stage=='nest':
        pass
        if day==6 and not combat1_won:
            choosecombat=True
            stage='combat'
            for soldier in soldiers:
                soldier.x=random.randint(100,1400)
                soldier.y=1500
            bosses.append(mantis)
            bosses[0].x,bosses[0].y=500,0
            dead_ants=[]
        elif day==8 and not combat2_won:
            choosecombat=True
            bosses.append(grasshopper)
            stage='combat'
            for soldier in soldiers:
                soldier.x=random.randint(100,1400)
                soldier.y=1500
            bosses[0].x,bosses[0].y=500,0
            dead_ants=[]
        elif day==10 and not combat3_won:
            choosecombat=True
            stage='combat'
            for soldier in soldiers:
                soldier.x=random.randint(100,1400)
                soldier.y=1500
            bosses.append(mantis)
            mantis.maxhp=5000
            mantis.hp=5000
            mantis.dmg=12
            mantis.attack_speed=0.1
            mantis.attack_duration=0.4
            bosses[0].x,bosses[0].y=500,0
            dead_ants=[]
        elif day==13 and not combat4_won:
            choosecombat=True
            stage='combat'
            for soldier in soldiers:
                soldier.x=random.randint(100,1400)
                soldier.y=1500
            bosses.append(grasshopper)
            grasshopper.maxhp=12000
            grasshopper.hp=12000
            grasshopper.dmg=5
            bosses[0].x,bosses[0].y=500,0
            dead_ants=[]




    if stage=='collecting':
        for worker in workers:
            worker.move_towards(dt)
            worker.update()
            for food in foods:
                food.update()
                if worker.rect.colliderect(food.rect) and worker.carrying == None:
                    if food.count < 5:
                        food.count += 1
                        food.img = food.images[food.count]
                        worker.carrying = food
                    elif food.count>=4:
                        if food in foods:
                            foods.remove(food)
                
            if worker.rect.colliderect(nest.rect) and worker.carrying:
                calories+=2
                if worker.carrying=='chips':calories+=1
                stamina-=1/len(workers)
                gacha=random.randint(1,10)
                if gacha in [8,9,10]:
                    if worker.carrying.type=='mosquito': blood+=1
                    if worker.carrying.type=='bread':wheat+=1
                    if worker.carrying.type=='apple':apple_seed+=1
                    if worker.carrying.type=='chips':salt+=1
                    if worker.carrying.type=='honeycomb':honey+=1
                    if worker.carrying.type=='leaf':leaf+=1
                    harvest.append(worker.carrying.type)
                worker.carrying=None

                if stamina<=0 or len(foods)<=0:
                    for worker in workers:
                        if worker.carrying:
                            calories+=2
                            if worker.carrying=='chips':calories+=1
                            worker.carrying=None
                            gacha=random.randint(1,10)
                            if gacha in [8,9,10]:
                                if worker.carrying!=None:
                                    if worker.carrying.type=='mosquito': blood+=1
                                    if worker.carrying.type=='bread':wheat+=1
                                    if worker.carrying.type=='apple':apple_seed+=1
                                    if worker.carrying.type=='chips':salt+=1
                                    if worker.carrying.type=='honeycomb':honey+=1
                                    if worker.carrying.type=='leaf':leaf+=1
                                    harvest.append(worker.carrying.type)
                                    worker.carrying=None
                    
                    collected=True
                    foods=[]

    #COMBAT LOGIC
    if stage=='combat':
        if choosecombat:
            if stage=='combat':
                if len(bosses)>1:
                    bosses.pop(0)
            skill=False
            choosecombat=False
        if bosses:
            ant_spawn_timer-=dt
            if ant_spawn_timer<0:
                ant_spawn_timer=1
                soldiers.append(SoldierAnt(1500,850,'black',0,0))
                soldiers.append(SoldierAnt(1500,850,'wood',0,0))
                soldiers.append(SoldierAnt(1500,850,'dracula',0,0))
                soldiers.append(SoldierAnt(1500,850,'fire',0,0))
                soldiers.append(SoldierAnt(1500,850,'leafcutter',0,0))
            if not bosses[0].is_attacking and not skill:
                bosses[0].move_towards(dt)
            elif not skill:
                bosses[0].is_moving=False
            for soldier in soldiers:
                if not soldier.rangerect.colliderect(bosses[0].rect):
                    soldier.target_x=bosses[0].x+random.uniform(-255,255)+soldier.range
                    soldier.target_y=bosses[0].y+random.uniform(-150,150)+soldier.range
                #Attack
                if soldier.is_attacking and not skill:
                    soldier.is_moving=False
                    soldier.attack_animation_timer+=dt
                    #Deal damage
                    if not soldier.attack_hit and soldier.attack_animation_timer>=soldier.attack_animation_speed:
                        soldier.attack_hit=True
                        if soldier.type=='wood':
                            dy=bosses[0].y-soldier.y
                            dx=bosses[0].x-soldier.x
                            acids.append(Acid(soldier.x,soldier.y,math.degrees(math.atan2(dy,dx)),soldier.dmg))
                        else:
                            if soldier.type=='fire':
                                if burn<500:
                                    burn+=1
                            bosses[0].hp-=soldier.dmg
                            if soldier.type=='dracula':
                                if soldier.hp<soldier.maxhp:
                                    if soldier.hp+soldier.dmg/2>soldier.maxhp:
                                        soldier.hp=soldier.maxhp
                                    else:
                                        soldier.hp+=soldier.dmg/2
                    if soldier.attack_animation_timer>=soldier.attack_duration:
                        soldier.is_attacking=False
                        soldier.attack_animation_timer=0
                        soldier.frame_index=0
                else:
                    if not soldier.is_attacking:
                        soldier.move_towards(dt)
                    soldier.attack_timer+=dt

                    if bosses and soldier.attack_timer>=soldier.attack_speed and soldier.rect.colliderect(bosses[0].rect):
                        soldier.is_attacking=True
                        soldier.attack_hit=False
                        soldier.attack_timer=0

                soldier.update()
            bosses[0].update()

        if burn>0:
            burn_timer+=dt
            if burn_timer>=burnspeed and bosses:
                bosses[0].hp-=1
                burn_timer=0
                                       
        if bosses and bosses[0].hp<=0:
            try:
                bosses.remove(bosses[0])
            except ValueError:
                pass
            if stage=='combat':
                if day==6:combat1_won=True
                elif day==8:combat2_won=True
                elif day==10:combat3_won=True
                elif day==13:combat4_won=True
                for s in soldiers[:]:
                    s.hp=s.maxhp
                if day==13:
                    stage='ending'         
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
                    dead_ants.append(s.type)
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
                            dead_ants.append(target.type)
                            soldiers.remove(target)
                if boss.attack_animation_timer>=boss.attack_duration:
                    boss.is_attacking=False
                    boss.attack_timer=boss.attack_speed
                    boss.frame_index=0                                  #Reset back to walking after hitting
                    boss.attack_target=None
                    boss.skill_activate+=1
                    if boss.skill_activate>=boss.skill_duration:
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
                    dead_ants.append(s.type)
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
                                s.hp-=boss.dmg
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
                                s.hp-=boss.dmg
                    if boss.x==boss.target_x and boss.y==boss.target_y:
                        skill=False
        if len(soldiers)==0:
            stage='return'

                                           
                    
                



    #RENDER HANDLING
    if stage=='start':
        time_ms=pygame.time.get_ticks()
        screen.blit(start,(0,0))
        screen.blit(logo,(750-45*10,500-23*20))
        dynamic_font=pygame.font.Font(get_resource_path('assets/font.ttf'),50+int(math.sin(time_ms*0.002)*4))
        text_surf=dynamic_font.render("Press Space to start",True,(255,255,0))
        text_surf1=pygame.transform.rotate(text_surf,10)
        text_rect=text_surf1.get_rect(center=(950, 600))
        screen.blit(text_surf1,text_rect)
        
    if stage=='return':
        time_ms=pygame.time.get_ticks()
        screen.blit(start,(0,0))
        dynamic_font=pygame.font.Font(get_resource_path('assets/font.ttf'),30+int(math.sin(time_ms*0.002)*4))
        text_surf=dynamic_font.render("Press Space to replay",True,(255,0,0))
        text_surf1=pygame.transform.rotate(text_surf,10)
        text_rect=text_surf1.get_rect(center=(750, 500))
        screen.blit(text_surf1,text_rect)
        #Storage
        blood=0
        wheat=0
        apple_seed=0
        salt=0
        honey=0
        leaf=0
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
        hatch_icons=[Icon(500,150,'leaf',leaf),Icon(600,150,'honey',honey),Icon(700,150,'seed',apple_seed),Icon(800,150,'blood',blood)]
        barrack_icons=[Icon(500,150,'wheat',blood),Icon(600,150,'salt',blood)]
        barrack_info_icons=[InfoButton(350,220,'wheat'),InfoButton(750,220,'salt')]
        combat1_won=False
        combat2_won=False
        combat3_won=False
        combat4_won=False



        #Collecting Stage
        max_foods=2
        week=1
        day=0
        max_stamina=3
        collected=False
        stamina=3
        foods=[]
        nest=Nest(100,50)
        workers=[WorkerAnt(100,50)]
        food_spawn_timer=0
        calories=0
        running=True
        hp_buff=0
        power_buff=0
        #Combat Stage
        mantis=Enemy(0,0,'mantis')
        grasshopper=Enemy(1000,400,'grasshopper')
        bosses=[mantis]
        soldiers=[SoldierAnt(100,50,'black',0,0)]
        ant_spawn_timer=0
        acids=[]
        choosecombat=False
        burn=0
        burnspeed=0.5
        burn_timer=0
    if stage=='nest':
        screen.blit(nest_background,(0,0))
        pygame.draw.rect(screen,(255,200,0),timeline)
        for i in range(0,1201,200):
            if i ==1200 and week==1:
                pygame.draw.rect(screen,(255,0,0),(pygame.Rect(150+i,50,50,50)))
            elif (i ==1200 or i==200 or i==600) and day>6:
                pygame.draw.rect(screen,(255,0,0),(pygame.Rect(150+i,50,50,50)))
            else:
                pygame.draw.rect(screen,(255,255,0),(pygame.Rect(150+i,50,50,50)))    
        pygame.draw.rect(screen,(0,255,0),(pygame.Rect(150+day%7*200,50,50,50)))
        draw_text(f'Day {day+1}',button_font,(0,0,0),150,5)
        for button in buttons:
            button.draw(screen)
        pygame.draw.rect(screen,(240,219,211),(50,120,280,120))
        pygame.draw.rect(screen,(0,0,0),(50,120,280,120),width=5)
        screen.blit(food_icon,(60,130))
        draw_text(str(calories),ui_font,(0,0,0),170,130)
        draw_text("Click F11 to toggle fullscreen",text_font,(0,0,0),1100,10)
        screen.blit(black_screen,(0,0))
        if menu_on:
            pygame.draw.rect(screen,(235,219,200),menu)
            pygame.draw.rect(screen,(0,0,0),menu,width=3)
            return_button_nest.draw(screen)
            pygame.draw.rect(screen,(240,219,211),(50,120,280,120))
            pygame.draw.rect(screen,(0,0,0),(50,120,280,120),width=5)
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
                        if icon.type=='soldier':h+=50
                        info_rect=pygame.Rect(x,y-150,w,h)
                        pygame.draw.rect(screen,(255,200,200),info_rect)
                        draw_text(icon.info,text_font,(0,0,0),x+10,y-130)
                        draw_text(icon.cost,text_font,(0,0,0),x+10,y-110)
                for icon in hatch_icons:
                    icon.update(leaf,honey,apple_seed,blood,wheat,salt)
                    icon.draw(screen)
                draw_text(f"Number of workers: {len(workers)}",text_font,(0,0,0),250,750)
                draw_text(f"Number of foods: {max_foods}",text_font,(0,0,0),1025,750)
            if storaging:
                for icon in barrack_icons:
                    icon.update(leaf,honey,apple_seed,blood,wheat,salt)
                    icon.draw(screen)
                for soldier in soldiers:
                    screen.blit(soldier.img,(soldier.random_x,soldier.random_y))
                for button in barrack_buttons:
                    button.draw(screen)
                for info in barrack_info_icons:
                    info.draw(screen)
                    if info.hovered:
                        x,y=info.x,info.y-30
                        w,h=250,100
                        if info.type=='salt':
                            x-=200
                            w+=400
                        if info.type=='wheat':
                            w+=420
                        info_rect=pygame.Rect(x,y-150,w,h)
                        pygame.draw.rect(screen,(255,200,200),info_rect)
                        draw_text(info.info,text_font,(0,0,0),x+10,y-130)
                        draw_text(info.cost,text_font,(0,0,0),x+10,y-110)

            screen.blit(food_icon,(60,130))
            draw_text(str(calories),ui_font,(0,0,0),170,130)
        mouse_x,mouse_y=pygame.mouse.get_pos()
        screen.blit(cursor_img,(mouse_x,mouse_y))


    if stage=='collecting':
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
        pygame.draw.rect(screen,(240,219,211),(950,20,520,120))
        pygame.draw.rect(screen,(0,0,0),(950,20,520,120),width=5)
        screen.blit(stamina_icon,(1260,30))
        draw_text(str(math.ceil(stamina)),ui_font,(0,0,0),1370,30)
        screen.blit(food_icon,(960,30))
        draw_text(str(calories),ui_font,(0,0,0),1070,30)
        draw_text('Click H to return if stuck',text_font,(0,0,0),1250,150)
        if collected:
            pygame.draw.rect(screen,(99,53,42),(300,200,900,550))
            draw_text('Collecting Complete',button_font,(255,255,255),500,250)
            return_button_collect.draw(screen)
            draw_text('Harvest:',hatch_font,(255,255,255),400,325)
            n=0
            for i in range(6):
                if food_types[i] in harvest:
                    screen.blit(food_icons[i],(475,350+n*45))
                    draw_text(f'+{harvest.count(food_types[i])}',button_font,(255,255,255),415,350+n*45)
                    n+=1



        screen.blit(black_screen,(0,0))


    if stage=='combat':
        
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
            pygame.draw.rect(screen,(255,0,0),boss.rect,2)
            boss.hbupdate()
            boss.hb()
        for soldier in soldiers:
            walks=getattr(soldier,'walks',[])
            attacks=getattr(soldier,'attacks',[])
            if soldier.is_attacking and attacks:
                progress=soldier.attack_animation_timer/soldier.attack_duration   #Soldier attack animation
                index=min(int(progress*len(attacks)),len(attacks)-1)
                soldier.img=pygame.transform.rotate(attacks[index], -soldier.angle)
            elif walks:
                if soldier.is_moving:
                    soldier.animation_timer+=dt
                    if soldier.animation_timer>soldier.animation_speed:
                        soldier.animation_timer=0
                        soldier.frame_index+=1
                        soldier.img=pygame.transform.rotate(soldier.walks[soldier.frame_index%len(soldier.walks)], -soldier.angle)
            soldier.draw(screen)
            soldier.hbupdate()
            soldier.hb()
            soldier.updaterange()
        for acid in acids:
            acid.draw(screen)
            acid.update()
            acid.move(dt)
        draw_text('Click H to return if stuck',text_font,(0,0,0),1250,150)
        if stage=='combat' and ((combat1_won and day==6) or (combat2_won and day==8) or (combat3_won and day==10)):
            pygame.draw.rect(screen,(99,53,42),(300,200,900,550))
            draw_text('Combat Complete',button_font,(255,255,255),500,250)
            return_button_combat.draw(screen)
            n=0
            draw_text('Casualties:',hatch_font,(255,255,255),400,325)
            for i in range(5):
                if ant_types[i] in dead_ants:
                    screen.blit(ant_icons[i],(475,350+n*75))
                    draw_text(f'-{dead_ants.count(ant_types[i])}',button_font,(255,255,255),415,350+n*75)
                    n+=1

        
    if stage=='ending':
        screen.fill((0,0,0))
        logo_y-=dt*150
        screen.blit(white_logo,(500,logo_y))
        for credit in credits:
            credit.update(dt)

    
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
    if tutorial_on and stage!='start':
        tutorial_manager.draw(screen)
        if day<3:
            tutorial_ant.draw(screen)
    if 0<mouse_pos[0]<1500 and 0<mouse_pos[1]<850:
        pygame.mouse.set_visible(False)
    if 10<mouse_pos[0]<1490 and 10<mouse_pos[1]<840:
        screen.blit(cursor_img,mouse_pos)
    else:
        pygame.mouse.set_visible(True)



        
    pygame.display.update()


pygame.quit()
