import pygame, sys, os
import ClassCharacter as CC
from pygame.locals import *
pygame.init()
class GameOver :
    def __init__(self, display, player, FPS=15) :
        self.Display = display
        self.FPS = FPS
        self.player = player
        self.FPSclock = pygame.time.Clock()
        self.gameover_img = pygame.image.load("image\scence\game over_img.png")
    def run(self) :
        pygame.mixer.music.load("sounds\SBG\Game Over_SBG.mid")
        pygame.mixer.music.play(1,0.0)
        while True :
            self.Display.blit(self.gameover_img, (0,0))
            for e in pygame.event.get() :
                if e.type == QUIT :
                    self.player.encode()
                    pygame.quit()
                    sys.exit()
                elif e.type == KEYDOWN :
                    if e.key == K_p and self.player.money >= 500 :
                        self.player.money -= 500
                        return "again"        # play again
                    if e.key == K_o :
                        return "back"        # back
                elif e.type == MOUSEBUTTONDOWN :
                    x,y = e.pos
                    if 353 <= y <= 451 :
                        if 183 <= x <= 438 :
                            return "back"
                        if 587 <= x <= 842 and self.player.money >= 500 :
                            self.player.money -= 500
                            return "again"
            pygame.display.update()
            self.FPSclock.tick(self.FPS)

class Complete :
    def __init__(self, display, player, FPS=15) :
        self.Display = display
        self.FPS = FPS
        self.player = player
        self.FPSclock = pygame.time.Clock()
        self.complete_img = pygame.image.load("image\scence\complete_img.png")
    def run(self) :
        pygame.mixer.music.load("sounds\SBG\Complete_SBG.mid")
        pygame.mixer.music.play(1,0.0)        
        while True :
            self.Display.blit(self.complete_img, (0,0))
            for e in pygame.event.get() :
                if e.type == QUIT :
                    self.player.encode()
                    pygame.quit()
                    sys.exit()
                elif e.type == KEYDOWN :
                    if e.key == K_p :
                        return "next"   # next state level
                    elif e.key == K_o :
                        return "back"   # back to select map
                elif e.type == MOUSEBUTTONDOWN :
                    x,y = e.pos
                    if 353 <= y <= 451 :
                        if 183 <= x <= 438 :
                            return "back"
                        if 587 <= x <= 842 :
                            return "next"
            pygame.display.update()
            self.FPSclock.tick(self.FPS)
            
class SelectState :
    imageRoot = "image\scence\\"
    
    def __init__(self, display, player, FPS=15) :
        self.Display = display
        self.FPS = FPS
        self.FPSclock = pygame.time.Clock()
        self.player = player
        self.state_unlock = player.state_unlock
        self.bg = pygame.image.load(self.imageRoot + "select state_BG.png")
        self.frame = pygame.image.load(self.imageRoot + "select state_frame.png")
        self.maps = [0]*7
        self.maps_lock = [0]*7
        for i in range(7) :
            self.maps[i] = pygame.image.load(self.imageRoot + "map" + str(i+1) + ".png")
            self.maps_lock[i] = pygame.image.load(self.imageRoot + "map" + str(i+1) + "_lock" + ".png")
    def run(self) :
        # draw background
        self.Display.blit(self.bg, (0,0))
        if self.state_unlock["map1"] :
            self.Display.blit(self.maps[0], (95,100))
        else :
            self.Display.blit(self.maps_lock[0], (95,100))
        if self.state_unlock["map2"] :
            self.Display.blit(self.maps[1], (190,300))
        else :
            self.Display.blit(self.maps_lock[1], (190,300))
        if self.state_unlock["map3"] :
            self.Display.blit(self.maps[2], (330,100))
        else :
            self.Display.blit(self.maps_lock[2], (330,100))
        if self.state_unlock["map4"] :
            self.Display.blit(self.maps[3], (450,300))
        else :
            self.Display.blit(self.maps_lock[3], (450,300))
        if self.state_unlock["map5"] :
            self.Display.blit(self.maps[4], (585,100))
        else :
            self.Display.blit(self.maps_lock[4], (585,100))
        if self.state_unlock["map6"] :
            self.Display.blit(self.maps[5], (680,300))
        else :
            self.Display.blit(self.maps_lock[5], (680,300))
        if self.state_unlock["map7"] :
            self.Display.blit(self.maps[6], (805,100))
        else :
            self.Display.blit(self.maps_lock[6], (805,100))
        self.Display.blit(self.frame, (0,0))  
        # play music
        pygame.mixer.music.load("sounds\SBG\SelectState_SBG.mid")
        pygame.mixer.music.play(-1,0.0)
        while True :           
            for e in pygame.event.get() :
                if e.type == QUIT :
                    self.player.encode()
                    pygame.quit()
                    sys.exit()
                elif e.type == MOUSEBUTTONDOWN :
                    x,y = e.pos
                    if 100 <= y <= 320 :
                        if 95 <= x <= 260 and self.state_unlock["map1"] :
                            return 1
                        elif 330 <= x <= 495 and self.state_unlock["map3"] :
                            return 3
                        elif 585 <= x <= 750 and self.state_unlock["map5"] :
                            return 5
                        elif 805 <= x <= 970 and self.state_unlock["map7"] :
                            return 7
                    elif 300 <= y <= 520 :
                        if 190 <= x <= 355 and self.state_unlock["map2"] :
                            return 2
                        elif 450 <= x <= 615 and self.state_unlock["map4"] :
                            return 4
                        elif 680 <= x <= 845 and self.state_unlock["map6"] :
                            return 6
                    elif x <= 130 and y >= 485 :
                        return "back"
            pygame.display.update()
            self.FPSclock.tick(self.FPS)
            
