import pygame, random
import ClassCharacter as CC
import ClassInterface as CI
import ClassItem as CIm
from pygame.locals import *
""" GameState Super class """
class GameState :
    #GameState's class variable
    imageRoot = "image\map\\"
    soundRoot = "sounds\SBG\\"
    def __init__(self, display, heroTeam, hero_able_use, player, FPS=15) :
        # display setup
        self.Display = display
        self.FPS = FPS
        self.FPSclock = pygame.time.Clock()
        self.display_width = self.Display.get_width()
        self.display_height = self.Display.get_height()
        self.cell_size = 32
        self.state_end = None
        pygame.mixer.music.load(self.soundRoot + self.sound_bg)
        
        self.player = player
        self.hero_able_use = hero_able_use
        self.cache_direction = "right"
        # obj list
        self.heroTeam = heroTeam
        self.monsterTeams = []
        self.attacks = []
        self.damages = []
        self.potions = [0, CIm.HpPotion1(), CIm.HpPotion2(), CIm.HpPotion3(), CIm.HpPotion4()]
        
        self.field = {}     #dictionary of field
        self.kill_counter = [0,0]   #[0] = counter , [1] = total monster
        # drop hero
        if len(hero_able_use) > 0 and len(heroTeam) < 5 :
            drop_hero = CIm.DropHero(self.randomPos(), hero_able_use)
            self.items = [drop_hero]        
        else :
            self.items = []
            self.wave_order[0] = 0
        # interface setup
        self.money = [0]
        self.potion_counter = [0,30]        #[0] = counter, [1] = max count
        self.interface = CI.StateInterface(self.Display, self.heroTeam, self.kill_counter, self.name, self.money, self.potion_counter, self.player.hp_potions)
    """inter state mrthod"""
    def run(self) :
        pygame.mixer.music.play(-1, 0.0)
        #state game loop
        while True :
            # check end loop
            if self.state_end == "complete" :
                self.player.money += self.money[0]
                pygame.mixer.music.stop()
                return "complete"
            if self.state_end == "over" :
                self.player.money += self.money[0]
                pygame.mixer.music.stop()
                return "over"
            # event handle phase                   #               [event handle phase]
            self.checkControlKey()                 #                ^                |          
            # modify phase                         #                |                v
            self.checkHeroHitWall()                #     [pre finish phase]      [modify phase]
            self.manageMoveTeam()                  #                ^                |
            self.manageWaveMonster()               #                |                v
            self.sendFrame()                       #                   [draw phase]
            if self.potion_counter[0] < self.potion_counter[1] :
                self.potion_counter[0] += 1
            # draw phase
            self.Display.fill((255,255,255))        #                1 loop process
            self.drawMap()
            self.drawItem()
            self.manageDrawTeam()
            self.drawAttack()
            self.drawDamage()
            self.interface.draw()
            # pre finish phase
            self.sendField()
            self.garbageCollect()
            self.resetField()
            # loop control
            if len(pygame.event.get(QUIT)) > 0 :
                self.player.encode()
                pygame.quit()
                sys.exit()
            pygame.display.update()
            self.FPSclock.tick(self.FPS)
    """ event handle method """
    def checkControlKey(self) :
        leader = self.heroTeam[0]
        events = pygame.event.get(KEYDOWN)
        for e in events :
            # direction control
            if (e.key == K_w or e.key == K_UP) and leader.direction != "down" :
                self.cache_direction = "up"
            elif (e.key == K_s or e.key == K_DOWN) and leader.direction != "up" :
                self.cache_direction = "down"
            elif (e.key == K_a or e.key == K_LEFT) and leader.direction != "right" :
                self.cache_direction = "left"            
            elif (e.key == K_d or e.key == K_RIGHT) and leader.direction != "left" :
                self.cache_direction = "right"
            # potion control
            elif e.key == 49 :  # ! (1)
                self.usePotion(1)
            elif e.key == 50 :  # @ (2)
                self.usePotion(2)
            elif e.key == 51 :  # # (3)
                self.usePotion(3)
            elif e.key == 52 :  # $ (4)
                self.usePotion(4)              
            elif e.key == K_ESCAPE :
                self.pause()    
    """ modify method """
    def checkHeroHitWall(self) :
        leader = self.heroTeam[0]
        if leader.x <= 3 or leader.x >= 31 or leader.y <= 1 or leader.y >= 17 :
            self.state_end = "over"  
    def manageMoveTeam(self) :
        if self.heroTeam[0].countMove() :
            self.heroTeam[0].direction = self.cache_direction
            self.moveTeam(self.heroTeam)
        for monsterTeam in self.monsterTeams :
            monsterTeam[0].countDirection()
            self.safeMonsterDirection(monsterTeam)
            if monsterTeam[0].countMove() :
                self.moveTeam(monsterTeam)
    def moveTeam(self, team) :  # call by manageMoveTeam
        for i in range(len(team)-1,0,-1) :
            team[i].x = team[i-1].x
            team[i].y = team[i-1].y
            team[i].direction = team[i-1].direction
        team[0].move()  
    def safeMonsterDirection(self, monsterTeam) :   # call by manageMoveTeam
        # make sure to no monster team hit the wall
        leader = monsterTeam[0]
        x,y = leader.x, leader.y
        if y-1 <= 1 and leader.direction == "up" :
            # toward top wall
            if x-1 <= 3 :
                # collision in top left wall with "up"
                if len(monsterTeam) > 1 :
                    if monsterTeam[1].direction == "up" :
                        leader.direction = "right"
                    elif monsterTeam[1].direction == "left" :
                        leader.direction = "down"
                else :
                    leader.direction = "right"
            elif x+1 >= 31 :
                # collision in top right wall with "up"
                if len(monsterTeam) > 1 :
                    if monsterTeam[1].direction == "up" :
                        leader.direction = "left"
                    elif monsterTeam[1].direction == "right" :
                        leader.direction = "down"
                else :
                    leader.direction = "left"
            else :
                # collision in top wall
                if len(monsterTeam) > 1 and monsterTeam[1].direction == "left" :
                    leader.direction = "left"
                else :
                    leader.direction = "right"
            leader.dc_spd = 0
        elif y+1 >= 17 and leader.direction == "down" :
            # toward bottom wall
            if x-1 <= 3 :
                # collision in bottom left wall with "down"
                if len(monsterTeam) > 1 :
                    if monsterTeam[1].direction == "down" :
                        leader.direction = "right"
                    elif monsterTeam[1].direction == "left" :
                        leader.direction = "up"
                else :
                    leader.direction = "right"                    
            elif x+1 >= 31 :
                # collision in bottom right wall with "down"
                if len(monsterTeam) > 1 :
                    if monsterTeam[1].direction == "down" :
                        leader.direction = "left"
                    elif monsterTeam[1].direction == "right" :
                        leader.direction = "up"
                else :
                    leader.direction = "left"                                        
            else :
                # collision in bottom wall
                if len(monsterTeam) > 1 and monsterTeam[1].direction == "right" :
                    leader.direction = "right"
                else :
                    leader.direction = "left"
            leader.dc_spd = 0
        elif x-1 <= 3 and leader.direction == "left" :
            # toward left wall
            if y-1 <= 1 :
                # collision in top left wall with "left"
                if len(monsterTeam) > 1 :
                    if monsterTeam[1].direction == "left" :
                        leader.direction = "down"
                    elif monsterTeam[1].direction == "up" :
                        leader.direction = "right"
                else :
                    leader.direction = "down"     
            elif y+1 >= 17 :
                # collision in bottom left wall with "left"
                if len(monsterTeam) > 1 :
                    if monsterTeam[1].direction == "left" :
                        leader.direction = "up"
                    elif monsterTeam[1].direction == "down" :
                        leader.direction = "right"
                else :
                    leader.direction = "up"
            else :
                # collision in left wall
                if len(monsterTeam) > 1 and monsterTeam[1].direction == "down" :
                    leader.direction = "down"
                else :
                    leader.direction = "up"
            leader.dc_spd = 0
        elif x+1 >= 31 and leader.direction == "right" :
            # toward right wall
            if y-1 <= 1 :
                # collision in top right wall with "right"
                if len(monsterTeam) > 1 :
                    if monsterTeam[1].direction == "right" :
                        leader.direction = "down"
                    elif monsterTeam[1].direction == "up" :
                        leader.direction = "left"
                else :
                    leader.direction = "down"
            elif y+1 >= 17 :
                # collision in bottom right wall with "right"
                if len(monsterTeam) > 1 :
                    if monsterTeam[1].direction == "right" :
                        leader.direction = "up"
                    elif monsterTeam[1].direction == "down" :
                        leader.direction = "left"
                else :
                    leader.direction = "up"
            else :
                # collision in right wall
                if len(monsterTeam) > 1 and monsterTeam[1].direction == "up" :
                    leader.direction = "up"
                else :
                    leader.direction = "down"
            leader.dc_spd = 0       
    def manageWaveMonster(self) :
        if self.wave_order[0] == 0 :
            self.wave_order.pop(0)
            if len(self.wave_order) == 0 :
                self.state_end = "complete" 
                return
            for i in range(self.wave_order[0]) :
                team = self.generateMonster(self.monster_order.pop(0))
                self.monsterTeams.append(team)       
    def generateMonster(self, order) :  # call by manageWaveMonster
        team = []
        x,y = self.randomPos()
        for script in order :
            name, level = script
            monster = CC.monster_lib[name](level)
            monster.x = x
            monster.y = y
            team.append(monster)
            x -= 1
        return team
    def sendFrame(self) :
        for hero in self.heroTeam :
            hero.receiveFrame()
        for monsterTeam in self.monsterTeams :
            for monster in monsterTeam :
                monster.receiveFrame()
        for attack in self.attacks :
            attack.receiveFrame()
        for damage in self.damages :
            damage.receiveFrame()    
    """ draw method """
    def drawMap(self) :
        self.Display.blit(self.map_img, (0,0))
    def drawItem(self) :
        for item in self.items :
            self.Display.blit(item.figure, item.getDisplayPos())
            self.setToField(item)    
    def manageDrawTeam(self) :
        for monsterTeam in self.monsterTeams :
            self.drawTeam(monsterTeam)
        self.drawTeam(self.heroTeam)    
    def drawTeam(self, team) :  # call by manage drawTeam
        if team[0].direction == "down" :
            for i in range(len(team)-1, -1,-1) :
                self.Display.blit(team[i].figure, team[i].getDisplayPos())
        else :
            for member in team :
                self.Display.blit(member.figure, member.getDisplayPos())
        for i in range(len(team)-1, -1,-1) :
            self.setToField(team[i])    
    def drawAttack(self) :
        for attack in self.attacks :
            self.Display.blit(attack.figure, (attack.x, attack.y))
            self.setToField(attack)
    def drawDamage(self) :
        for damage in self.damages :
            self.Display.blit(damage.figure, (damage.x, damage.y))  
    def setToField(self, obj) :     # call by draw method
        if obj.obj_type == "Item" :
            self.field[(obj.x, obj.y)] = [obj]
        if obj.obj_type == "Attack" and obj.active:
            # set atk obj to field
            for hold in obj.holding :
                if hold in self.field :
                    # have another in this cell before
                    for another in self.field[hold] :
                        if another.obj_type == obj.target :
                            # another is target of atk obj
                            dmg_obj = obj.damage(another)
                            if dmg_obj != None :
                                self.damages.append(dmg_obj)
                    self.field[hold].append(obj)
                else :
                    self.field[hold] = [obj]
        elif obj.obj_type == "Hero" :
            # set hero to field
            hold = (obj.x, obj.y)
            if hold in self.field :
                # have another in this cell before
                for another in self.field[hold] :
                    if another.obj_type == "Monster" :
                        # another is Monster
                        if obj.leader :
                            #leder hit monster
                            #game over
                            self.state_end = "over"
                        else :
                            # support hero hit monster
                            obj.expire = True
                    elif another.obj_type == "Hero" :
                        # hit hero in same team
                        another.expire = True
                    elif another.obj_type == "Item" and another.target == "Hero" :
                        another.work(self.heroTeam)
                        self.wave_order[0] = len(self.monsterTeams)
                self.field[hold].append(obj)
            else :
                self.field[hold] = [obj]
        elif obj.obj_type == "Monster" :
            # set monster to field
            hold = (obj.x, obj.y)
            if hold in self.field :
                # have another in this cell before
                self.field[hold].append(obj)
            else :
                self.field[hold] = [obj]   
    """ pre finish method """
    def sendField(self) :
        # send field to hero
        for hero in self.heroTeam :  
            # receive obj request field
            request = hero.requestField()
            # pack field
            packed = []
            for cell in request :
                if cell in self.field :
                    packed.append(self.field[cell])
            # send pack and receive attack obj
            attack = hero.receiveField(packed)
            if attack != None :
                self.attacks.append(attack)
        # send field to monster
        for monsterTeam in self.monsterTeams :
            for monster in monsterTeam :
                request = monster.requestField()
                packed = []
                for cell in request :
                    if cell in self.field :
                        packed.append(self.field[cell])
                attack = monster.receiveField(packed)
                if attack != None :
                    self.attacks.append(attack)  
    def garbageCollect(self) :
        # waste expired attack obj
        i = 0
        while i < len(self.attacks) :
            if self.attacks[i].expire :
                self.attacks.pop(i)
                continue
            i += 1
        # waste expire damage
        i = 0
        while i < len(self.damages) :
            if self.damages[i].expire :
                self.damages.pop(i)
                continue
            i += 1        
        # waste expire hero
        i = 0
        while i < len(self.heroTeam) :
            if self.heroTeam[i].expire or self.heroTeam[i].hp <= 0 :
                if self.heroTeam[i].leader :
                    self.state_end = "over"
                self.hero_able_use.append(self.heroTeam[i].char_name)
                self.heroTeam.pop(i)
                continue
            i += 1
        # waste expire monster
        i = 0
        while i < len(self.monsterTeams) :
            monsterTeam = self.monsterTeams[i]
            j = 0
            while j < len(monsterTeam) :
                if monsterTeam[j].expire or monsterTeam[j].hp <= 0 :
                    # send exp to all hero in team
                    mon_level = monsterTeam[j].level
                    self.money[0] += mon_level
                    for hero in self.heroTeam :
                        hero.gainExp(mon_level)
                    monsterTeam.pop(j)
                    continue
                j += 1
            if len(monsterTeam) == 0 :
                self.monsterTeams.pop(i)
                self.wave_order[0] -= 1
                self.kill_counter[0] += 1
            i += 1
        # waste expire item
        i = 0
        while i < len(self.items) :
            if self.items[i].expire :
                self.items.pop(i)
                continue
            i += 1    
    def resetField(self) :
        del self.field
        self.field = {}
    """ utility method """   
    def randomPos(self) :
        return (random.randint(4,30), random.randint(2,16))    
    def pause(self) :
        pygame.mixer.music.stop()
        while True :
            for e in pygame.event.get() :
                if e.type == QUIT :
                    self.player.file.close()
                    pygame.quit()
                    sys.exit()
                elif e.type == KEYDOWN and e.key == K_ESCAPE :
                    pygame.mixer.music.play(-1, 0.0)
                    return
            pygame.display.update()
            self.FPSclock.tick(self.FPS)
    def usePotion(self, type) :
        if self.potion_counter[0] >= self.potion_counter[1] and self.player.hp_potions[type] > 0 :
            heal_dmgs = self.potions[type].work(self.heroTeam)  
            self.damages.extend(heal_dmgs)
            self.player.hp_potions[type] -= 1
            self.potion_counter[0] = 0
            self.potion_counter[1] = 15*type
    
