import pygame
import random
import math
import os
import sys
pygame.mixer.init()

os.environ['SDL_VIDEO_CENTERED'] = '1' 
def get_resource_path(relative_path):
    try:
        base_path=sys._MEIPASS
    except Exception:
        base_path=os.path.abspath(".")
    return os.path.join(base_path, relative_path)

#Sounds
button_click=pygame.mixer.Sound(get_resource_path('assets/sound/button.wav'))

#Music
ambient_music_path=get_resource_path('assets/sound/ambient_background.wav')
combat_music_path=get_resource_path('assets/sound/combat_music.wav')

current_music=''

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((1500, 850))
is_fullscreen=False
pygame.display.set_caption("Tiny Colony")
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
ant_moving_timer=0


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

class Card:
    def __init__(self,x,y,gacha):
        self.x=x
        self.y=y
        self.gacha=gacha
        if self.gacha<65:
            self.index=random.randint(0,3)
        elif 65<=self.gacha<91:
            self.index=random.randint(4,7)
        else:
            self.index=random.randint(8,12)
        self.types=[{'rarity':'common','buff':'leaf','name':'Greener Leaves'},
                    {'rarity':'common','buff':'apple_seed','name':'Sweet Apple'},
                    {'rarity':'common','buff':'honey','name':'Premium Honey'},
                    {'rarity':'common','buff':'blood','name':'Fresh Blood'},
                    {'rarity':'uncommon','buff':'wheat','name':'Whole Grain'},
                    {'rarity':'uncommon','buff':'salt','name':'Sea Salt'},
                    {'rarity':'uncommon','buff':'wealth','name':'Wealth Bless'},
                    {'rarity':'uncommon','buff':'labour','name':'Labour Bless'},
                    {'rarity':'rare','buff':'wood','name':'Acidic Longevity'},
                    {'rarity':'rare','buff':'fire','name':'Painful Bites'},
                    {'rarity':'rare','buff':'leafcutter','name':'Tough Shell'},
                    {'rarity':'rare','buff':'dracula','name':'Bloodlust'},
                    {'rarity':'rare','buff':'black','name':'Strength In Numbers'}
        ]
        self.rect=pygame.Rect(x,y,300,450)
        if self.types[self.index]['rarity']=='common':
            self.active_color=(135,119,100)
            self.passive_color=(235,219,200)
        elif self.types[self.index]['rarity']=='uncommon':
            self.active_color=(100,155,100)
            self.passive_color=(200,255,200)
        else:
            self.active_color=(75,75,155)
            self.passive_color=(175,175,255)
        self.toggled=False
    def draw(self,screen):
        if self.toggled:
            pygame.draw.rect(screen,self.active_color,self.rect)
            draw_text(self.types[self.index]['name'],hatch_font,(255,255,255),self.x+10,self.y+10)
        else:
            pygame.draw.rect(screen,self.passive_color,self.rect)
            draw_text(self.types[self.index]['name'],hatch_font,(0,0,0),self.x+10,self.y+10)
choosing_cards=[]
cards=[]
wheat_buff=0
apple_seed_buff=0
salt_buff=0
honey_buff=0
leaf_buff=0
blood_buff=0


class SoundMenu:
    def __init__(self):
        self.toggled=False
        self.rect=pygame.Rect(300,200,900,450)
        self.slider_rect=pygame.Rect(500,300,200,20)
        self.slider_handle=pygame.Rect(500+100,285,20,50)
        self.dragged=False
        self.volume=0.5
    def draw(self,screen):
        pygame.draw.rect(screen,(235,219,200),self.rect,0,10)
        pygame.draw.rect(screen,(255,255,255),self.slider_rect,0,10)
        pygame.draw.rect(screen,(0,0,0),self.slider_handle,0,10)
        draw_text(f'Music Volume: {self.volume*100:.0f}%',button_font,(0,0,0),400,220)
sound_menu=SoundMenu()

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
    def draw(self,screen,dt):
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
        if self.type in ['worker10x','scout10x','soldier10x','leafcutter10x','wood10x','fire10x','dracula10x','wheat10x','salt10x']:
            self.rect=pygame.Rect(x,y,50,50)
    def draw(self,screen):
        
        pygame.draw.rect(screen,self.color,self.rect)
        pygame.draw.rect(screen,self.border_color,self.rect,width=2)
        text_surface= hatch_font.render(self.type, True, (0, 0, 0))
        if self.type in ['worker10x','scout10x','soldier10x','leafcutter10x','wood10x','fire10x','dracula10x','wheat10x','salt10x']:
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
        self.speed=250
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
            self.hp=4000
            self.maxhp=4000
            self.dmg=10
            self.range=100
            self.attack_speed=0.4
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
            attacks_path2_charge=get_resource_path('assets/grasshopper-attack-2-charging')
            attacks_path2_dash=get_resource_path('assets/grasshopper-attack-2-dashing')
            self.walks=[pygame.transform.rotate(pygame.transform.scale(pygame.image.load(f"{walks_path}/{f}").convert_alpha(), (34*10,54*10)),-90) for f in os.listdir(walks_path) if f.endswith(".png")]
            self.attacks1=[pygame.transform.rotate(pygame.transform.scale(pygame.image.load(f"{attacks_path}/{f}").convert_alpha(), (34*10,54*10)),-90) for f in os.listdir(attacks_path) if f.endswith(".png")]
            self.attacks2_charge=[pygame.transform.rotate(pygame.transform.scale(pygame.image.load(f"{attacks_path2_charge}/{f}").convert_alpha(), (34*10,54*10)),-90) for f in os.listdir(attacks_path2_charge) if f.endswith(".png")]
            self.attacks2_dash=[pygame.transform.rotate(pygame.transform.scale(pygame.image.load(f"{attacks_path2_dash}/{f}").convert_alpha(), (34*10,54*10)),-90) for f in os.listdir(attacks_path2_dash) if f.endswith(".png")]
            self.img=self.walks[0]
            self.rect=pygame.Rect(x-225,y-150,450,300)
            self.speed=200
            self.hp=10000
            self.maxhp=10000
            self.dmg=6
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

            self.is_skill1_waiting=False
            self.skill1_wait_timer=0
            self.skill1_wait_duration=0.75

            self.is_flying=False
            self.flight_timer=0
            self.flight_duration=1.5
            self.start_x=0
            self.start_y=0

            self.is_skill2_waiting=False
            self.skill2_wait_timer=0
            self.skill2_wait_duration=0.75
            self.is_dashing=False
            self.dash_timer=0
            self.dash_duration=1
        self.untouchable=False

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
        if self.x>1250: 
            self.x=1250
        if self.type=='mantis':
            if self.y>600:
                self.y=600
        else:
            if self.y>500:
                self.y=500
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
               HatchButton(475,450,'worker10x'),HatchButton(1275,450,'scout10x'),HatchButton(875,450,'soldier10x'),HatchButton(875,515,'leafcutter10x'),HatchButton(875,580,'wood10x'),HatchButton(875,645,'fire10x'),HatchButton(875,710,'dracula10x')]
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
barrack_buttons=[HatchButton(400,250,'wheat'),HatchButton(700,250,'salt'),HatchButton(325,250,'wheat10x'),HatchButton(975,250,'salt10x')]
barrack_info_icons=[InfoButton(370,220,'wheat'),InfoButton(950,220,'salt')]
tutorial_ant=TutorialAnt(50,650)
tutorial_on=True

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
reward_chosen=True