class SelectCharacter :
    imageRoot = "image\scence\\"
    hero_icon_pos = {"Lancer":(100,505), "Paladin":(164,505), "Mage":(228,505), "Elf-Ranger":(292,505), "Elemental-Master":(356,505), "Magnus":(420,505)}
    font_price = pygame.font.Font("font\JS Noklae Normal.ttf", 97)
    font_status = pygame.font.Font("font\JS Noklae Normal.ttf", 63)
    font_exp = pygame.font.Font("font\JS Noklae Normal.ttf", 36)
    font_name = pygame.font.Font("font\OLDENGL.TTF", 63)
    font_potion = pygame.font.Font("font\JS Noklae Normal.ttf", 24)
    def __init__(self, display, player, FPS=15) :
        # initial setup
        self.Display = display
        self.FPS = FPS
        self.FPSclock = pygame.time.Clock()
        self.player = player
        self.selected = "Lancer"
        # load image
        self.img_bg = pygame.image.load(self.imageRoot + "select character_BG.png")
        self.status_bg = pygame.image.load(self.imageRoot + "status_bg.png")
        self.select_ring = pygame.image.load(self.imageRoot + "select_hero.png")
        self.money_slot = pygame.image.load(self.imageRoot + "money slot.png")
        self.exp_gauge = pygame.image.load(self.imageRoot + "exp_gauge.png")
        self.unlock_btn = pygame.image.load(self.imageRoot + "select character_unlock_btn.png")
        self.potion_sale = pygame.image.load(self.imageRoot + "potion_sale.png")
    def run(self) :
        # play music bg
        pygame.mixer.music.load("sounds\SBG\SelectCharacter_SBG.mid")
        pygame.mixer.music.play(-1,0.0)        
        while True :
            self.Display.blit(self.img_bg, (0,0))
            self.drawIcon()
            self.drawSelected()
            self.drawStatus()
            self.drawMoney()
            self.drawPotionSale()
            
            for e in pygame.event.get() :
                if e.type == MOUSEBUTTONDOWN :
                    x,y = e.pos 
                    if 505 <= y <= 561 :
                        if 100 <= x <= 156 :
                            self.selected = "Lancer"
                        elif 164 <= x <= 220 :
                            self.selected = "Paladin"
                        elif 228 <= x <= 284 :
                            self.selected = "Mage"
                        elif 292 <= x <= 348 :
                            self.selected = "Elf-Ranger"
                        elif 356 <= x <= 412 :
                            self.selected = "Elemental-Master"
                        elif 420 <= x <= 476 :
                            self.selected = "Magnus"
                    if (900 <= x <= 990) and (490 <= y <= 555) :
                        if self.player.hero_unlock[self.selected] :
                            return self.generate()
                    if 225 <= x <= 394 and 310 <= y <= 368 and  not self.player.hero_unlock[self.selected] :
                        self.unlockHero()
                    if 48 <= x <= 70 :
                        if 205 <= y <= 228 and self.player.money >= 30 :
                            self.player.money -=  30
                            self.player.hp_potions[1] += 1
                        elif 250 <= y <= 273 and self.player.money >= 50 :
                            self.player.money -=  50
                            self.player.hp_potions[2] += 1
                        elif 295 <= y <= 318 and self.player.money >= 100 :
                            self.player.money -=  100
                            self.player.hp_potions[3] += 1                            
                        elif 340 <= y <= 363 and self.player.money >= 150 :
                            self.player.money -=  150
                            self.player.hp_potions[4] += 1                            
                    
                elif e.type == QUIT :
                    self.player.encode()
                    pygame.quit()
                    sys.exit()
            pygame.display.update()
            self.FPSclock.tick(self.FPS)
    def drawMoney(self) :
        self.Display.blit(self.money_slot, (0,75))
        money_text = self.font_exp.render(str(self.player.money), True, (255,255,255))
        self.Display.blit(money_text, (30,68))
    def drawSelected(self) :
        self.Display.blit(self.select_ring, self.hero_icon_pos[self.selected])
        self.Display.blit(CC.hero_lib[self.selected].img, (180,50))
        name_text = self.font_name.render(CC.hero_lib[self.selected].char_name, True, (255,255,255))
        name_rect = name_text.get_rect()
        name_rect.center = (325, 450)
        self.Display.blit(name_text, name_rect)
        if not self.player.hero_unlock[self.selected] :
            self.drawSale()
    def drawSale(self) :
        price = "$" + str(CC.hero_lib[self.selected].price)
        price_text = self.font_price.render(price, True, (255,255,255))
        price_rect = price_text.get_rect()
        price_rect.center = (340,277)
        self.Display.blit(self.unlock_btn, (255,310))
        self.Display.blit(price_text, price_rect)
    def unlockHero(self) :
        price = CC.hero_lib[self.selected].price
        if price <= self.player.money :
            self.player.money -= price
            self.player.hero_unlock[self.selected] = True
    def drawIcon(self) :
        if self.player.hero_unlock["Lancer"] :
            self.Display.blit(CC.Lancer.icon, (104,509))
        else :
            self.Display.blit(CC.Lancer.icon_lock, (104,509))
        if self.player.hero_unlock["Paladin"] :
            self.Display.blit(CC.Paladin.icon, (168, 509))
        else :
            self.Display.blit(CC.Paladin.icon_lock, (168, 509))
        if self.player.hero_unlock["Mage"] :
            self.Display.blit(CC.Mage.icon, (232, 509))
        else :
            self.Display.blit(CC.Mage.icon_lock, (232, 509))
        if self.player.hero_unlock["Elf-Ranger"] :
            self.Display.blit(CC.ElfRanger.icon, (296, 509))
        else :
            self.Display.blit(CC.ElfRanger.icon_lock, (296, 509))
        if self.player.hero_unlock["Elemental-Master"] :
            self.Display.blit(CC.ElementalMaster.icon, (360, 509))
        else :
            self.Display.blit(CC.ElementalMaster.icon_lock, (360,509))
        if self.player.hero_unlock["Magnus"] :
            self.Display.blit(CC.Magnus.icon, (424, 509))
        else :
            self.Display.blit(CC.Magnus.icon_lock, (424, 509))
    def drawStatus(self) :
        self.Display.blit(self.status_bg, (577,148))
        (Atk, Def, Hp) = CC.hero_lib[self.selected].calStatus()
        m_spd = 15 / CC.hero_lib[self.selected].m_spd
        a_spd = 15 / CC.hero_lib[self.selected].a_spd
        level = CC.hero_lib[self.selected].level
        Atk_text = self.font_status.render("ATK  " + str(Atk), True, (255,255,255))
        Def_text = self.font_status.render("DEF  " + str(Def), True, (255,255,255))
        Hp_text = self.font_status.render("Hp   " + str(Hp), True, (255,255,255))
        M_spd_text = self.font_status.render("Move spd  %.2f"%(m_spd), True, (255,255,255))
        A_spd_text = self.font_status.render("Attack spd  %.2f"%(a_spd), True, (255,255,255))
        level_text = self.font_status.render("Lv." + str(level), True, (255,255,255))
        self.Display.blit(level_text, (565,70))
        self.Display.blit(Atk_text, (600,150))
        self.Display.blit(Def_text, (600,200))
        self.Display.blit(Hp_text, (600,250))
        self.Display.blit(M_spd_text, (600,300))
        self.Display.blit(A_spd_text, (600,350))
        self.drawExp()
    def drawExp(self) :
        exp = CC.hero_lib[self.selected].exp
        max_exp = CC.hero_lib[self.selected].max_exp
        # generate text
        text = "exp.(%d/%d)"%(exp, max_exp)
        exp_text = self.font_exp.render(text, True, (255,255,255))
        exp_text_rect = exp_text.get_rect()
        exp_text_rect.topright = (955,110)
        exp_gw = (exp * 290) // max_exp     # exp gauge width
        # blit
        pygame.draw.rect(self.Display, (0,0,0), (680,85,290,23))
        pygame.draw.rect(self.Display, (0,255,0), (681,85,exp_gw,23))
        self.Display.blit(self.exp_gauge, (680,85))
        self.Display.blit(exp_text, exp_text_rect)
    def drawPotionSale(self) :
        self.Display.blit(self.potion_sale, (0,160))
        potion_amounts = [0]*5
        for i in range(1,5) :
            potion_amounts[i] = self.player.hp_potions[i]
            amount_text = self.font_potion.render(str(potion_amounts[i]), True, (255,255,255))
            self.Display.blit(amount_text, (20, 45*i + 157))
    def generate(self) :
        leader = CC.hero_lib[self.selected]()
        leader.leader = True
        hero_team = [leader]
        hero_able_use = []
        self.player.hero_unlock[self.selected] = False # fake set
        for hero in self.player.hero_unlock.keys() :
            if self.player.hero_unlock[hero] :
                hero_able_use.append(hero)
        self.player.hero_unlock[self.selected] = True
        return (hero_team, hero_able_use)