""" concret class """
""" state 1 : Wind Forrest """
class WindForest_1(GameState) :
    name = "Wind Forest - 1"
    sound_bg = "Wind Forrest_SBG.mid"
    def __init__(self, display, heroSet, hero_able_use, player, FPS=15) :
        self.wave_order = [-1,1,2]
        GameState.__init__(self, display, heroSet, hero_able_use, player, FPS)
        self.map_img = pygame.image.load(self.imageRoot + "wind forest.png")
        self.kill_counter[1] = 3
        self.monster_order = [[("Slime1",1), ("Slime1",1)],
                              
                              [("Slime1",1), ("Slime1",2), ("Slime1",2)],
                              [("BigSlime1",2)]]
class WindForest_2(GameState) :
    name = "Wind Forest - 2"
    sound_bg = "Wind Forrest_SBG.mid"
    def __init__(self, display, heroSet, hero_able_use, player, FPS=15) :
        self.wave_order = [-1,1,2,3]
        GameState.__init__(self, display, heroSet, hero_able_use, player, FPS)
        self.map_img = pygame.image.load(self.imageRoot + "wind forest.png")
        self.kill_counter[1] = 6
        self.monster_order = [[("Slime2",2), ("Slime2",2), ("Slime2",2)],
                              
                              [("Slime2",3), ("Slime2",2), ("Slime2",2)],
                              [("BigSlime2",2), ("BigSlime2",2)],
                              
                              [("Slime2",4), ("Slime2",3), ("Slime2",3)],
                              [("BigSlime2",3), ("Slime2",2), ("Slime2",2), ("Slime2",2)],
                              [("BigSlime3",4)]]
