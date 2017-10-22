import pygame
from pygame.locals import *
pygame.init()
class StateInterface :
    imageRoot = "image\interface\\"
    Font = pygame.font.Font("font\OCRAEXT.TTF", 19)
    font_potion = pygame.font.Font("font\JS Noklae Normal.ttf", 24)
    def __init__(self, display, heroTeam, kill_counter, state_name, money, potion_counter, potions) :
        self.Display = display
        self.heroTeam = heroTeam
        self.leader = heroTeam[0]
        self.kill_counter = kill_counter
        self.state_name = state_name
        self.money = money
        self.potion_counter = potion_counter
        self.potions = potions
        
        self.leader_hp_w = 99
        self.leader_ap_w = 103
        self.leader_sp_w = 111
        self.member_hp_w = 68
        self.member_ap_w = 76
        self.state_w = 340
        self.potion_gauge_r = 72
        
        
        # load image
        self.icon_bg = pygame.image.load(self.imageRoot + "member_gauge-pic.png")
        self.member_gauge = pygame.image.load(self.imageRoot + "member_gauge-bar.png")
        self.leader_gauge = pygame.image.load(self.imageRoot + "leader_gauge-pic.png")
        self.state_gauge = pygame.image.load(self.imageRoot + "state_gauge.png")
        self.coin = pygame.image.load(self.imageRoot + "coin.png")
        self.potion_gauge = pygame.image.load(self.imageRoot + "potion_gauge.png")
        self.potion_gauge_full = pygame.image.load(self.imageRoot + "potion_gauge_full.png")
    def draw(self) :
        self.drawHeroGauge()
        self.drawStateGauge()
        self.drawMoney()
        self.drawPotionGauge()
    """ draw mrthod """
    def drawHeroGauge(self) :
        # draw leader interface
        pygame.draw.rect(self.Display, (0,0,0), (38,25,125,30))
        pygame.draw.rect(self.Display, (255,0,0), (54,28,self.calGaugeHp(self.leader),5))
        pygame.draw.rect(self.Display, (0,0,255), (50,38,self.calGaugeAp(self.leader),5))
        self.Display.blit(self.leader_gauge, (38,25))
        self.Display.blit(self.icon_bg, (0,0))
        self.Display.blit(self.leader.icon, (4,4))
        nameText = self.Font.render(self.leader.char_name, True, (255,255,255))
        self.Display.blit(nameText, (58,6))
        # draw member interface
        for i in range(1,len(self.heroTeam)) :
            hero = self.heroTeam[i]
            pygame.draw.rect(self.Display, (0,0,0), (42,30+64*i,90,22))
            pygame.draw.rect(self.Display, (255,0,0), (54,33+i*64,self.calGaugeHp(hero),5))
            pygame.draw.rect(self.Display, (0,0,255), (46,43+i*64,self.calGaugeAp(hero),5))
            self.Display.blit(self.member_gauge, (42,30+64*i))
            self.Display.blit(self.icon_bg, (0,64*i))
            self.Display.blit(hero.icon, (4,4+64*i))
            nameText = self.Font.render(hero.char_name, True, (255,255,255)) 
            self.Display.blit(nameText, (58,13+63*i))
    def drawStateGauge(self) :
        # draw state gauge
        pygame.draw.rect(self.Display, (0,0,0), (342,0,340,25))
        pygame.draw.rect(self.Display, (0,255,0), (342,0,self.calGaugeState(),25))
        self.Display.blit(self.state_gauge, (322,0))
        nameText = self.Font.render(self.state_name, True, (255,255,255))
        textRect = nameText.get_rect()
        textRect.centerx = 512
        self.Display.blit(nameText, textRect)        
    def drawMoney(self) :
        # draw money
        text = str(self.money[0])
        money_text = self.Font.render(text, True, (255,255,255))
        self.Display.blit(money_text, (900,10))
        self.Display.blit(self.coin, (865,10))        
    def drawPotionGauge(self) :
        potion1_text = self.font_potion.render(str(self.potions[1]), True, (255,255,255))
        potion2_text = self.font_potion.render(str(self.potions[2]), True, (255,255,255))
        potion3_text = self.font_potion.render(str(self.potions[3]), True, (255,255,255))
        potion4_text = self.font_potion.render(str(self.potions[4]), True, (255,255,255))
        rect_p1 = potion1_text.get_rect()
        rect_p2 = potion2_text.get_rect()
        rect_p3 = potion3_text.get_rect()
        rect_p4 = potion4_text.get_rect()
        rect_p1.center = (20,462)
        rect_p2.center = (74,462)
        rect_p3.center = (112,499)
        rect_p4.center = (117,555)
        
        # draw potion gauge
        pygame.draw.circle(self.Display, (59,59,59), (46,532), 72)
        pygame.draw.circle(self.Display, (255,0,0), (46,532), self.calGaugePotion())
        if self.potion_counter[0] >= self.potion_counter[1] :
            self.Display.blit(self.potion_gauge_full, (0,443))        
        else :
            self.Display.blit(self.potion_gauge, (0,443))        
        self.Display.blit(potion1_text, rect_p1)
        self.Display.blit(potion2_text, rect_p2)
        self.Display.blit(potion3_text, rect_p3)
        self.Display.blit(potion4_text, rect_p4)
    """ calculate method """
    def calGaugeHp(self, hero) :
        if hero is self.leader :
            return hero.hp * self.leader_hp_w // hero.Hp
        return hero.hp * self.member_hp_w // hero.Hp
    def calGaugeAp(self, hero) :
        if hero is self.leader :
            return hero.ac_spd * self.leader_ap_w // hero.a_spd
        return hero.ac_spd * self.member_ap_w // hero.a_spd
    def calGaugeState(self) :
        return self.kill_counter[0] * self.state_w // self.kill_counter[1]
    def calGaugePotion(self) :
        return self.potion_counter[0] * self.potion_gauge_r // self.potion_counter[1]
    
                                                
        