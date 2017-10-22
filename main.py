import pygame, sys
import ClassCharacter as CC
import ClassState as CS
import ClassScence as CSc 
import ClassPlayer as CP
from pygame.locals import *
pygame.init()

def reborn(hero_team) :
    x = 10
    for hero in hero_team :
        hero.hp = hero.Hp
        hero.expire = False
        hero.x = x
        hero.y = 10
        hero.direction = "right"
        x -= 1
    return hero_team
# initial setup
CELL_SIZE = 32
WIDTH = CELL_SIZE * 32
HEIGHT = CELL_SIZE * 18
Display = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("RADIUS")
FPS = 15

# define carrier
hero_team = 0                   # list
hero_able_use = 0               # list
select_state_carrier = 0        # str
state_counter = 1               # int
state_carrier = 0               # str
complete_carrier = 0            # str
over_carrier = 0                # str

# start manu >> plyer obj
start_scence = CSc.StartScence(Display, FPS)
f_name = start_scence.run()
player = CP.Player(f_name)

select_character_scence = CSc.SelectCharacter(Display, player, FPS)
over_scence = CSc.GameOver(Display, player, FPS)
complete_scence = CSc.Complete(Display, player, FPS)
select_state_scence = CSc.SelectState(Display, player, FPS)
while True :   
    # select character >> hero team(only leader)
    (hero_team, hero_able_use) = select_character_scence.run()
    while True :       
        if over_carrier == "back" or complete_carrier == "back" :
            # back to select character
            complete_carrier = ""
            over_carrier = ""
            break
        # copy hero team for sent to state
        hero_team_copy = hero_team[:]
        hero_able_use_copy = hero_able_use[:]        
        # select state >> select state carrier
        select_state_carrier = select_state_scence.run()
        if select_state_carrier == "back" :
            # back to select character
            break
        state_counter = 1 # setup state counter
        while True :         
            # generate state obj.
            select_lib = CS.state_lib[select_state_carrier]
            state = select_lib[state_counter](Display, hero_team_copy, hero_able_use_copy, player, FPS)
            hero_team_copy = reborn(hero_team_copy) # reset status hero team
            state_carrier = state.run() # play game
            if state_carrier == "over" :
                over_carrier = over_scence.run()
                if over_carrier == "again" :
                    # copy hero team for replay (reset team)
                    hero_team_copy = hero_team[:]
                    hero_able_use_copy = hero_able_use[:]                     
                    continue
                elif over_carrier == "back" :
                    break
            if state_carrier == "complete" :
                # copy hero team for next game
                hero_team = hero_team_copy[:]
                hero_able_use = hero_able_use_copy[:]
                complete_carrier = complete_scence.run()
                state_counter += 1
                if state_counter > select_lib[0] : 
                    # clear all game in state
                    select_state_carrier += 1   # go to next state
                    state_counter = 1   # reset counter
                    if select_state_carrier > CS.state_lib[0] :
                        # clear all state
                        break   
                    # unlock next state
                    key = "map" + str(select_state_carrier)
                    player.state_unlock[key] = True                
                if complete_carrier == "back" :
                    break
                elif complete_carrier == "next" :
                    continue
player.file.close()
pygame.quit()
sys.exit()