class WindForest_3(GameState) :
    name = "Wind Forest - 3"
    sound_bg = "Wind Forrest_SBG.mid"
    def __init__(self, display, heroSet, hero_able_use, player, FPS=15) :
        self.wave_order = [-1,2,2,3]
        GameState.__init__(self, display, heroSet, hero_able_use, player, FPS)
        self.map_img = pygame.image.load(self.imageRoot + "wind forest.png")
        self.kill_counter[1] = 7
        self.monster_order = [[("Slime3",3), ("Slime3",3), ("Slime3",3)],
                              [("Slime3",4), ("BigSlime3",3), ("Slime3",4)],
                              
                              [("Slime3",4), ("BigSlime3",3), ("Slime3",5)],
                              [("BigSlime3",4), ("Slime4",5), ("BigSlime5",3)],
                              
                              [("Slime3",6), ("Slime3",6)],
                              [("Slime3",5), ("Slime3",5), ("Slime3",5)],
                              [("BigSlime3",2), ("BigSlime2",3), ("BigSlime1",4)]]

class WindForest_4(GameState) :
    name = "Wind Forest - 4"
    sound_bg = "Wind Forrest_SBG.mid"
    def __init__(self, display, heroSet, hero_able_use, player, FPS=15) :
        self.wave_order = [-1,2,3,3]
        GameState.__init__(self, display, heroSet, hero_able_use, player, FPS)
        self.map_img = pygame.image.load(self.imageRoot + "wind forest.png")
        self.kill_counter[1] = 8
        self.monster_order = [[("Slime4",4), ("Slime4",4), ("Slime4",4)],
                              [("Slime5",4), ("Slime5",5), ("Slime5",4)],
                              
                              [("Slime1",6), ("Slime2",6), ("Slime3",6)],
                              [("Slime4",6), ("Slime5",6), ("Slime2",6)],
                              [("Slime1",6), ("Slime3",6), ("Slime4",6)],
                              
                              [("BigSlime1",5), ("BigSlime2",5)],
                              [("BigSlime3",5), ("BigSlime4",5)],
                              [("BigSlime5",5), ("Slime1",7)]]