class StartScence :
    imageRoot = "image\scence\\"
    fileRoot = "file\\"
    font_new = pygame.font.Font("font\JS Noklae Normal.ttf", 45)
    def __init__(self, display, FPS=15) :
        # display initialize
        self.Display = display
        self.FPS = FPS
        self.FPSclock = pygame.time.Clock()
        # load img
        self.img_bg = pygame.image.load(self.imageRoot + "menu_BG.png")
        self.all_btn = pygame.image.load(self.imageRoot + "menu_all_btn.png")
        self.new_interface = pygame.image.load(self.imageRoot + "menu_new_interface.png")
        self.new_used_img = pygame.image.load(self.imageRoot + "menu_new_used.png")
        self.load_interface = pygame.image.load(self.imageRoot + "menu_load_interface.png")
        self.normal_full_img = pygame.image.load(self.imageRoot + "menu_normal_full.png")
        self.normal_empty_img = pygame.image.load(self.imageRoot + "menu_normal_empty.png")
        self.how_bg = pygame.image.load(self.imageRoot + "menu_how_bg.png")
        how_p1 = pygame.image.load(self.imageRoot + "menu_how_p1.png")
        how_p2 = pygame.image.load(self.imageRoot + "menu_how_p2.png")
        how_p3 = pygame.image.load(self.imageRoot + "menu_how_p3.png")
        how_p4 = pygame.image.load(self.imageRoot + "menu_how_p4.png")
        how_p5 = pygame.image.load(self.imageRoot + "menu_how_p5.png")
        how_p6 = pygame.image.load(self.imageRoot + "menu_how_p6.png")
        self.how_pages = [0, how_p1, how_p2, how_p3, how_p4, how_p5, how_p6]
        self.how_select = 1
    
        # scence initial
        self.state = "normal"
        self.end_scence = False
        self.select_file = ""
        # new state initialize
        self.text_new = ""
        self.new_used = False
        # load state initialize
        self.loadFileName()
        # normal state initialize
        self.normal_empty = False
        self.normal_full = False
        if len(self.files) == 0 :
            self.normal_empty = True
        elif len(self.files) == 5 :
            self.normal_full = True
    def run(self) :
        pygame.mixer.music.load("sounds\SBG\StartMenu_SBG.mid")
        pygame.mixer.music.play(-1,0.0)                
        while True :
            if self.end_scence :
                return self.select_file
            self.Display.blit(self.img_bg, (0,0))
            if self.normal_empty :
                self.Display.blit(self.normal_empty_img, (429,520))
            elif self.normal_full :
                self.Display.blit(self.normal_full_img, (429,520))
                
            if self.state == "normal" :
                self.run_Normal()
            elif self.state == "new"  :
                self.run_New() 
            elif self.state == "load" :
                self.run_Load()
            elif self.state == "how" :
                self.run_How()
            pygame.display.update()
            self.FPSclock.tick(self.FPS)
    def loadFileName(self) :
        self.files = []
        for file in os.listdir(self.fileRoot) :
            self.files.append(file)
    def run_Normal(self) :
        self.Display.blit(self.all_btn, (410,330))
        for e in pygame.event.get() :
            if e.type == QUIT :
                pygame.quit()
                sys.exit()
            elif e.type == MOUSEBUTTONDOWN :
                x,y = e.pos
                if 410 <= x <= 606 :
                    if 330 <= y <= 390 and not self.normal_full :
                        self.state =  "new"
                    elif 390 <= y <= 452 and not self.normal_empty :
                        self.state = "load"
                    elif 455 <= y <= 515 :
                        self.state = "how"
    def run_New(self) :
        self.Display.blit(self.new_interface, (281,349))
        text = self.font_new.render(self.text_new, True, (0,0,0))
        self.Display.blit(text, (424,368))
        if self.new_used :
            self.Display.blit(self.new_used_img, (356,519))
        for e in pygame.event.get() :
            if e.type == QUIT :
                pygame.quit()
                sys.exit()
            elif e.type == MOUSEBUTTONDOWN :
                x,y = e.pos
                if 436 <= y <= 481 :
                    if 555 <= x <= 676 :
                        self.state = "normal" 
                    if 354 <= x <= 474 and len(self.text_new) > 0 :
                        self.generateNewFile()
            elif e.type == KEYDOWN :
                if e.unicode.isalnum() and len(self.text_new) < 10 :
                    self.text_new += e.unicode
                if e.key == K_BACKSPACE :
                    self.text_new = self.text_new[:-1]
    def generateNewFile(self) :
        if self.text_new + ".csv" in self.files :
            self.new_used = True
            return 
        new_file = open(self.fileRoot + self.text_new + ".csv", "a+")
        lines = ["money,300\n",
                 "potion,5,0,0,0\n",
                 "state_unlock_key,map1,map2,map3,map4,map5,map6,map7\n",
                 "state_unlock_value,True,False,False,False,False,False,False,\n",
                 "hero_unlock_key,Paladin,Lancer,Elf-Ranger,Mage,Elemental-Master,Magnus\n",
                 "hero_unlock_value,True,True,False,False,False,False\n",
                 "Paladin,1,0\n",
                 "Lancer,1,0\n",
                 "Elf-Ranger,1,0\n",
                 "Mage,1,0\n",
                 "Elemental-Master,1,0\n",
                 "Magnus,1,0\n"]
        new_file.writelines(lines)
        new_file.close()
        self.select_file = self.text_new + ".csv"
        self.end_scence = True
    def run_Load(self) :
        self.Display.blit(self.load_interface, (373,275))
        for i in range(len(self.files)) :
            text = self.font_new.render(self.files[i][:-4], True, (0,0,0))
            self.Display.blit(text, (400, 285 + i*38))
        for e in pygame.event.get() :
            if e.type == QUIT :
                pygame.quit()
                sys.exit()
            elif e.type == MOUSEBUTTONDOWN :
                x,y = e.pos
                if 460 <= x <= 522 :
                    if 484 <= y <= 518 :
                        self.state = "normal"
                if 392 <= x <= 618 :
                    if 294 <= y <= 327 and len(self.files) > 0:
                        self.select_file = self.files[0]
                        self.end_scence = True
                    elif 332 <= y <= 365 and len(self.files) > 1 :
                        self.select_file = self.files[1]
                        self.end_scence = True
                    elif 370 <= y <= 403 and len(self.files) > 2 :
                        self.select_file = self.files[2]
                        self.end_scence = True
                    elif 408 <= y <= 441 and len(self.files) > 3 :
                        self.select_file = self.files[3]
                        self.end_scence = True
                    elif 446 <= y <= 479 and len(self.files) > 4 :
                        self.select_file = self.files[4]
                        self.end_scence = True
    def run_How(self) :
        self.Display.blit(self.how_bg, (190,246))
        self.Display.blit(self.how_pages[self.how_select], (190,246))
        for e in pygame.event.get() :
            if e.type == QUIT :
                pygame.quit()
                sys.exit()
            if e.type == MOUSEBUTTONDOWN :
                x,y = e.pos
                if 379 <= y <= 414 :
                    if 200 <= x <= 222 and self.how_select > 1 :
                        self.how_select -= 1
                    elif 805 <= x <= 823 and self.how_select < 6 :
                        self.how_select += 1
                if 794 <= x <= 821 and 258 <= y <= 285 :
                    self.state = "normal"
                if 516 <= y <= 531 :
                    if 441 <= x <= 456 :
                        self.how_select = 1
                    elif 446 <= x <= 481 :
                        self.how_select = 2
                    elif 492 <= x <= 507 :
                        self.how_select = 3
                    elif 517 <= x <= 532 :
                        self.how_select = 4
                    elif 543 <= x <= 558 :
                        self.how_select = 5
                    elif 568 <= x <= 583 :
                        self.how_select = 6