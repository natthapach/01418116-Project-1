import pygame, math
pygame.init()
class Damage :
    colors = {"Monster":(0,0,255), "Hero":(255,0,0), "Heal":(0,255,0)}
    fontObj = pygame.font.Font("font\OLDENGL.TTF", 25)
    obj_type = "Damage"
    def __init__(self, type, dmg, base_pos) :
        self.color = self.colors[type]
        self.dmg = str(dmg)
        self.figure = self.generate()
        self.x, self.y = base_pos
        self.y  = self.y - (self.figure.get_height())
        self.expire = False
        self.expire_time = 15
        self.ec_spd = 0      # expire speed counter
    def generate(self) :
        base = self.fontObj.render(self.dmg, True, self.color)
        border = self.fontObj.render(self.dmg, True, (0,0,0))
        text = pygame.Surface((base.get_width()+2, base.get_height()+2))
        text.fill((255,255,255))
        text.blit(border, (0,0))
        text.blit(border, (0,2))
        text.blit(border, (2,2))
        text.blit(border, (2,0))
        text.blit(base, (1,1))
        text.set_colorkey((255,255,255))
        return text
    def receiveFrame(self) :
        self.ec_spd += 1
        if self.ec_spd >= self.expire_time :
            self.expire = True
        self.x += 2
        self.y -= 2
        
class Attack:
    imageRoot = "image\\attack\\"
    soundRoot = "sounds\SFX\\"
    obj_type = "Attack"
    have_sound = False
    def __init__(self, atk, target, x, y, holding):
        self.atk = atk
        self.target = target
        self.x = x
        self.y = y
        self.holding = holding  #field holding
        self.figure = None
        self.f_spd = 1    #figure speed
        self.fc_spd = 0     #figure speed counter
        self.expire = False
    def setFigure(self):
        pass
    def damage(self, target) :
        dmg = self.atk - target.Def
        if dmg < 0 :
            dmg = 0
        target.hp -= dmg
        self.active = False
        return  Damage(target.obj_type, dmg, target.getDisplayPos())
    def loadChar(self) :
        self.char_ls = [0] * self.expire_time
        for i in range(self.expire_time) :
            self.char_ls[i] = pygame.image.load(self.imageRoot + self.char_name + "_" + "%02d.png"%(i+1))
        self.figure = pygame.transform.rotate(self.char_ls[0], self.degree)   
    def __repr__(self) :
        return self.char_name