class WindForest_5(GameState) :
    name = "Wind Forest - 5"
    sound_bg = "Wind Forrest_SBG.mid"
    def __init__(self, display, heroSet, hero_able_use, player, FPS=15) :
        self.wave_order = [-1,1,4,3,1]
        GameState.__init__(self, display, heroSet, hero_able_use, player, FPS)
        self.map_img = pygame.image.load(self.imageRoot + "wind forest.png")
        self.kill_counter[1] = 9   
        self.monster_order = [[("Slime1",10)],
                              
                              [("Slime2",7), ("Slime2",7), ("Slime2",7)],
                              [("Slime3",7), ("Slime3",7), ("Slime3",7)],
                              [("Slime4",8), ("Slime4",8), ("Slime4",8)],
                              [("Slime5",8), ("Slime5",8), ("Slime5",8)],
                              
                              [("BigSlime1",6), ("BigSlime2",6)],
                              [("BigSlime3",6), ("BigSlime4",6)],
                              [("BigSlime4",6), ("BigSlime5",6)],
                              
                              [("BigSlime5",8)]]
    
""" map 2 : Forbidden Forrest """        
class ForbiddenForest_1(GameState) :
    name = "Forbidden Forest - 1"
    sound_bg = "Forbidden Forest_SBG.mid"
    def __init__(self, display, heroTeam, hero_able_use, player, FPS=15) :
        self.wave_order = [-1,2,2,2]
        GameState.__init__(self, display, heroTeam, hero_able_use, player, FPS=15)
        self.map_img = pygame.image.load(self.imageRoot + "forbidden forest.png")
        self.kill_counter[1] = 6
        self.monster_order = [[("Mushroom1",5), ("Mushroom1",5), ("Mushroom1",6)],
                              [("Flower1",5), ("Flower1",5), ("Flower2",6)],
                              
                              [("Mushroom1",6), ("Flower1",5), ("Flower1",5)],
                              [("Mushroom1",6), ("Flower2",5), ("Flower2",5)],
                              
                              [("Mushroom1",7), ("Flower1",7), ("Flower2",8)],
                              [("Mushroom1",8), ("Mushroom1",9), ("Mushroom1",8)]]
class ForbiddenForest_2(GameState) :
    name = "Forbidden Forest - 2"
    sound_bg = "Forbidden Forest_SBG.mid"
    def __init__(self, display, heroTeam, hero_able_use, player, FPS=15) :
        self.wave_order = [-1,2,3,2]
        GameState.__init__(self, display, heroTeam, hero_able_use, player, FPS)
        self.map_img = pygame.image.load(self.imageRoot + "forbidden forest.png")
        self.kill_counter[1] = 7
        self.monster_order = [[("Bat1",6), ("Bat2",6), ("Bat3",6)],
                              [("Wolf1",6), ("Wolf1",7), ("Wolf1",6)],
                
                              [("Wolf2",7), ("Wolf1",6), ("Wolf1",6)],
                              [("Bat1",8), ("Bat2",9), ("Bat2",8)],
                              [("Wolf1",8), ("Wolf3",9), ("Wolf2",7)],
                              
                              [("Wolf3",10), ("Wolf1",7), ("Wolf1",7)],
                              [("Bat3",10), ("Bat1",7), ("Bat1",8)]]
class ForbiddenForest_3(GameState) :
    name = "Forbidden Forest - 3"
    sound_bg = "Forbidden Forest_SBG.mid"
    def __init__(self, display, heroTeam, hero_able_use, player, FPS=15) :
        self.wave_order = [-1, 3, 3, 2, 1]
        GameState.__init__(self, display, heroTeam, hero_able_use, player, FPS) 
        self.map_img = pygame.image.load(self.imageRoot + "forbidden forest.png")
        self.kill_counter[1] = 9
        self.monster_order = [[("WolfGoblin",8), ("Wolf1",6), ("Wolf1",7)],
                              [("WolfGoblin",8), ("Wolf2",6), ("Wolf2",6)],
                              [("WolfGoblin",9), ("Wolf3",7), ("Wolf3",7)],
                              
                              [("GreenGoblin",10), ("Wolf2",7), ("Wolf2",7)],
                              [("GreenGoblin",10), ("WolfGoblin",9), ("WolfGoblin",8)],
                              [("RedGoblin",11), ("WolfGoblin",8)],
                              
                              [("RedGoblin",12), ("GreenGoblin",11), ("WolfGoblin",10)],
                              [("RedGoblin",12), ("GreenGoblin",11), ("WolfGoblin",10)],
                              
                              [("RedGoblin",14)]]
