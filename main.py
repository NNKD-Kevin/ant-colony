import pygame
import random
import math
import os
import sys
pygame.mixer.init()

from init import *

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
        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_m:
                if sound_menu.toggled:
                    sound_menu.toggled=False
                else:
                    sound_menu.toggled=True

        
        mouse_pos=pygame.mouse.get_pos()
        if sound_menu.toggled:
            if event.type==pygame.MOUSEBUTTONDOWN:
                if event.button==1:
                    if sound_menu.slider_rect.collidepoint(mouse_pos):
                        sound_menu.dragged=True
            if event.type==pygame.MOUSEBUTTONUP:
                if event.button==1:
                    sound_menu.dragged=False
            if event.type==pygame.MOUSEMOTION:
                if sound_menu.dragged:
                    sound_menu.slider_handle.x=max(500,min(mouse_pos[0],680))
                    sound_menu.volume=(sound_menu.slider_handle.x-500)/200
                    pygame.mixer.music.set_volume(sound_menu.volume)


        if stage=='collecting':
            if event.type==pygame.MOUSEBUTTONDOWN and collected==False:
                button_click.play()
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
                        button_click.play()
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
                            button_click.play()
                            for i in range(max_foods):
                                foods.append(Food(random.randint(400,1300),random.randint(200,750),random.randint(0,100)))
                            for worker in workers:
                                worker.carrying=None
                        if button.function=='sleep':
                            button_click.play()
                            day+=1
                            stamina=max_stamina
                            collected=False
                            transition=True
                            darkness=255
                        if button.function=='storage' and not menu_on:
                            button_click.play()
                            menu_on=True
                            storaging=True
                            for soldier in soldiers:
                                soldier.x=soldier.random_x
                                soldier.y=soldier.random_y
                                soldier.target_x=soldier.random_x
                                soldier.target_y=soldier.random_y
                        if button.function=='hatch' and not menu_on:
                            button_click.play()
                            menu_on=True
                            hatching=True
                else:
                    button.img=button.passive
            if menu_on:
                if event.type==pygame.MOUSEBUTTONDOWN:
                    if not menu.collidepoint(mouse_pos):
                        button_click.play()
                        menu_on=False
                        storaging=False
                        hatching=False
                if return_button_nest.rect.collidepoint(mouse_pos):
                    return_button_nest.img=return_button_nest.active_img
                    if event.type==pygame.MOUSEBUTTONDOWN:
                        button_click.play()
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
                                button_click.play()
                                if button.type=='worker ant' and calories>=5:
                                    calories-=5
                                    workers.append(WorkerAnt(100,50))
                                if button.type=='scout ant' and calories>=5:
                                    calories-=5
                                    max_foods+=1
                                if button.type=='soldier ant' and calories>=3:
                                    calories-=3
                                    soldiers.append(SoldierAnt(1500,850,'black',hp_buff,power_buff))
                                if button.type=='leafcutter ant' and calories>=3 and leaf>0:
                                    calories-=3
                                    leaf-=1
                                    soldiers.append(SoldierAnt(1500,850,'leafcutter',hp_buff,power_buff))
                                if button.type=='wood ant' and calories>=3 and honey>0:
                                    calories-=3
                                    honey-=1
                                    soldiers.append(SoldierAnt(1500,850,'wood',hp_buff,power_buff))
                                if button.type=='fire ant' and calories>=3 and apple_seed>0:
                                    calories-=3
                                    apple_seed-=1
                                    soldiers.append(SoldierAnt(1500,850,'fire',hp_buff,power_buff))
                                if button.type=='dracula ant' and calories>=3 and blood>0:
                                    blood-=1
                                    calories-=3
                                    soldiers.append(SoldierAnt(1500,850,'dracula',hp_buff,power_buff))
                                if button.type=='worker10x' and calories>=50:
                                    calories-=50
                                    for i in range(10):
                                        workers.append(WorkerAnt(100,50))
                                if button.type=='scout10x' and calories>=50:
                                    calories-=50
                                    for i in range(10):
                                        max_foods+=1
                                if button.type=='soldier10x' and calories>=30:
                                    calories-=30
                                    for i in range(10):
                                        soldiers.append(SoldierAnt(1500,850,'black',hp_buff,power_buff))
                                if button.type=='leafcutter10x' and calories>=30 and leaf>=10:
                                    calories-=30
                                    for i in range(10):
                                        leaf-=1
                                        soldiers.append(SoldierAnt(1500,850,'leafcutter',hp_buff,power_buff))
                                if button.type=='wood10x' and calories>=30 and honey>=10:
                                    calories-=30
                                    for i in range(10):
                                        honey-=1
                                        soldiers.append(SoldierAnt(1500,850,'wood',hp_buff,power_buff))
                                if button.type=='fire10x' and calories>=30 and apple_seed>=10:
                                    calories-=30
                                    for i in range(10):
                                        apple_seed-=1
                                        soldiers.append(SoldierAnt(1500,850,'fire',hp_buff,power_buff))
                                if button.type=='dracula10x' and calories>=30 and blood>=10:
                                    calories-=30
                                    for i in range(10):
                                        blood-=1
                                        soldiers.append(SoldierAnt(1500,850,'dracula',hp_buff,power_buff))
                            
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
                                button_click.play()
                                if button.type=='wheat' and wheat>0:
                                    wheat-=1
                                    hp_buff+=1
                                if button.type=='salt' and salt>0:
                                    salt-=1
                                    power_buff+=1
                                if button.type=='wheat10x' and wheat>=10:
                                    wheat-=10
                                    hp_buff+=10
                                if button.type=='salt10x' and salt>=10:
                                    salt-=10
                                    power_buff+=10
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
            if reward_chosen:
                if return_button_combat.rect.collidepoint(mouse_pos):
                    return_button_combat.img=return_button_combat.active_img
                    if event.type==pygame.MOUSEBUTTONDOWN:
                        button_click.play()
                        stage='nest'
                else:
                    return_button_combat.img=return_button_combat.passive_img
            else:
                for card in choosing_cards:
                    if card.rect.collidepoint(mouse_pos):
                        card.toggled=True
                        if event.type==pygame.MOUSEBUTTONDOWN:
                            button_click.play()
                            reward_chosen=True
                            cards.append(card)
                            choosing_cards=[]
                    else:
                        card.toggled=False

                    


    #LOGIC HANDLING
    if tutorial_on:
        tutorial_manager.check_progress()
        if not tutorial_manager.finished_talking and not tutorial_manager.is_hidden:
            tutorial_ant.update(dt)
    #Boss Logic
    if stage=='nest':
        pass
        if day==6 and not combat1_won:
            choosecombat=True
            stage='combat'
            for soldier in soldiers:
                soldier.x=random.randint(100,1400)
                soldier.y=1500
            bosses.append(mantis)
            mantis.hp=1
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
            mantis.maxhp=20000
            mantis.hp=20000
            mantis.dmg=16
            mantis.attack_speed=0.1
            mantis.attack_duration=0.3
            bosses[0].x,bosses[0].y=500,0
            dead_ants=[]
        elif day==13 and not combat4_won:
            choosecombat=True
            stage='combat'
            for soldier in soldiers:
                soldier.x=random.randint(100,1400)
                soldier.y=1500
            bosses.append(grasshopper)
            grasshopper.maxhp=100000
            grasshopper.hp=100000
            grasshopper.dmg=35
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
                if worker.carrying.type=='chips':calories+=1
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
                        if worker.carrying.type=='chips':calories+=1
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
                            if not bosses[0].untouchable:
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
                cardset=set()
                processor=[]
                i=0
                while len(choosing_cards)<3:
                    processor.append(Card(100+500*i,200,random.randint(1,100)))
                    if processor[-1].index not in cardset:
                        cardset.add(processor[-1].index)
                        choosing_cards.append(processor[-1])
                        choosing_cards[-1].x=100+500*i
                        i+=1
                reward_chosen=False
                if day==13:
                    stage='ending'         
        for acid in acids[:]:
            acid.update()
            if not bosses:
                break
            if not skill:
                if acid.rect.colliderect(bosses[0].rect) and not bosses[0].untouchable:
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
            #Boss Attack
            if boss.is_attacking:
                boss.is_moving=False
                boss.attack_animation_timer+=dt                    
                if not boss.attack_hit and boss.attack_animation_timer>=boss.attack_animation_speed:
                    boss.attack_hit=True
                    target=boss.attack_target
                    if target is not None and target in soldiers:
                        if boss.type!='grasshopper':
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
                    if boss.type=='mantis':
                        boss.attack_target=nearest_soldier
                        boss.is_attacking=True
                        boss.attack_hit=False
                        boss.attack_animation_timer=0
                    else:
                        boss.skill_activate+=1
                        boss.attack_timer=1
                        if boss.skill_activate>=boss.skill_duration:
                            skill=True
                            furthestsoldier=False
                            boss.skill_activate=0
                            chooseskill=random.randint(1,2)
        elif bosses and skill:              
            boss=bosses[0]                      
            for s in soldiers[:]:
                if s.hp<=0:
                    dead_ants.append(s.type)
                    soldiers.remove(s)
            if boss.type=='mantis':
                skill=False
            elif boss.type=='grasshopper':
                #Jump Skill
                if chooseskill==1:
                    #1. Identify Target
                    if not furthestsoldier:
                        furthest_soldier=max(soldiers,key=lambda s:math.hypot(s.x-bosses[0].x,s.y-bosses[0].y),default=None)                  
                        if furthest_soldier:
                            bosses[0].target_x=furthest_soldier.x
                            bosses[0].target_y=furthest_soldier.y-150
                        if boss.target_y>500:
                            boss.target_y=500
                        if boss.target_y<250:
                            boss.target_y=250
                        if boss.target_x<250:
                            boss.target_x=250
                        if boss.target_x>1250:
                            boss.target_x=1250
                        boss.is_skill1_waiting=True
                        boss.skill1_wait_timer=0
                        furthestsoldier=True

                    #2.Charging
                    if boss.is_skill1_waiting:
                        boss.skill1_wait_timer+=dt
                        boss.is_moving=False
                        if boss.skill1_wait_timer>=boss.skill1_wait_duration:
                            boss.is_skill1_waiting=False
                            boss.is_flying=True
                            boss.flight_timer=0
                            boss.start_x=boss.x
                            boss.start_y=boss.y
                            boss.untouchable=True

                    #3. Flyingg
                    if boss.is_flying:
                        boss.flight_timer+=dt
                        p=min(1.0,boss.flight_timer/boss.flight_duration)
                        boss.x=boss.start_x+(boss.target_x-boss.start_x)*p
                        boss.y=boss.start_y+(boss.target_y-boss.start_y)*p
                        if boss.flight_timer>=boss.flight_duration:
                            boss.is_flying=False
                            boss.untouchable=False
                            skill=False
                            furthestsoldier=False
                            for s in soldiers[:]:
                                if s.rect.colliderect(boss.rect):
                                    s.hp-=boss.dmg
                else:
                    #Dash Skill
                    #1. Identify Target
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
                        furthestsoldier=True
                        boss.is_skill2_waiting=True
                        boss.skill2_wait_timer=0

                    #2. Wait
                    if boss.is_skill2_waiting:
                        boss.skill2_wait_timer+=dt
                        boss.is_moving=False
                        if boss.skill2_wait_timer>=boss.skill2_wait_duration:
                            boss.is_skill2_waiting=False
                            boss.is_dashing=True
                            boss.dash_timer=0
                            boss.start_x=boss.x
                            boss.start_y=boss.y
                            boss.untouchable=True

                    #3. Dash
                    if boss.is_dashing:
                        boss.dash_timer+=dt
                        p=min(1.0,boss.dash_timer/boss.dash_duration)
                        boss.x=boss.start_x+(boss.target_x-boss.start_x)*p
                        boss.y=boss.start_y+(boss.target_y-boss.start_y)*p
                        if boss.dash_timer>=boss.dash_duration:
                            boss.is_dashing=False
                            boss.untouchable=False
                            skill=False
                            furthestsoldier=False
                            for s in soldiers[:]:
                                    if s.rect.colliderect(boss.rect):
                                        s.hp-=boss.dmg
        if len(soldiers)==0:
            stage='return'

    target_music='combat' if stage=='combat' else 'ambient'
    if current_music!=target_music:
        if target_music=='combat':
            pygame.mixer.music.load(combat_music_path)   
        else:
            pygame.mixer.music.load(ambient_music_path)
        pygame.mixer.music.play(loops=-1) 
        current_music=target_music                
                    
                



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
        info_icons=[InfoButton(350,220,'worker'),InfoButton(750,220,'soldier'),InfoButton(1150,220,'scout')]
        cocoons=[Cocoon(280,250,1),Cocoon(680,250,2),Cocoon(1080,250,3)]
        notifications=[]
        hatch_icons=[Icon(500,150,'leaf',leaf),Icon(600,150,'honey',honey),Icon(700,150,'seed',apple_seed),Icon(800,150,'blood',blood)]
        barrack_icons=[Icon(500,150,'wheat',blood),Icon(600,150,'salt',blood)]
        barrack_info_icons=[InfoButton(350,220,'wheat'),InfoButton(750,220,'salt')]
        barrack_buttons=[HatchButton(400,250,'wheat'),HatchButton(700,250,'salt'),HatchButton(325,250,'wheat10x'),HatchButton(975,250,'salt10x')]
        combat1_won=False
        combat2_won=False
        combat3_won=False
        combat4_won=False
        harvest=[]
        dead_ants=[]



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
    #Nest Rendering
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
        draw_text("Click M to toggle settings",text_font,(0,0,0),700,10)
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
                    screen.blit(soldier.img,(soldier.x,soldier.y))
                    soldier.move_towards(dt)
                ant_moving_timer-=dt
                if ant_moving_timer<=0:
                    ant_moving_timer=5
                    for soldier in soldiers:
                        gacha_x=soldier.x+random.randint(-200,200)
                        gacha_y=soldier.y+random.randint(-200,200)
                        soldier.target_x=max(150,min(1200,gacha_x))
                        soldier.target_y=max(300,min(700,gacha_y))
                for soldier in soldiers:
                    if soldier.is_moving:
                        soldier.animation_timer+=dt
                        if soldier.animation_timer>soldier.animation_speed:
                            soldier.animation_timer=0
                            soldier.frame_index+=1
                            soldier.img=pygame.transform.rotate(soldier.walks[soldier.frame_index%len(soldier.walks)], -soldier.angle)
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
        for boss in bosses:
            if stage=='combat':
                walks=getattr(boss,'walks',[])
                attacks1=getattr(boss,'attacks1',[])
            if boss.type=='grasshopper' and boss.is_skill1_waiting:
                progress=boss.skill1_wait_timer/boss.skill1_wait_duration   #Grasshoper skill 1 animation
                index=min(int(progress*len(attacks1)),len(attacks1)-1)
                boss.img=pygame.transform.rotate(attacks1[index], -boss.angle)
                boss.draw(screen)
            elif boss.type=='grasshopper' and boss.is_flying:
                p=min(1.0,boss.flight_timer/boss.flight_duration)
                if p<0.5:
                    scale=1.0+p
                else:
                    scale=1.5-(p-0.5)
                boss.animation_timer+=dt
                if boss.animation_timer>boss.animation_speed:
                    boss.animation_timer=0
                    boss.frame_index+=1
                frame=walks[boss.frame_index%len(walks)]
                new_width=int(frame.get_width()*scale)
                new_height=int(frame.get_height()*scale)
                scaled_frame=pygame.transform.scale(frame,(new_width,new_height))
                boss.img=pygame.transform.rotate(scaled_frame, -boss.angle)

                draw_x=boss.x-150-(new_width-340)/2
                draw_y=boss.y-150-(new_height-540)/2
                screen.blit(boss.img,(draw_x,draw_y))
            elif boss.type=='grasshopper' and boss.is_skill2_waiting:
                dash_dx=boss.target_x-boss.x
                desired_angle=0 if dash_dx>0 else 180
                delta=(desired_angle-boss.angle+180)%360-180
                boss.angle+=max(-10,min(10,delta))
                boss.angle%=360
                boss.skill2_wait_timer+=dt
                progress=boss.skill2_wait_timer/boss.skill2_wait_duration
                attacks2_charge=getattr(boss,'attacks2_charge',[])
                if attacks2_charge:
                    frame_idx=min(int(progress*3),2)
                    boss.img=pygame.transform.rotate(attacks2_charge[frame_idx], -boss.angle)
                boss.draw(screen)
            elif boss.type=='grasshopper' and boss.is_dashing:
                boss.dash_timer+=dt
                progress=boss.dash_timer/boss.dash_duration
                attacks2_dash=getattr(boss,'attacks2_dash',[])
                if attacks2_dash:
                    frame_idx=min(int(progress*3),2)
                    boss.img=pygame.transform.rotate(attacks2_dash[frame_idx], -boss.angle)
                boss.draw(screen)

            else:
                if boss.is_attacking and attacks1:
                    progress=boss.attack_animation_timer/boss.attack_duration   #Matis attack animation
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
        
        for acid in acids:
            acid.draw(screen)
            acid.update()
            acid.move(dt)
        if stage=='combat' and ((combat1_won and day==6) or (combat2_won and day==8) or (combat3_won and day==10)):
            pygame.draw.rect(screen,(99,53,42),(300,200,900,550))
            draw_text('Combat Complete',button_font,(255,255,255),500,250)
            n=0
            draw_text('Casualties:',hatch_font,(255,255,255),400,325)
            for i in range(5):
                if ant_types[i] in dead_ants:
                    screen.blit(ant_icons[i],(475,350+n*75))
                    draw_text(f'-{dead_ants.count(ant_types[i])}',button_font,(255,255,255),415,350+n*75)
                    n+=1
            if not reward_chosen:
                overlay=pygame.Surface((1500,850),pygame.SRCALPHA)
                overlay.fill((0,0,0,150))
                screen.blit(overlay,(0,0))
                for card in choosing_cards:
                    card.draw(screen)
            if reward_chosen:
                return_button_combat.draw(screen)


        
    if stage=='ending':
        screen.fill((0,0,0))
        logo_y-=dt*150
        screen.blit(white_logo,(500,logo_y))
        for credit in credits:
            credit.update(dt)

    
    #Global Rendering
    if reward_chosen:
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
        tutorial_manager.draw(screen,dt)
        if day<3:
            tutorial_ant.draw(screen)
    if sound_menu.toggled:
        sound_menu.draw(screen)
    if 0<mouse_pos[0]<1500 and 0<mouse_pos[1]<850:
        pygame.mouse.set_visible(False)
    if 10<mouse_pos[0]<1490 and 10<mouse_pos[1]<840:
        screen.blit(cursor_img,mouse_pos)
    else:
        pygame.mouse.set_visible(True)


        
    pygame.display.update()


pygame.quit()