class Melee(Attack) :
    # the close distant attack
    # have 1 phase 1.damage phase
    expire_time = 5     # defualt expire_time
    def __init__(self, atk, target, x, y, holding, degree):
        Attack.__init__(self, atk, target, x, y, holding)
        self.degree = degree
        self.active = True
        self.loadChar()
        if self.have_sound :
            self.sfx.play()
    def receiveFrame(self):
            self.fc_spd += 1
            if self.fc_spd >= self.expire_time :
                self.expire = True
            else :
                self.setFigure()    
    def setFigure(self):
        self.figure = pygame.transform.rotate(self.char_ls[self.fc_spd // self.f_spd], self.degree)
        
        
class Range(Attack) :
    def __init__(self, atk, target, start_x, start_y, goal_x, goal_y, end_x, end_y, holding) :
        Attack.__init__(self, atk, target, start_x, start_y, holding)
        self.goal_x = goal_x
        self.goal_y = goal_y
        self.start_x = start_x
        self.start_y = start_y
        self.end_x = end_x
        self.end_y = end_y
        self.dx = self.goal_x - self.start_x
        self.dy = self.goal_y - self.start_y
        self.m_spd = max(abs(self.dx), abs(self.dy)) // 32 * 4
        self.mc_spd = 0        
        self.calDegree()
        self.active = False
        self.loadChar()
        self.figure = pygame.image.load(self.imageRoot + self.char_name + "_move.png")
        self.figure = pygame.transform.rotate(self.figure, self.degree)
    def receiveFrame(self) :
        if self.mc_spd < self.m_spd :
            # in first phase : movement phase
            self.move()
            self.mc_spd += 1
        elif self.mc_spd == self.m_spd :
            # end first and start second phase
            self.active = True
            self.x = self.end_x
            self.y = self.end_y
            self.setFigure()
            self.mc_spd += 1
            if self.have_sound :
                self.sfx.play()
        else :
            # in second phase : active phase
            self.fc_spd += 1
            if self.fc_spd >= self.expire_time :
                self.expire = True
            self.setFigure() 
    def setFigure(self):
        try :
            self.figure = self.char_ls[self.fc_spd // self.f_spd]
        except :
            pass      
    def calDegree(self) :
        if self.dx > 0 :
            if self.dy > 0 :    # Q'4
                self.degree = -(math.fabs(math.degrees(math.atan(self.dy/self.dx))) + 90)
                # degree = -(|arctan(dy/dx)| + 90)
            elif self.dy < 0 :  # Q'1
                self.degree = -(math.fabs(math.degrees(math.atan(self.dx/self.dy))))
                # degree = -|arctan(dx/dy)|
            else :
                self.degree = -90
        elif self.dx < 0 :
            if self.dy > 0 :    # Q'3
                self.degree = (math.fabs(math.degrees(math.atan(self.dy/self.dx))) + 90)
                # degree = |arctan(dy/dx)| + 90
            elif self.dy < 0 :  # Q'2
                self.degree = (math.fabs(math.degrees(math.atan(self.dx/self.dy))))
                # degree = |arctan(dx/dy)|
            else :
                self.degree = 90
        else :
            if self.dy > 0 :
                self.degree = 180
            if self.dy < 0 :
                self.degree = 0
    def move(self) :
        self.x += self.dx / self.m_spd
        self.y += self.dy / self.m_spd
class Range_extra(Attack) :
    def __init__(self, atk, target, start_x, start_y, goal_x, goal_y, holding) :
        x = start_x * 32
        y = start_y * 32
        Attack.__init__(self, atk, target, x, y, holding)
        self.start_x = start_x
        self.start_y = start_y
        self.goal_x = goal_x
        self.goal_y = goal_y
        self.current_x = start_x
        self.current_y = start_y
        self.calDegree()
        self.active = True
        self.crush = False
        self.loadChar()
    def loadChar(self) :
        char_m = pygame.image.load(self.imageRoot + self.char_name + "_move.png")
        self.figure = self.figure = pygame.transform.rotate(char_m, self.degree)
        self.char_ls = [0] * self.expire_time
        for i in range(self.expire_time) :
            self.char_ls[i] = pygame.image.load(self.imageRoot + self.active_name + "_%02d"%(i+1) + ".png")
    def calDegree(self) :
        dx = self.goal_x - self.start_x
        dy = self.goal_y - self.start_y
        if dx > 0 :
            if dy > 0 :
                self.degree = -135
                self.changer_x = +1
                self.changer_y = +1
            elif dy < 0 :
                self.degree = -45
                self.changer_x = +1
                self.changer_y = -1
            else :
                self.degree =  -90
                self.changer_x = +1
                self.changer_y = 0
        elif dx < 0 :
            if dy > 0 :
                self.degree = 135
                self.changer_x = -1
                self.changer_y = +1
            elif dy < 0 :
                self.degree = 45
                self.changer_x = -1
                self.changer_y = -1
            else :
                self.degree = 90
                self.changer_x = -1
                self.changer_y = 0
        else :
            if dy > 0 :
                self.degree = 180
                self.changer_x = 0
                self.changer_y = +1
            elif dy < 0 :
                self.degree  = 0
                self.changer_x = 0
                self.changer_y = -1
    def receiveFrame(self) :
        if (self.current_x == self.goal_x and self.current_y == self.goal_y and not self.crush) or (self.fc_spd >= self.expire_time) :
            self.expire = True 
        if not self.crush :
            self.current_x += self.changer_x
            self.current_y += self.changer_y
            self.holding = [(self.current_x, self.current_y)]
            self.x = self.current_x * 32
            self.y = self.current_y * 32            
        if self.crush :
            self.fc_spd += 1
        self.setFigure()
    def setFigure(self) :
        if not self.crush :
            self.figure = self.figure
        else :
            try :
                self.figure = self.char_ls[self.fc_spd // self.f_spd]
            except :
                pass   
    def damage(self, other) :
        if not self.crush :
            self.crush = True
            x = self.current_x
            y = self.current_y
            self.holding = ((x,y-1), (x,y+1), (x-1,y), (x,y), (x+1,y))
            self.x = (x-1) * 32
            self.y = (y-1) * 32
            if self.have_sound :
                self.sfx.play()
            return
                
        return Attack.damage(self, other)
        
""" Melee Attack class """
""" Concrete Attack class """
class Sword1(Melee):
    char_name = "sword1"
class Sword2(Melee) :
    char_name = "Sword2"
    expire_time = 4
    have_sound = True
    sfx = pygame.mixer.Sound("sounds\SFX\Sword2.ogg")
class Lance1(Melee) :
    char_name = "lance1"
    have_sound = True
    sfx = pygame.mixer.Sound("sounds\SFX\Lance1.ogg")
class Lance2(Melee) :
    char_name = "lance1"
class Attack2(Melee) :
    char_name = "Attack2"
class Claw1(Melee) :
    char_name = "Claw1"
class Impact1(Melee) :
    char_name = "Impact1"
class Poision1(Melee) :
    char_name = "Poision1"
class Poision2(Melee) :
    char_name = "Poision2"
class Ghost1(Melee) :
    char_name = "Ghost1"
    expire_time = 4
class DeathMark(Melee) :
    char_name = "DeathMark"
class Hole1(Melee) :
    char_name = "Hole1"
class Xcross1(Melee) :
    char_name = "Xcross1"
class Xcross2(Melee) :
    char_name = "Xcross2"
    expire_time = 6
class Fire1(Melee) :
    char_name = "Fire1"
class Wind1(Melee) :
    char_name = "Wind1"
class Earth1(Melee) :
    char_name = "Earth1"
    expire_time = 4
class Aqua2(Melee) :
    char_name = "Aqua2"
    expire_time = 4
class Aqua1(Melee) :
    char_name = "Aqua1"
    expire_time = 9
class AngelAttack1(Melee) :
    char_name = "AngelAttack1"
    expire_time = 6
class AngelAttack2(Melee) :
    char_name = "AngelAttack2"
class Earth2(Melee) :
    char_name = "Earth2"
    expire_time = 7
class ClawFire(Melee) :
    char_name = "ClawFire"
class Ice1(Melee) :
    char_name = "Ice1"
    expire_time = 8
class Tornado1(Melee) :
    char_name = "Tornado1"
    expire_time = 8
class Soul2(Melee) :
    char_name = "Soul2"
    expire_time = 7
class Thunder2(Melee) :
    char_name = "Thunder2"
    expire_time = 8
class Bomb5(Melee) :
    char_name = "Bomb5"
    expire_time = 7
class Meteorite1(Melee) :
    char_name = "Meteorite1"
    expire_time = 11
class BlackHole1(Melee) :
    char_name = "BlackHole1"
    expire_time = 8
    have_sound = True
    sfx = pygame.mixer.Sound("sounds\SFX\BlackHole.ogg")

""" Range Attack class """
class Bomb1(Range) :
    char_name = "Bomb1"
    expire_time = 5
    have_sound = True
    sfx = pygame.mixer.Sound("sounds\SFX\Bomb1.ogg")
class Bomb2(Range) :
    char_name = "Bomb1"
    expire_time = 5
class Bubble1(Range) :
    char_name = "bubble1"
    expire_time = 5
class Bubble2(Range) :
    char_name = "bubble2"
    expire_time = 5
class Bubble3(Range) :
    char_name = "bubble3"
    expire_time = 5
class Bubble4(Range) :
    char_name = "bubble4"
    expire_time = 5
class Bubble5(Range) :
    char_name = "bubble5"
    expire_time = 5
class Earth3(Range) :
    char_name = "Earth3"
    expire_time = 5
class Wind2(Range) :
    char_name = "Wind2"
    expire_time = 8
class AngelAttack3(Range) :
    char_name = "AngelAttack3"
    expire_time = 7
""" Range extra Attack class """
class Arrow1(Range_extra) :
    char_name = "arrow1"
    active_name = "Attack2"
    expire_time = 5
    have_sound = True
    sfx = pygame.mixer.Sound("sounds\SFX\Arrow1.ogg")
class FireArrow(Range_extra) :
    char_name = "FireArrow"
    active_name = "Bomb5"
    expire_time = 7
    have_sound = True
    sfx = pygame.mixer.Sound("sounds\SFX\FireArrow.ogg")    
class IceArrow(Range_extra) :
    char_name = "IceArrow"
    active_name = "Bomb3"
    expire_time = 5
    have_sound = True
    sfx = pygame.mixer.Sound("sounds\SFX\IceArrow.ogg")    
class ThunderArrow(Range_extra) :
    char_name = "ThunderArrow"
    active_name = "Thunder1"
    expire_time = 7
    have_sound = True
    sfx = pygame.mixer.Sound("sounds\SFX\ThunderArrow.ogg")    
class FireBreath1(Range_extra) :
    char_name = "FireArrow"
    active_name = "FireBreath1"
    expire_time = 6
    