class ForbiddenForest_4(GameState) :
    name = "Forbidden Forest - 4"
    sound_bg = "Forbidden Forest_SBG.mid"
    def __init__(self, display, heroTeam, hero_able_use, player, FPS=15) :
        self.wave_order = [-1, 2, 3, 2]
        GameState.__init__(self, display, heroTeam, hero_able_use, player, FPS)
        self.map_img = pygame.image.load(self.imageRoot + "forbidden forest.png")
        self.kill_counter[1] = 7
        self.monster_order = [[("Ghost1",10), ("Ghost2",11), ("Ghost3",10)],
                              [("Ghost3",11), ("Doll",10), ("Doll",10)],
                              
                              [("Ghost1",12), ("Doll",10), ("Doll",10)],
                              [("Ghost2",13), ("Doll",11), ("Doll",11)],
                              [("Ghost3",14), ("Doll",12), ("Doll",12)],
                              
                              [("Ghost1",14), ("Ghost3",13), ("Ghost2",12)],
                              [("Doll",16)]]
class ForbiddenForest_5(GameState) :
    name = "Forbidden Forest - 5"
    sound_bg = "Forbidden Forest_SBG.mid"
    def __init__(self, display, heroTeam, hero_able_use, player, FPS=15) :
        self.wave_order = [-1, 2, 3, 3]
        GameState.__init__(self, display, heroTeam, hero_able_use, player, FPS)
        self.map_img = pygame.image.load(self.imageRoot + "forbidden forest.png")
        self.kill_counter[1] = 8
        self.monster_order = [[("SkeletonKnight",14), ("RedGoblin",12), ("RedGoblin",12)],
                              [("Zombie",14), ("Ghost1",12), ("Ghost3",12)],
                              
                              [("SkeletonKnight",16), ("SkeletonKnight",15), ("SkeletonKnight",14)],
                              [("Zombie",17), ("Zombie",16), ("Zombie",16)],
                              [("SkeletonKnight",17), ("Zombie",15), ("Zombie",16)],
                              
                              [("SkeletonKnight",19)],
                              [("Zombie",19)],
                              [("SkeletonKing",20)]]
""" map 3 : Fairy Hill """                            
class FairyHill_1(GameState) :
    name = "FairyHill - 1"
    sound_bg = "Fairy Hill_SBG.mid"
    def __init__(self, display, heroTeam, hero_able_use, player, FPS=15) :
        self.wave_order = [-1, 4, 4, 6]
        GameState.__init__(self, display, heroTeam, hero_able_use, player, FPS)
        self.map_img = pygame.image.load(self.imageRoot + "fairy hill.png")
        self.kill_counter[1] = 14
        self.monster_order = [[("FireElemental1",16), ("FireElemental1",16)],
                              [("FireElemental1",17), ("FireElemental1",16)],
                              [("FireElemental1",17), ("FireElemental1",17)],
                              [("FireElemental1",18)],
                              
                              [("FireElemental2",19)], [("FireElemental1",18)],
                              [("FireElemental2",19)], [("FireElemental1",18)],
                              [("FireElemental2",18)], [("FireElemental1",19)],
                              [("FireElemental2",20)],
                              
                              [("FireElemental2",20)],
                              [("FireElemental2",20)],
                              [("FireElemental2",20)],
                              [("FireElemental2",20)],
                              [("FireElemental2",20)],
                              [("FireElemental2",20)]]
class FairyHill_2(GameState) :
    name = "FairyHill - 2"
    sound_bg = "Fairy Hill_SBG.mid"
    def __init__(self, display, heroTeam, hero_able_use, player, FPS=15) :
        self.wave_order = [-1, 4, 4, 6]
        GameState.__init__(self, display, heroTeam, hero_able_use, player, FPS)   
        self.map_img = pygame.image.load(self.imageRoot + "fairy hill.png")
        self.kill_counter[1] = 14
        self.monster_order = [[("EarthElemental1",18), ("EarthElemental1",19)],
                              [("EarthElemental1",18), ("EarthElemental1",19)],
                              [("EarthElemental1",19), ("EarthElemental1",20)],
                              [("EarthElemental2",20)],
                              
                              [("EarthElemental2",20), ("EarthElemental1",19)],
                              [("EarthElemental2",20), ("EarthElemental1",19)],
                              [("EarthElemental2",20), ("EarthElemental1",19)],
                              [("EarthElemental2",21), ("EarthElemental2",20)],
                              
                              [("EarthElemental2",21)],
                              [("EarthElemental2",21)],
                              [("EarthElemental2",21)],
                              [("EarthElemental2",21)],
                              [("EarthElemental2",21)],
                              [("EarthElemental2",22)]]
class FairyHill_3(GameState) :
    name = "FairyHill - 3"
    sound_bg = "Fairy Hill_SBG.mid"
    def __init__(self, display, heroTeam, hero_able_use, player, FPS=15) :
        self.wave_order = [-1, 5, 4, 5]
        GameState.__init__(self, display, heroTeam, hero_able_use, player, FPS)    
        self.map_img = pygame.image.load(self.imageRoot + "fairy hill.png")
        self.kill_counter[1] = 14
        self.monster_order = [[("WindElemental1",20), ("WindElemental1",20)],
                              [("WindElemental1",20), ("WindElemental1",21)],
                              [("WindElemental1",21), ("WindElemental1",20)],
                              [("WindElemental1",21), ("WindElemental1",21)],
                              [("WindElemental2",20)],
                              
                              [("WindElemental2",21), ("WindElemental1",20)],
                              [("WindElemental2",21), ("WindElemental1",20)],
                              [("WindElemental2",21), ("WindElemental1",20)],
                              [("WindElemental2",21), ("WindElemental1",20)],
                              
                              [("WindElemental2",22), ("WindElemental2",21)],
                              [("WindElemental2",22), ("WindElemental2",21)],
                              [("WindElemental2",22), ("WindElemental2",21)],
                              [("WindElemental2",22), ("WindElemental2",21)],
                              [("WindElemental2",23)]]
class FairyHill_4(GameState) :
    name = "Fairy Hill - 4"
    sound_bg = "Fairy Hill_SBG.mid"
    def __init__(self, display, heroTeam, hero_able_use, player, FPS=15) :
        self.wave_order = [-1, 3, 4, 6]
        GameState.__init__(self, display, heroTeam, hero_able_use, player, FPS)    
        self.map_img = pygame.image.load(self.imageRoot + "fairy hill.png")
        self.kill_counter[1] = 13
        self.monster_order = [[("AquaElemental1",15), ("AquaElemental1",16)],
                              [("AquaElemental1",15), ("AquaElemental1",15)],
                              [("AquaElemental1",16), ("AquaElemental1",15)],
                              [("AquaElemental1",17), ("AquaElemental1",15)],
                              
                              [("AquaElemental1",16), ("AquaElemental1",17)],
                              [("AquaElemental2",17)],
                              [("AquaElemental2",16), ("AquaElemental1",17)],
                              [("AquaElemental2",16)],
                              
                              [("AquaElemental2",16)],
                              [("AquaElemental2",17)],
                              [("AquaElemental2",17)],
                              [("AquaElemental2",16)],
                              [("AquaElemental2",17)],
                              [("AquaElemental2",16)]]
""" map 4 : Temple of God """
class TempleOfGod_1(GameState) :
    name = "Temple of God - 1"
    sound_bg = "Temple of God_SBG.mid"
    def __init__(self, display, heroTeam, hero_able_use, player, FPS=15) :
        self.wave_order = [-1, 3, 3, 2]
        GameState.__init__(self, display, heroTeam, hero_able_use, player, FPS)    
        self.map_img = pygame.image.load(self.imageRoot + "temple of god.png")
        self.kill_counter[1] = 8
        self.monster_order = [[("Angel1",23), ("Angel1",22), ("Angel1",22)],
                              [("Angel1",23), ("Angel1",21), ("Angel1",22)],
                              [("Angel1",22), ("Angel1",23), ("Angel1",23)],
                              
                              [("Angel1",22), ("Angel1",23), ("Angel1",23)],
                              [("Angel1",23), ("Angel1",22), ("Angel1",22)],
                              [("Angel1",22), ("Angel1",23), ("Angel1",23)],
                              
                              [("Angel1",24), ("Angel1",23)],
                              [("Angel1",25)]]
class TempleOfGod_2(GameState) :
    name = "Temple of God - 2"
    sound_bg = "Temple of God_SBG.mid"
    def __init__(self, display, heroTeam, hero_able_use, player, FPS=15) :
        self.wave_order = [-1, 3, 3, 2]
        GameState.__init__(self, display, heroTeam, hero_able_use, player, FPS) 
        self.map_img = pygame.image.load(self.imageRoot + "temple of god.png")
        self.kill_counter[1] = 8
        self.monster_order = [[("Angel2",23), ("Angel2",22), ("Angel2",22)],
                              [("Angel2",24), ("Angel2",23), ("Angel2",23)],
                              [("Angel2",24), ("Angel2",24), ("Angel2",23)],
                              
                              [("Angel2",25), ("Angel2",24), ("Angel2",24)],
                              [("Angel2",25), ("Angel2",24), ("Angel2",23)],
                              [("Angel2",26), ("Angel2",24)],
                              
                              [("Angel2",27), ("Angel2",26)],
                              [("Angel2",28), ("Angel2",27)]]
class TempleOfGod_3(GameState) :
    name = "Temple of God - 3"
    sound_bg = "Temple of God_SBG.mid"
    def __init__(self, display, heroTeam, hero_able_use, player, FPS=15) :
        self.wave_order = [-1, 3, 3, 2]
        GameState.__init__(self, display, heroTeam, hero_able_use, player, FPS)  
        self.map_img = pygame.image.load(self.imageRoot + "temple of god.png")
        self.kill_counter[1] = 8
        self.monster_order = [[("Angel3",25), ("Angel3",25), ("Angel3",25)],
                              [("Angel3",25), ("Angel3",26), ("Angel3",26)],
                              [("Angel3",26), ("Angel3",25), ("Angel3",25)],
                              
                              [("Angel3",27), ("Angel3",26), ("Angel3",26)],
                              [("Angel3",28), ("Angel3",27), ("Angel3",26)],
                              [("Angel3",27), ("Angel3",28), ("Angel3",29)],
                              
                              [("Angel3",29), ("Angel3",28), ("Angel3",28)],
                              [("Angel3",29), ("Angel3",29), ("Angel3",28)]]
class TempleOfGod_4(GameState) :
    name = "Temple of God - 4"
    sound_bg = "Temple of God_SBG.mid"
    def __init__(self, display, heroTeam, hero_able_use, player, FPS=15) :
        self.wave_order = [-1, 3, 3, 1]
        GameState.__init__(self, display, heroTeam, hero_able_use, player, FPS)    
        self.map_img = pygame.image.load(self.imageRoot + "temple of god.png")
        self.kill_counter[1] = 7
        self.monster_order = [[("Angel4",29), ("Angel3",29)],
                              [("Angel4",29), ("Angel2",29)],
                              [("Angel4",29), ("Angel2",29)],
                              
                              [("Angel4",30), ("Angel4",30)],
                              [("Angel4",30), ("Angel4",31)],
                              [("Angel4",31)],
                              
                              [("Angel4",35)]]
""" map 5 : Catacomb Frost """
class CatacombFrost_1(GameState) :
    name = "Catacomb Frost - 1"
    sound_bg = "Catacomb Frost_SBG.mid"
    def __init__(self, display, heroTeam, hero_able_use, player, FPS=15) :
        self.wave_order = [-1, 3, 3, 6]
        GameState.__init__(self, display, heroTeam, hero_able_use, player, FPS)  
        self.map_img = pygame.image.load(self.imageRoot + "catacomb frost.png")
        self.kill_counter[1] = 12
        self.monster_order = [[("Ghost1",27), ("Ghost2",28), ("Ghost3",28)],
                              [("Doll",27), ("BigSlime1",28), ("BigSlime1",28)],
                              [("Bat1",28), ("Bat2",29), ("Bat3",29)],
                              
                              [("Mushroom1",30), ("BigSlime3",31), ("Mushroom1",30)],
                              [("Mushroom1",31), ("BigSlime1",31), ("Mushroom1",32)],
                              [("Mushroom1",31), ("BigSlime2",32), ("BigSlime2",32)],
                              
                              [("Mushroom1",34)],
                              [("Doll",33)],
                              [("BigSlime3",34)],
                              [("BigSlime1",33)],
                              [("Bat1",34)],
                              [("Bat2",33)]]
        
class CatacombFrost_2(GameState) :
    name = "Ctacomb Frost - 2"
    sound_bg = "Catacomb Frost_SBG.mid"
    def __init__(self, display, heroTeam, hero_able_use, player, FPS=15) :
        self.wave_order = [-1, 3, 4, 6]
        GameState.__init__(self, display, heroTeam, hero_able_use, player, FPS) 
        self.map_img = pygame.image.load(self.imageRoot + "catacomb frost.png")
        self.kill_counter[1] = 13
        self.monster_order = [[("WolfGoblin",33), ("WolfGoblin",34)],
                              [("GreenGoblin",34), ("GreenGoblin",34)],
                              [("RedGoblin",35)],
                              
                              [("SkeletonKnight",35), ("SkeletonKnight",35)],
                              [("Zombie",36), ("Zombie",36), ("Zombie",37)],
                              [("Zombie",35), ("Zombie",35), ("Zombie",35)],
                              [("Zombie",37), ("Zombie",37), ("Zombie",37)],
                              
                              [("WolfGoblin",36)],
                              [("GreenGoblin",36)],
                              [("RedGoblin",37)],
                              [("SkeletonKnight",37)],
                              [("Zombie",37)],
                              [("SkeletonKing",37)]]
        
class CatacombFrost_3(GameState) :
    name = "Catacomb Frost - 3"
    sound_bg = "Catacomb Frost_SBG.mid"
    def __init__(self, display, heroTeam, hero_able_use, player, FPS=15) :
        self.wave_order = [-1, 2, 3, 1]
        GameState.__init__(self, display, heroTeam, hero_able_use, player, FPS)    
        self.map_img = pygame.image.load(self.imageRoot + "catacomb frost.png")
        self.kill_counter[1] = 6
        self.monster_order = [[("Wolf1",35), ("Wolf1",35), ("Wolf1",36)],
                              [("Wolf2",35), ("Wolf2",36), ("Wolf2", 36)],
                              
                              [("Giant",38), ("Wolf1",36), ("Wolf1",36)],
                              [("Giant",37), ("Wolf2",36), ("Wolf2",36)],
                              [("Giant",39), ("Wolf3",37), ("Wolf3",37)],
                              
                              [("Giant",42)]]
class CatacombFrost_4(GameState) :
    name = "Catacomb Frost - 4"
    sound_bg = "Catacomb Frost_SBG.mid"
    def __init__(self, display, heroTeam, hero_able_use, player, FPS=15) :
        self.wave_order = [-1, 3, 2, 1] 
        GameState.__init__(self, display, heroTeam, hero_able_use, player, FPS)  
        self.map_img = pygame.image.load(self.imageRoot + "catacomb frost.png")
        self.kill_counter[1] = 6
        self.monster_order = [[("Devil3",39), ("Zombie",38), ("Zombie",37)],
                              [("Devil4",40), ("Zombie",38), ("Zombie",38)],
                              [("Devil3",40), ("Zombie",38), ("Zombie",38)],
                              
                              [("Devil3",45)],
                              [("Devil4",45)],
                              
                              [("Devil2_Ice",47)]]
class CatacombFrost_5(GameState) :
    name = "Catacomb Frost - 5"
    sound_bg = "Catacomb Frost_SBG.mid"
    def __init__(self, display, heroTeam, hero_able_use, player, FPS=15) :
        self.wave_order = [-1, 4, 1, 1, 1, 1, 1, 1]
        GameState.__init__(self, display, heroTeam, hero_able_use, player, FPS)  
        self.map_img = pygame.image.load(self.imageRoot + "catacomb frost.png")
        self.kill_counter[1] = 10
        self.monster_order = [[("Devil3",40), ("Zombie",35), ("Zombie",35), ("Zombie",35)],
                              [("Devil3",40), ("Zombie",35), ("Zombie",35), ("Zombie",35)],
                              [("Devil4",40), ("SkeletonKnight",35), ("SkeletonKnight",35), ("SkeletonKnight",35)],
                              [("Devil4",40), ("SkeletonKnight",35), ("SkeletonKnight",35), ("SkeletonKnight",35)],
                              
                              [("BigSlime3",45)],
                              
                              [("SkeletonKing",46)],
                              
                              [("AquaElemental2",48)],
                              
                              [("Angel4",49)],
                              
                              [("Devil2_Ice",50)],
                              
                              [("Dracula",52)]]
""" map 6 : Vocanic Citadel """
class VocanicCitadel_1(GameState) :
    name = "Vocanic Citadel - 1"
    sound_bg = "Vocanic Citadel_SBG.mid"
    def __init__(self, display, heroTeam, hero_able_use, player, FPS=15) :
        self.wave_order = [-1, 3, 5, 2]        
        GameState.__init__(self, display, heroTeam, hero_able_use, player, FPS)  
        self.map_img = pygame.image.load(self.imageRoot + "vocanic citadel.png")
        self.kill_counter[1] = 10
        self.monster_order = [[("Cerberus",42), ("Wolf3",40), ("Wolf3",40)],
                              [("Cerberus",43), ("Wolf2",41), ("Wolf2",41)],
                              [("Cerberus",43), ("Wolf3",42), ("Wolf3",41)],
                              
                              [("Cerberus",44)],
                              [("Cerberus",44)],
                              [("Cerberus",45)],
                              [("Cerberus",45)],
                              [("Cerberus",47)],
                              
                              [("Cerberus",48)],
                              [("Cerberus",48)]]
        
class VocanicCitadel_2(GameState) :
    name = "Vocanic Citadel - 2"
    sound_bg = "Vocanic Citadel_SBG.mid"
    def __init__(self, display, heroTeam, hero_able_use, player, FPS=15) :
        self.wave_order = [-1, 3, 4]
        GameState.__init__(self, display, heroTeam, hero_able_use, player, FPS)      
        self.map_img = pygame.image.load(self.imageRoot + "vocanic citadel.png")
        self.kill_counter[1] = 7
        self.monster_order = [[("FireElemental2",46), ("FireElemental2",46)],
                              [("FireElemental2",47), ("FireElemental2",47)],
                              [("Soldier1",47), ("Soldier1",46), ("Soldier1",46)],
                              
                              [("Soldier1",48), ("Soldier1",47), ("Soldier1",47)],
                              [("Soldier1",48), ("Soldier1",47), ("Soldier1",47)],
                              [("Soldier2",49), ("Soldier1",48), ("Soldier1",47)],
                              [("FireElemental2",50)]]
                              
class VocanicCitadel_3(GameState) :
    name = "Vocanic Citadel - 3"
    sound_bg = "Vocanic Citadel_SBG.mid"
    def __init__(self, display, heroTeam, hero_able_use, player, FPS=15) :
        self.wave_order = [-1, 3, 3, 1]
        GameState.__init__(self, display, heroTeam, hero_able_use, player, FPS)    
        self.map_img = pygame.image.load(self.imageRoot + "vocanic citadel.png")
        self.kill_counter[1] = 7
        self.monster_order = [[("Soldier2",51), ("Soldier1",50), ("Soldier1",50), ("Soldier1",50)],
                              [("Soldier3",52), ("Soldier1",50), ("Soldier1",50), ("Soldier1",50)],
                              [("Soldier4",53), ("Soldier1",50), ("Soldier1",50), ("Soldier1",50)],
                              
                              [("Soldier2",52), ("Soldier2",52), ("Soldier2",52), ("Soldier2",52)],
                              [("Devil2",54), ("Soldier1",51), ("Soldier1",51)],
                              [("Devil2",55), ("Soldier1",51), ("Soldier1",51)],
                              
                              [("Devil2",58)]]
class VocanicCitadel_4(GameState) :
    name = "Vocanic Citadel - 4"
    sound_bg = "Vocanic Citadel_SBG.mid"
    def __init__(self, display, heroTeam, hero_able_use, player, FPS=15) :
        self.wave_order = [-1, 4, 5, 2]
        GameState.__init__(self, display, heroTeam, hero_able_use, player, FPS)    
        self.map_img = pygame.image.load(self.imageRoot + "vocanic citadel.png")
        self.kill_counter[1] = 11
        self.monster_order = [[("Soldier2",54), ("Soldier2",53), ("Soldier2", 53), ("Soldier2",53)],
                              [("Devil2",55), ("Devil2",54)],
                              [("Devil3",55), ("Devil3",55)],
                              [("Giant",56), ("Giant",55)],
                              
                              [("Devil2",58)],
                              [("SnakeDragon",58)],
                              [("SnakeDragon",58)],
                              [("SnakeDragon",59)],
                              [("SnakeDragon",59)],
                              
                              [("SnakeDragon",60)],
                              [("SnakeDragon",60)]]
class VocanicCitadel_5(GameState) :
    name = "Vocanic Citadel - 5"
    sound_bg = "Vocanic Citadel_SBG.mid"
    def __init__(self, display, heroTeam, hero_able_use, player, FPS=15) :
        self.wave_order = [-1, 4, 3, 1]
        GameState.__init__(self, display, heroTeam, hero_able_use, player, FPS)     
        self.map_img = pygame.image.load(self.imageRoot + "vocanic citadel.png")
        self.kill_counter[1] = 8
        self.monster_order = [[("SnakeDragon",60)],
                              [("SnakeDragon",60)],
                              [("Devil2",60)],
                              [("Devil3",60)],
                              
                              [("SnakeDragon",62)],
                              [("SnakeDragon",62)],
                              [("SnakeDragon",62)],
                              
                              [("Dragon",65)]]
""" map 7 : Lost Island """
class LostIsland_1(GameState) :
    name = "Lost Island - 1"
    sound_bg = "Lost Island_SBG.mid"
    def __init__(self, display, heroTeam, hero_able_use, player, FPS=15) :
        GameState.__init__(self, display, heroTeam, hero_able_use, player, FPS)      
class LostIsland_2(GameState) :
    name = "Lost Island - 2"
    sound_bg = "Lost Island_SBG.mid"
    def __init__(self, display, heroTeam, hero_able_use, player, FPS=15) :
        GameState.__init__(self, display, heroTeam, hero_able_use, player, FPS)      
class LostIsland_3(GameState) :
    name = "Lost Island - 3"
    sound_bg = "Lost Island_SBG.mid"
    def __init__(self, display, heroTeam, hero_able_use, player, FPS=15) :
        GameState.__init__(self, display, heroTeam, hero_able_use, player, FPS)      
class LostIsland_4(GameState) :
    name = "Lost Island - 4"
    sound_bg = "Lost Island_SBG.mid"
    def __init__(self, display, heroTeam, hero_able_use, player, FPS=15) :
        GameState.__init__(self, display, heroTeam, hero_able_use, player, FPS)      
class LostIsland_5(GameState) :
    name = "Lost Island - 5"
    sound_bg = "Lost Island_SBG.mid"
    def __init__(self, display, heroTeam, hero_able_use, player, FPS=15) :
        GameState.__init__(self, display, heroTeam, hero_able_use, player, FPS)      

""" class library """
windForest_lib = (5, WindForest_1, WindForest_2, WindForest_3, WindForest_4, WindForest_5)
forbiddenForest_lib = (5, ForbiddenForest_1, ForbiddenForest_2, ForbiddenForest_3, ForbiddenForest_4, ForbiddenForest_5)
fairyHill_lib = (4, FairyHill_1, FairyHill_2, FairyHill_3, FairyHill_4)
templeOfGod_lib = (4, TempleOfGod_1, TempleOfGod_2, TempleOfGod_3, TempleOfGod_4)
catacombFrost_lib = (5, CatacombFrost_1, CatacombFrost_2, CatacombFrost_3, CatacombFrost_4, CatacombFrost_5)
vocanicCitadel_lib = (5, VocanicCitadel_1, VocanicCitadel_2, VocanicCitadel_3, VocanicCitadel_4, VocanicCitadel_5)
lostIsland_lib = (5, LostIsland_1, LostIsland_2, LostIsland_3, LostIsland_4, LostIsland_5)
state_lib = [6, windForest_lib, forbiddenForest_lib, fairyHill_lib, templeOfGod_lib, catacombFrost_lib, vocanicCitadel_lib, lostIsland_lib]
