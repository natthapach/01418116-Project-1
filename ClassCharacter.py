import pygame, random, math
import ClassAttack as CA
class Character :
    #Character's class variable
    degrees_melee = {"up":0, "down":180, "left":90, "right":-90}
    f_spd = 3 #figure speed
    fm_spd = f_spd*4 - 1    #figure speed max
    a_spd = 12
    ac_spd = 0
    def __init__(self,cell_size=32):
        #set initialize obj variable
        self.cell_size = 32
        # define position 
        self.x = 10
        self.y = 10
        self.direction = "right"
        # define scale
        self.width = 32
        self.height = 32
        # define counter
        self.fc_spd = 0     #figure speed counter    
        self.mc_spd = 0
        self.ac_spd = 0
        self.expire = False
        self.loadChar()
    def loadChar(self) :
        self.charSet = {}   #dictionary of character image
        charSet_up = []
        charSet_down = []
        charSet_left = []
        charSet_right = []
        for i in range(4) :
            i_str = str(i)
            charSet_up.append(pygame.image.load(self.imageRoot + self.char_name  + "_Up_" + i_str + ".png"))
            charSet_down.append(pygame.image.load(self.imageRoot + self.char_name + "_Down_" + i_str + ".png"))
            charSet_left.append(pygame.image.load(self.imageRoot + self.char_name + "_Left_" + i_str + ".png"))
            charSet_right.append(pygame.image.load(self.imageRoot + self.char_name + "_Right_" + i_str + ".png"))
        self.charSet["up"] = charSet_up
        self.charSet["down"] = charSet_down
        self.charSet["left"] = charSet_left
        self.charSet["right"] = charSet_right
        self.height = self.charSet["up"][0].get_height()
        self.width = self.charSet["up"][0].get_width()
        self.figure = self.charSet["up"][0]
    def __repr__(self) :
        return self.char_name
    def receiveFrame(self) :
        #stimulate figure counter
        if self.fc_spd >= self.fm_spd :
            self.fc_spd = 0
        else :
            self.fc_spd += 1
        self.setFigure()
        #stimulate attack counter
        if self.ac_spd < self.a_spd :
            self.ac_spd += 1
    def countMove(self) :
        #stimulate movement counter
        self.mc_spd += 1
        if self.mc_spd >= self.m_spd :
            self.mc_spd = 0
            return True
        return False
    def move(self) :
        if self.direction == "up" :
            self.y -= 1
        elif self.direction == "down" :
            self.y += 1
        elif self.direction == "right" :
            self.x += 1
        elif self.direction == "left" :
            self.x -= 1
    def getDisplayPos(self,cell_size=32) :
        return (self.x * cell_size, (self.y+1)*cell_size - self.height)
    def setFigure(self):
        div_fc = (self.fc_spd // self.f_spd) % 4
        self.figure = self.charSet[self.direction][div_fc]
    def requestField(self) :
        if self.ac_spd >= self.a_spd :
            return self.requestField_types[self.request_type](self)
        return []
    def receiveField(self, field) :
        for cell in field :
            # check all cell
            for obj in cell :
                # check obj in cell
                if obj.obj_type == self.target :
                    self.ac_spd = 0
                    return self.attack(obj.x, obj.y)
        return None
    def attack(self, target_x, target_y) :
        return self.attack_types[self.attack_type](self, target_x, target_y)  
    """ requestField template method """
    def requestField_type1(self) :
        #       [x]
        #       [x]
        #       [M]
        request = []
        if self.ac_spd >= self.a_spd :
            x = self.x
            y = self.y
            if self.direction == "up" :
                request = ((x,y-1), (x,y-2))
            elif self.direction == "down" :
                request = ((x,y+1), (x,y+2))
            elif self.direction == "left" :
                request = ((x-2,y), (x-1,y))
            elif self.direction == "right" :
                request = ((x+2,y), (x-2,y))
        return request
    def requestField_type2(self) :
        # [x][x][x]
        # [x][x][x]
        #    [M]
        request = []
        if self.ac_spd >= self.a_spd :
            x = self.x
            y = self.y
            if self.direction == "up" :
                request = ((x-1,y-2), (x,y-2), (x+1,y-2),
                           (x-1,y-1), (x,y-1), (x+1,y-1))
            elif self.direction == "down" :
                request = ((x-1,y+2), (x,y+2), (x+1,y+2),
                           (x-1,y+1), (x,y+1), (x+1,y+1))                
            elif self.direction == "left" :
                request = ((x-2,y-1), (x-2,y), (x-2,y+1),
                           (x-1,y-1), (x-1,y), (x-1,y+1))
            elif self.direction == "right" :
                request = ((x+2,y-1), (x+2,y), (x+2,y+1),
                           (x+1,y-1), (x+1,y), (x+1,y+1))
        return request    
    def requestField_type3(self) :
        # [x][x][x][x][x]
        # [x]         [x]
        # [x]   [M]   [x]
        # [x]         [x]
        # [x][x][x][x][x]
        request = []
        if self.ac_spd >= self.a_spd :
            x = self.x 
            y = self.y
            request = ((x-2,y-2), (x-1,y-2), (x,y-2), (x+1,y-2), (x+2,y-2),
                       (x-2,y-1), (x-2,y), (x-2,y+1),
                       (x+2,y-1), (x+2,y), (x+2,y+1),
                       (x-2,y+2), (x-1,y+2), (x,y+2), (x+1,y+2), (x+2,y+2))
        return request    
    def requestField_type4(self) :
        #    [x][x][x]
        #           
        #       [^]   
        request = []
        if self.ac_spd >= self.a_spd :
            x = self.x
            y = self.y          
            if self.direction == "up" :
                request = ((x-1,y-2), (x,y-2), (x+1,y-2))
            elif self.direction == "down" :
                request = ((x-1,y+2), (x,y+2), (x+1,y+2))
            elif self.direction == "left" :
                request = ((x-2,y-1), (x-2,y), (x-2,y+1))
            elif self.direction == "right" :
                request = ((x+2,y-1), (x+2,y), (x+2,y+1))       
        return request  
    def requestField_type5(self) :
        # [x]   [x][x][x]   [x]
        #    [x][x][x][x][x]
        # [x][x]         [x][x]
        # [x][x]   [^]   [x][x]
        # [x][x]         [x][x]
        #    [x][x][x][x][x]
        # [x]   [x][x][x]   [x]
        request = []
        if self.ac_spd >= self.a_spd :
            x = self.x
            y = self.y
            request = ((x-2,y-2), (x-1,y-2), (x,y-2), (x+1,y-2), (x+2,y-2),
                       (x-2,y-1), (x-2,y), (x-2,y+1),
                       (x+2,y-1), (x+2,y), (x+2,y+1),
                       (x-2,y+2), (x-1,y+2), (x,y+2), (x+1,y+2), (x+2,y+2),
                       
                       (x-1,y-3), (x,y-3), (x+1,y-3), (x-1,y+3), (x,y+3), (x+1,y+3),
                       (x-3,y-3), (x+3,y-3), (x-3,y+3), (x+3,y+3))
        return request    
    def requestField_type6(self) :
        #             [x]               
        #          [x][x][x]            
        #       [x][x][x][x][x]         
        #    [x][x]         [x][x]
        # [x][x][x]   [^]   [x][x][x]
        #    [x][x]         [x][x]
        #       [x][x][x][x][x]
        #          [x][x][x]
        #             [x]  
        request = []
        if self.ac_spd >= self.a_spd :
            x = self.x
            y = self.y
            request = ((x-2,y-2), (x-1,y-2), (x,y-2), (x+1,y-2), (x+2,y-2),
                       (x-2,y+2), (x-1,y+2), (x,y+2), (x+1,y+2), (x+2,y+2),
                       (x-2,y-1), (x-2,y), (x-2,y+1),
                       (x+2,y-1), (x+2,y), (x+2,y+1),
                       
                       (x-1,y-3), (x,y-3), (x+1,y-3),
                       (x-1,y+3), (x,y+3), (x+1,y+3),
                       (x-3,y-1), (x+3,y-1), (x-3,y), (x+3,y), (x-3,y+1), (x+3,y+1),
                       
                       (x,y-4), (x-4,y), (x+4), (x,y+4))        
        return request  
    def requestField_type8(self) :
        # [x][x][x][x][<]
        x = self.x
        y = self.y
        if self.direction == "up" :
            request = ((x,y-4), (x,y-3), (x,y-2), (x,y-1))
        elif self.direction == "down" :
            request = ((x,y+1), (x,y+2), (x,y+3), (x,y+4))
        elif self.direction == "left" :
            request = ((x-1,y), (x-2,y), (x-3,y), (x-4,y))
        elif self.direction == "right" :
            request = ((x+1,y), (x+2,y), (x+3,y), (x+4,y))
        return request
    def requestField_type9(self) :
        x = self.x
        y = self.y
        request = ((x-2,y-2), (x-1,y-2), (x,y-2), (x+1,y-2), (x+2,y-2),
                   (x-2,y+2), (x-1,y+2), (x,y+2), (x+1,y+2), (x+2,y+2),
                   (x-2,y-1), (x-2,y), (x-2,y+1), (x+2,y-1), (x+2,y), (x+2,y+1),
                   
                   (x-3,y-3), (x-2,y-3), (x-1,y-3), (x,y-3), (x+1,y-3), (x+2,y-3), (x+3,y-3),
                   (x-3,y+3), (x-2,y+3), (x-1,y+3), (x,y+3), (x+1,y+3), (x+2,y+3), (x+3,y+3),
                   (x-3,y-2), (x-3,y-1), (x-3,y), (x-3,y+1), (x-3,y+2), (x+3,y-2), (x+3,y-1), (x+3,y), (x+3,y+1), (x+3,y+2),
                   
                   (x-4,y-4), (x-3,y-4), (x-2,y-4), (x-1,y-4), (x,y-4), (x+1,y-4), (x+2,y-4), (x+3,y-4), (x+4,y-4),
                   (x-4,y+4), (x-3,y+4), (x-2,y+4), (x-1,y+4), (x,y+4), (x+1,y+4), (x+2,y+4), (x+3,y+4), (x+4,y+4),
                   (x-4,y-3), (x-4,y-2), (x-4,y-1), (x-4,y), (x-4,y+1), (x-4,y+2), (x-4,y+3), (x+4,y-3), (x+4,y-2), (x+4,y-1), (x+4,y), (x+4,y+1), (x+4,y+2), (x+4,y+3))
        return request 
                   
                   
                   
    """ attack template method """
    def attack_type1(self, target_x, target_y) :
        # target attack for Range
        # [x][x][x]
        # [x][T][x]     # [T] = target
        # [x][x][x]
        x = target_x
        y = target_y
        holding = ((x-1,y-1), (x,y-1), (x+1,y-1),
                   (x-1,y), (x,y), (x+1,y),
                   (x-1,y+1), (x,y+1), (x+1,y+1))
        start_x = self.x * self.cell_size
        start_y = self.y * self.cell_size
        goal_x = target_x * self.cell_size
        goal_y = target_y * self.cell_size
        end_x = (x-1) * self.cell_size
        end_y = (y-1) * self.cell_size
        return self.attack_class(self.Atk, self.target, start_x, start_y, goal_x, goal_y, end_x, end_y, holding)
    def attack_type1_2(self, target_x, target_y) :
        # target attack for Melee
        x = target_x
        y = target_y
        holding = ((x-1,y-1), (x,y-1), (x+1,y-1),
                   (x-1,y), (x,y), (x+1,y),
                   (x-1,y+1), (x,y+1), (x+1,y+1))        
        x = (x-1) * self.cell_size
        y = (y-1) * self.cell_size
        degree = 0
        return self.attack_class(self.Atk, self.target, x, y, holding, degree)
    def attack_type2(self, target_x, target_y) :
        # target attack
        #    [x]
        # [x][T][x]
        #    [x]
        x = target_x
        y = target_y
        holding = ((x-1,y), (x,y), (x+1,y), (x,y-1), (x,y+1))
        start_x = self.x * self.cell_size
        start_y = self.y * self.cell_size
        goal_x = target_x * self.cell_size
        goal_y = target_y * self.cell_size
        end_x = (x-1) * self.cell_size
        end_y = (y-1) * self.cell_size
        return self.attack_class(self.Atk, self.target, start_x, start_y, goal_x, goal_y, end_x, end_y, holding)
    def attack_type3(self, target_x, target_y) :
        # non target attack
        # [x]
        # [x]
        # [^]
        x = self.x
        y = self.y
        if self.direction == "up" :
            holding = ((x,y-1), (x,y-2))
            x = x * self.cell_size
            y = (y-2) * self.cell_size
        elif self.direction == "down" :
            holding = ((x,y+1), (x,y+2))
            x = x * self.cell_size
            y = (y+1) * self.cell_size
        elif self.direction == "left" :
            holding = ((x-1,y), (x-2,y))
            x = (x-2) * self.cell_size
            y = y * self.cell_size
        elif self.direction == "right" :
            holding = ((x+1,y), (x+2,y))
            x = (x+1) * self.cell_size
            y = y * self.cell_size
        degree = self.degrees_melee[self.direction]
        return self.attack_class(self.Atk, self.target, x, y, holding, degree)
    def attack_type4(self, target_x, target_y) :
        # non target attack
        # [x][x][x][x][<]
        x = self.x
        y = self.y
        if self.direction == "up" :
            holding = ((x,y-4), (x,y-3), (x,y-2), (x,y-1))
            x = x * self.cell_size
            y = (y-4) * self.cell_size
        elif self.direction == "down" :
            holding = ((x,y+1), (x,y+2), (x,y+3), (x,y+4))
            x = x * self.cell_size
            y = (y+1) * self.cell_size
        elif self.direction == "left" :
            holding = ((x-4,y) ,(x-3,y), (x-2,y), (x-1,y))
            x = (x-4) * self.cell_size 
            y = y *self.cell_size
        elif self.direction == "right" :
            holding = ((x+4,y), (x+3,y), (x+2,y), (x+1,y))
            x = (x+1) * self.cell_size
            y = y * self.cell_size
        degree = self.degrees_melee[self.direction]
        return self.attack_class(self.Atk, self.target, x, y, holding, degree)
    def attack_type5(self, target_x, target_y) :
        # non target attack
        # [x][x][x]
        # [x][x][x]
        #    [^]
        x = self.x
        y = self.y
        if self.direction == "up" :
            holding = ((x-1,y-2), (x,y-2), (x+1,y-2),
                       (x-1,y-1), (x,y-1), (x+1,y-1))
            x = (x-1) * self.cell_size
            y = (y-2) * self.cell_size
        elif self.direction == "down" :
            holding = ((x-1,y+2), (x,y+2), (x+1,y+2),
                        (x-1,y+1), (x,y+1), (x+1,y+1))
            x = (x-1) * self.cell_size
            y = (y+1) * self.cell_size    
        elif self.direction == "left" :
            holding = ((x-2,y-1), (x-2,y), (x-2,y+1),
                       (x-1,y-1), (x-1,y), (x-1,y+1))
            x = (x-2) * self.cell_size
            y = (y-1) * self.cell_size
        elif self.direction == "right" :
            holding = ((x+2,y-1), (x+2,y), (x+2,y+1),
                       (x+1,y-1), (x+1,y), (x+1,y+1))
            x = (x+1) * self.cell_size
            y = (y-1) * self.cell_size    
        degree = self.degrees_melee[self.direction]
        return self.attack_class(self.Atk, self.target, x, y, holding, degree)
    def attack_type6(self, target_x, target_y) :
        # non target attack
        # [x][x][x]
        # [x][^][x]
        # [x][x][x]
        x = self.x
        y = self.y
        holding = ((x-1,y-1), (x,y-1), (x+1,y), (x-1,y), (x+1,y), (x-1,y+1), (x,y+1), (x+1,y+1))
        x = (x-1) * self.cell_size
        y = (y-1) * self.cell_size
        degree = self.degrees_melee[self.direction]
        return self.attack_class(self.Atk, self.target, x, y, holding, degree)
    def attack_type7(self, target_x, target_y) :
        # non target attack
        # [x][x][x]
        # [x][x][x]
        # [x][x][x]
        #    [^]
        x = self.x
        y = self.y
        if self.direction == "up" :
            holding = ((x-1,y-3), (x,y-3), (x+1,y-3),
                       (x-1,y-2), (x,y-2), (x+1,y-2),
                       (x-1,y-1), (x,y-1), (x+1,y-1))
            x = (x-1) * self.cell_size
            y = (y-3) * self.cell_size
        elif self.direction == "down" :
            holding = ((x-1,y+3), (x,y+3), (x+1,y+3),
                       (x-1,y+2), (x,y+2), (x+1,y+2),
                       (x-1,y+1), (x,y+1), (x+1,y+1))
            x = (x-1) * self.cell_size
            y = (y+1) * self.cell_size
        elif self.direction == "left" :
            holding = ((x-1,y-1), (x-1,y), (x-1,y+1),
                       (x-2,y-1), (x-2,y), (x-2,y+1),
                       (x-3,y-1), (x-3,y), (x-3,y+1))
            x = (x-3) * self.cell_size
            y = (y-1) * self.cell_size
        elif self.direction == "right" :
            holding = ((x+1,y-1), (x+1,y), (x+1,y+1),
                       (x+2,y-1), (x+2,y), (x+2,y+1),
                       (x+3,y-1), (x+3,y), (x+3,y+1))            
            x = (x+1) * self.cell_size
            y = (y-1) * self.cell_size
        degree = self.degrees_melee[self.direction]
        return self.attack_class(self.Atk, self.target, x, y, holding, degree)
    def attack_type8(self, target_x, target_y) :
        holding = [(self.x, self.y)]
        return self.attack_class(self.Atk, self.target, self.x, self.y, target_x, target_y, holding)        
        
                       
    
    requestField_types = {"type1":requestField_type1, "type2":requestField_type2,
                          "type3":requestField_type3, "type4":requestField_type4,
                          "type5":requestField_type5, "type6":requestField_type6,
                          "type8":requestField_type8, "type9":requestField_type9}       
    attack_types = {"type1":attack_type1, "type1_2":attack_type1_2, "type2":attack_type2, "type3":attack_type3, "type4":attack_type4,
                    "type5":attack_type5, "type6":attack_type6, "type7":attack_type7, "type8":attack_type8}
""" Hero Class """        
class Hero(Character) :
    #Hero's class variable
    imageRoot = "image\character\hero\\"
    obj_type = "Hero"
    target = "Monster"
    a_spd = 12  #default attack speed
    m_spd = 4   #default movement speed
    def __init__(self) :
        Character.__init__(self)
        self.leader = False
        self.Atk = self.Atk_base + math.ceil(self.Atk_rate * self.level)
        self.Def = self.Def_base + math.ceil(self.Def_rate * self.level)
        self.Hp = self.Hp_base + math.ceil(self.Hp_rate * self.level)
        self.hp = self.Hp  
        self.Sp = 0 
    def gainExp(self, mon_level) :
        # cal exp
        exp = (2 * (mon_level - self.level)) + 10
        if exp > 20 :
            exp = 20
        elif exp < 0 :
            exp = 0
        # add exp
        total_exp = self.__class__.exp + exp
        if total_exp >= self.max_exp :
            # check level up
            self.__class__.exp = total_exp - self.max_exp
            self.__class__.level += 1
            self.__class__.calMaxExp()
        else :
            self.__class__.exp = total_exp
    @classmethod
    def calMaxExp(klass) :
        lv = klass.level
        klass.max_exp = (lv**2 - 2*lv + 5) * 10
        # f(x) = x**2 - 2x + 5
    @classmethod
    def calStatus(klass) :
        Atk = klass.Atk_base + math.ceil(klass.Atk_rate * klass.level)
        Def = klass.Def_base + math.ceil(klass.Def_rate * klass.level)
        Hp = klass.Hp_base + math.ceil(klass.Hp_rate * klass.level)
        return (Atk, Def, Hp)
    @classmethod
    def getStatus(klass, status) :
        level = status[1]
        exp = status[2]
        klass.level = int(level)
        klass.exp = int(exp)
        klass.calMaxExp()
    @classmethod
    def getEncode(klass) :
        line = klass.char_name + "," + str(klass.level) + "," + str(klass.exp)
        return line
        

class Paladin(Hero) :
    #Paladin's class variable
    char_name = "Paladin"
    exp = 0
    price = 500
    # define status
    # mutable status
    level = 1
    Atk_base = 24
    Def_base = 12
    Hp_base = 80
    # immutable status
    Atk_rate = 5.5
    Def_rate = 3.9
    Hp_rate = 15
    # image and file data
    icon = pygame.image.load(Hero.imageRoot + "Paladin_icon_unlock.png")
    icon_lock = pygame.image.load(Hero.imageRoot + "Paladin_icon_lock.png") 
    img = pygame.image.load(Hero.imageRoot + "Paladin_img.png")
    def __init__(self) :
        Hero.__init__(self)       
    def __repr__(self) :
        return "Paladin"
    def requestField(self) :
        if self.ac_spd >= self.a_spd :
            x = self.x
            y = self.y
            if self.direction == "up" :
                request = ((x-1,y-2), (x,y-2), (x+1,y-2),
                           (x-1,y-1), (x,y-1), (x+1,y-1))
            elif self.direction == "down" :
                request = ((x-1,y+1), (x,y+1), (x+1,y-2),
                           (x-1,y+2), (x,y+2), (x+1,y-2))      
            elif self.direction == "left" :
                request = ((x-2,y-1), (x-1,y-1),
                           (x-2,y),   (x-1,y),
                           (x-2,y+1), (x-1,y+1))
            elif self.direction == "right" :
                request = ((x+1,y-1), (x+2,y-1),
                           (x+1,y),   (x+2,y),
                           (x+1,y+1), (x+2,y+1)) 
            return request
        else :
            return []
    def attack(self, target_x, target_y) :
        # [a][a][a]     # a = attack area
        # [a][a][a]
        #    [^]
        x = self.x      #temporary x 
        y = self.y      #temporary y
        if self.direction == "up" :
            rotate = 0
            holding = ((x-1,y-2), (x,y-2), (x+1,y-2),
                       (x-1,y-1), (x,y-1), (x+1,y-1))
            x = (x-1) * self.cell_size
            y = (y-2) * self.cell_size
        elif self.direction == "left" :
            rotate = 90
            holding = ((x-2,y-1), (x-1,y-1),
                       (x-2,y),   (x-1,y),
                       (x-2,y+1), (x-1,y+1))
            x = (x-2) * self.cell_size
            y = (y-1) * self.cell_size
        elif self.direction == "down" :
            rotate = 180
            holding = ((x-1,y+1), (x,y+1), (x+1,y-2),
                       (x-1,y+2), (x,y+2), (x+1,y-2))            
            x = (x-1) * self.cell_size
            y = (y+1) * self.cell_size
        elif self.direction == "right" :
            rotate = 270    
            holding = ((x+1,y-1), (x+2,y-1),
                       (x+1,y),   (x+2,y),
                       (x+1,y+1), (x+2,y+1))            
            x = (x+1) * self.cell_size
            y = (y-1) * self.cell_size
        return CA.Sword2(self.Atk, "Monster", x, y, holding, rotate)
        
class Lancer(Hero) :
    #Lancer's class variable
    char_name = "Lancer"
    exp = 0
    price = 300
    level = 1
    Atk_base = 26
    Def_base = 10
    Hp_base = 70
    Atk_rate = 5.9
    Def_rate = 3.4
    Hp_rate = 16
    
    icon = pygame.image.load(Hero.imageRoot + "Lancer_icon_unlock.png")
    icon_lock = pygame.image.load(Hero.imageRoot + "Lancer_icon_lock.png")
    img = pygame.image.load(Hero.imageRoot + "Lancer_img.png")
    def __init__(self) :
        Hero.__init__(self)
    def requestField(self) :
        if self.ac_spd >= self.a_spd :
            x = self.x
            y = self.y
            if self.direction == "up" :
                request = ((x, y-1), (x, y-2), (x, y-3), (x, y-4))
            elif self.direction == "down" :
                request = ((x, y+1), (x, y+2), (x, y+3), (x, y+4))
            elif self.direction == "left" :
                request = ((x-4, y), (x-3, y), (x-2, y), (x-1, y))
            elif self.direction == "right" :
                request = ((x+1, y), (x+2, y), (x+3, y), (x+4, y))
            return request
        else :
            return []
    def attack(self, target_x, target_y) :
        # [a]    # a = attack area
        # [a]
        # [a]
        # [a]
        # [^]
        x = self.x
        y = self.y
        if self.direction == "up" :
            holding = ((x, y-1), (x, y-2), (x, y-3), (x, y-4))
            rotate = 0
            x = x * self.cell_size
            y = (y-4) * self.cell_size            
        elif self.direction == "down" :
            holding = ((x, y+1), (x, y+2), (x, y+3), (x, y+4))
            rotate = 180
            x = x * self.cell_size
            y = (y+1) * self.cell_size            
        elif self.direction == "left" :
            holding = ((x-4, y), (x-3, y), (x-2, y), (x-1, y))
            rotate = 90
            x = (x-4) * self.cell_size
            y = y * self.cell_size
        elif self.direction == "right" :
            holding = ((x+1, y), (x+2, y), (x+3, y), (x+4, y))
            rotate = 270
            x = (x+1) * self.cell_size
            y = y * self.cell_size            
        return CA.Lance1(self.Atk, "Monster", x, y, holding, rotate)
    def __repr__(self) :
        return "Lancer"
    
class Mage(Hero) :
    # Mage's class variable
    char_name = "Mage"
    exp = 0
    price = 500
    # define status
    # mutable status
    level = 1
    Atk_base = 24
    Def_base = 9
    Hp_base = 70
    a_spd = 16
    # immutable status
    Atk_rate = 5.4
    Def_rate = 3.2
    Hp_rate = 14
    
    request_type = "type6"
    attack_type = "type1"
    attack_class = CA.Bomb1
    icon = pygame.image.load(Hero.imageRoot + "Mage_icon_unlock.png")
    icon_lock = pygame.image.load(Hero.imageRoot + "Mage_icon_lock.png") 
    img = pygame.image.load(Hero.imageRoot + "Mage_img.png")
    
class ElfRanger(Hero) :
    char_name = "Elf-Ranger"
    exp = 0
    price = 700
    level = 1
    Atk_base = 21
    Def_base = 9
    Hp_base = 60
    a_spd = 10
    Atk_rate = 5.3
    Def_rate = 3.2
    Hp_rate = 14
    
    icon = pygame.image.load(Hero.imageRoot + "Elf-Ranger_icon_unlock.png")
    icon_lock = pygame.image.load(Hero.imageRoot + "Elf-Ranger_icon_lock.png")
    img = pygame.image.load(Hero.imageRoot + "Elf-Ranger_img.png") 

    def requestField(self) :
        if self.ac_spd >= self.a_spd :
            x = self.x
            y = self.y
            request = ((x-1,y-1), (x,y-1), (x+1,y-1), (x-1,y), (x+1,y), (x-1,y+1), (x,y+1), (x+1,y+1),
                       (x-2,y-2), (x,y-2), (x+2,y-2), (x-2,y), (x+2,y), (x-2,y+2), (x,y+2), (x+2,y+2),
                       (x-3,y-3), (x,y-3), (x+3,y-3), (x-3,y), (x+3,y), (x-3,y+3), (x,y+3), (x+3,y+3),
                       (x-4,y-4), (x,y-4), (x+4,y-4), (x-4,y), (x+4,y), (x-4,y+4), (x,y+4), (x+4,y+4),
                       (x-5,y-5), (x,y-5), (x+5,y-5), (x-5,y), (x+5,y), (x-5,y+5), (x,y+5), (x+5,y+5))
                       
            return request
        return []
    def attack(self, target_x, target_y) :
        holding = [(self.x, self.y)]
        return CA.Arrow1(self.Atk, "Monster", self.x, self.y, target_x, target_y, holding)
class ElementalMaster(Hero) :
    char_name = "Elemental-Master"
    exp = 0
    price = 700
    level = 1
    Atk_base = 25
    Def_base = 8
    Hp_base = 60
    a_spd = 11
    Atk_rate = 5.8 
    Def_rate = 3.0
    Hp_rate = 13 
    
    icon = pygame.image.load(Hero.imageRoot + "Elemental-Master_icon_unlock.png")
    icon_lock = pygame.image.load(Hero.imageRoot + "Elemental-Master_icon_lock.png")
    img = pygame.image.load(Hero.imageRoot + "Elemental-Master_img.png")     
    def requestField(self) :
        if self.ac_spd >= self.a_spd :
            x = self.x
            y = self.y
            request = ((x-1,y-1), (x,y-1), (x+1,y-1), (x-1,y), (x+1,y), (x-1,y+1), (x,y+1), (x+1,y+1),
                       (x-2,y-2), (x,y-2), (x+2,y-2), (x-2,y), (x+2,y), (x-2,y+2), (x,y+2), (x+2,y+2),
                       (x-3,y-3), (x,y-3), (x+3,y-3), (x-3,y), (x+3,y), (x-3,y+3), (x,y+3), (x+3,y+3),
                       (x-4,y-4), (x,y-4), (x+4,y-4), (x-4,y), (x+4,y), (x-4,y+4), (x,y+4), (x+4,y+4),
                       (x-5,y-5), (x,y-5), (x+5,y-5), (x-5,y), (x+5,y), (x-5,y+5), (x,y+5), (x+5,y+5))
                       
            return request
        return []
    def attack(self, target_x, target_y) :
        holding = [(self.x, self.y)]
        attack_classes = [CA.FireArrow, CA.IceArrow, CA.ThunderArrow]
        attack_class = random.choice(attack_classes)
        return attack_class(self.Atk, "Monster", self.x, self.y, target_x, target_y, holding)    
class Magnus(Hero) :
    char_name = "Magnus"
    exp = 0
    level = 1
    price = 1000
    Atk_base = 25
    Def_base = 11
    Hp_base = 80
    Atk_rate = 5.7
    Def_rate = 3.5
    Hp_rate = 15
    
    request_type = "type5"
    attack_type = "type1_2"
    attack_class = CA.BlackHole1
    icon = pygame.image.load(Hero.imageRoot + "Magnus_icon_unlock.png")
    icon_lock = pygame.image.load(Hero.imageRoot + "Magnus_icon_lock.png")
    img = pygame.image.load(Hero.imageRoot + "Magnus_img.png")    
    
    
    
""" Monsters class """
""" super class """
class Monster(Character) :
    imageRoot = "image\character\monster\\"
    obj_type = "Monster"
    target = "Hero"
    m_spd = 6
    a_spd = 15
    d_spd = 24
    def __init__(self, level) :
        Character.__init__(self)
        self.expire = False
        self.level = level
        self.Atk = self.Atk_base + math.ceil(self.Atk_rate * self.level)
        self.Def = self.Def_base + math.ceil(self.Def_rate * self.level)
        self.Hp = self.Hp_base + math.ceil(self.Hp_rate * self.level)
        self.hp = self.Hp  
        self.dc_spd = 0
    def countDirection(self) :
        #stimulate direction counter for leader
        if self.dc_spd >= self.d_spd :
            self.dc_spd = 0
            self.randomDirection()
        else :
            self.dc_spd += 1
    def randomDirection(self) :
        if self.direction == "up" :
            self.direction = random.choice(("up", "left", "right"))
        elif self.direction == "down" :
            self.direction = random.choice(("down", "left", "right"))
        elif self.direction == "left" :
            self.direction = random.choice(("up", "down", "left"))
        elif self.direction == "right" :
            self.direction = random.choice(("up", "down", "right"))   
    

class Slime(Monster) :
    # define status
    # mutable status
    Atk_base = 20
    Def_base = 5
    Hp_base = 60
    a_spd = 15
    m_spd = 8
    d_spd = m_spd * 4
    # immutable status
    Atk_rate = 5.0
    Def_rate = 2.95
    Hp_rate = 7
    
    request_type = "type4"
    attack_type = "type7"
    attack_class = CA.Attack2
        
class BigSlime(Monster) :
    # define status
    # mutable status
    Atk_base = 22
    Def_base = 6
    Hp_base = 65
    a_spd = 15
    m_spd = 8
    d_spd = m_spd * 4
    # immutable status
    Atk_rate = 5.1
    Def_rate = 3.2
    Hp_rate = 8
    request_type = "type3"
    attack_type = "type2"
class Bat(Monster) :
    Atk_base = 22
    Def_base = 7
    Hp_base = 70
    Atk_rate = 3.3
    Def_rate = 5.4
    Hp_rate = 9
    request_type = "type1"
    attack_type = "type3"
    attack_class = CA.Attack2
    
class Wolf(Monster) :
    Atk_base = 23
    Def_base = 6
    Hp_base = 68
    Atk_rate = 5.5
    Def_rate = 3.1
    Hp_rate = 9
    request_type = "type2"
    attack_type = "type5"
    attack_class = CA.Claw1

class Ghost(Monster) :
    Atk_base = 22
    Def_base = 7
    Hp_base = 60
    m_spd = 9
    d_spd = 36
    Atk_rate = 5.1
    Def_rate = 3.4
    Hp_rate = 9
    request_type = "type4"
    attack_type = "type7"
    attack_class = CA.Ghost1

    
""" concrete Monster class """
""" State 1 : Wind Forrest monsters """
# Slime
class Slime1(Slime) :
    char_name = "Slime1"
class Slime2(Slime) :
    char_name = "Slime2"
class Slime3(Slime) :
    char_name = "Slime3"
class Slime4(Slime) :
    char_name = "Slime4"
class Slime5(Slime) :
    char_name = "Slime5"
# Big Slime
class BigSlime1(BigSlime) :
    char_name = "Big-Slime1"
    attack_class = CA.Bubble1
class BigSlime2(BigSlime) :
    char_name = "Big-Slime2"
    attack_class = CA.Bubble2
class BigSlime3(BigSlime) :
    char_name = "Big-Slime3"
    attack_class = CA.Bubble3
class BigSlime4(BigSlime) :
    char_name = "Big-Slime4"
    attack_class = CA.Bubble4
class BigSlime5(BigSlime) :
    char_name = "Big-Slime5"
    attack_class = CA.Bubble5
""" State 2 : Forbidden Forrest monsters """
# Mushroom
class Mushroom1(Monster) :
    char_name = "Mushroom1"
    Atk_base = 23
    Def_base = 6
    Hp_base = 60
    m_spd = 7
    d_spd = 28
    Atk_rate = 5.5
    Def_rate = 3.5
    Hp_rate = 8
    request_type = "type2"
    attack_type = "type5"
    attack_class = CA.Impact1
# Flower
class Flower1(Monster) :
    char_name = "Flower1"
    Atk_base = 22
    Def_base = 9
    Hp_base = 85
    a_spd = 14
    m_spd = 7
    d_spd = 28
    Atk_rate = 5.5
    Def_rate = 3.7
    Hp_rate = 11
    request_type = "type3"
    attack_type = "type6"
    attack_class = CA.Poision1
class Flower2(Monster) :
    char_name = "Flower2"
    Atk_base = 24
    Def_base = 7
    Hp_base = 80
    a_spd = 14
    m_spd = 7
    d_spd = 28
    Atk_rate = 5.6
    Def_rate = 3.5
    Hp_rate = 10
    request_type = "type3"
    attack_type = "type6"
    attack_class = CA.Poision2
#Bat
class Bat1(Bat) :
    char_name = "Bat1"
class Bat2(Bat) :
    char_name = "Bat2"
class Bat3(Bat) :
    char_name = "Bat3"
#Wolf
class Wolf1(Wolf) :
    char_name = "Wolf1"
class Wolf2(Wolf) :
    char_name = "Wolf2"
class Wolf3(Wolf) :
    char_name = "Wolf3"
#Goblin
class WolfGoblin(Monster) :
    char_name = "WolfGoblin"
    Atk_base = 23
    Def_base = 7
    Hp_base = 70
    Atk_rate = 5.5
    Def_rate = 3.5
    Hp_rate = 9
    request_type = "type2"
    attack_type = "type5"
    attack_class = CA.Sword1
class GreenGoblin(Monster) :
    char_name = "GreenGoblin"
    Atk_base = 21
    Def_base = 9
    Hp_base = 80
    Atk_rate = 5.2
    Def_rate = 3.7
    Hp_rate = 10
    request_type = "type2"
    attack_type = "type5"
    attack_class = CA.Xcross2
class RedGoblin(Monster) :
    char_name = "RedGoblin"
    Atk_base = 21
    Def_base = 4
    Hp_base = 90
    Atk_rate = 5.8
    Def_rate = 5.6
    Hp_rate = 11
    request_type = "type8"
    attack_type = "type4"
    attack_class = CA.Lance2
class Ghost1(Ghost) :
    char_name = "Ghost1"
class Ghost2(Ghost) :
    char_name = "Ghost2"
class Ghost3(Ghost) :
    char_name = "Ghost3"
class Doll(Monster) :
    char_name = "Doll"
    Atk_base = 23
    Def_base = 7
    Hp_base = 80
    m_spd = 9
    d_spd = 36
    Atk_rate = 5.5
    Def_rate = 3.6
    Hp_rate = 9
    request_type = "type3"
    attack_type = "type1_2"
    attack_class = CA.Hole1
class SkeletonKnight(Monster) :
    char_name = "SkeletonKnight"
    Atk_base = 24
    Def_base = 7
    Hp_base = 65
    Atk_rate = 5.8
    Def_rate = 3.4
    Hp_rate = 9
    request_type = "type2"
    attack_type = "type7"
    attack_class = CA.Xcross1       # red cross
class Zombie(Monster) :
    char_name = "Zombie"
    Atk_base = 21
    Def_base = 9
    Hp_base = 95
    m_spd = 9
    d_spd = 36
    Atk_rate = 5.3
    Def_rate = 3.8
    Hp_rate = 11
    request_type = "type2"
    attack_type = "type7"
    attack_class = CA.Attack2
class SkeletonKing(Monster) :
    char_name = "SkeletonKing"
    Atk_base = 21
    Def_base = 9
    Hp_base = 100
    m_spd = 5
    d_spd = 20
    Atk_rate = 5.6
    Def_rate = 3.8
    Hp_rate = 15
    request_type = "type9"
    attack_type = "type1_2"
    attack_class = CA.DeathMark

""" State 3 : Fairy Hill monsters """
class FireElemental2(Monster) :
    char_name = "FireElemental2"
    Atk_base = 24
    Def_base = 6
    Hp_base = 70
    Atk_rate = 5.7
    Def_rate = 3.4
    Hp_rate = 9
    request_type = "type6"
    attack_type = "type1"
    attack_class = CA.Bomb2    
class FireElemental1(FireElemental2) :
    char_name = "FireElemental1"
    request_type = "type3"
    attack_type = "type6"
    attack_class = CA.Fire1       
class EarthElemental2(Monster) :
    char_name = "EarthElemental2"
    Atk_base = 20
    Def_base = 9
    Hp_base = 80
    Atk_rate = 5.2
    Def_rate = 3.8
    Hp_rate = 10
    request_type = "type5"
    attack_type = "type1"
    attack_class = CA.Earth3
class EarthElemental1(EarthElemental2) :
    char_name = "EarthElemental1"
    request_type = "type3"
    attack_type = "type6"
    attack_class = CA.Earth1
class AquaElemental2(Monster) :
    char_name = "AquaElemental2"
    Atk_base = 21
    Def_base = 7
    Hp_base = 100
    Atk_rate = 5.0
    Def_rate = 3.4
    Hp_rate = 12
    request_type = "type5"
    attack_type = "type1_2"
    attack_class = CA.Aqua1
class AquaElemental1(AquaElemental2) :
    char_name = "AquaElemental1"
    request_type = "type3"
    attack_type = "type6"
    attack_class = CA.Aqua2
class WindElemental2(Monster) :
    char_name = "WindElemental2"
    Atk_base = 22
    Def_base = 7
    Hp_base = 70
    a_spd = 12
    Atk_rate = 5.4
    Def_rate = 3.4
    Hp_rate = 9
    request_type = "type6"
    attack_type = "type1"
    attack_class = CA.Wind2
class WindElemental1(WindElemental2) :
    char_name = "WindElemental1"
    request_type = "type3"
    attack_type = "type6"
    attack_class = CA.Wind1
    
""" state 4 : Temple of God monster """
class Angel1(Monster) :
    char_name = "Angel1"
    Atk_base = 22
    Def_base = 7
    Hp_base = 80
    Atk_rate = 5.4
    Def_rate = 3.4
    Hp_rate = 9
    request_type = "type3"
    attack_type = "type1_2"
    attack_class = CA.Attack2
class Angel2(Monster) :
    char_name = "Angel2"
    Atk_base = 22
    Def_base = 9
    Hp_base = 80
    Atk_rate = 5.5
    Def_rate = 3.7
    Hp_rate = 10
    request_type = "type5"
    attack_type = "type1_2"
    attack_class = CA.AngelAttack1
class Angel3(Monster) :
    char_name = "Angel3"
    Atk_base = 24
    Def_base = 6
    Hp_base = 90
    Atk_rate = 5.8
    Def_rate = 3.5
    Hp_rate = 10
    request_type = "type2"
    attack_type = "type5"
    attack_class = CA.AngelAttack2
class Angel4(Monster) :
    char_name = "Angel4"
    Atk_base = 22
    Def_base = 7
    Hp_base = 100
    Atk_rate = 5.5
    Def_rate = 3.6
    Hp_rate = 11
    request_type = "type6"
    attack_type = "type1"
    attack_class = CA.AngelAttack3

""" state 5 : Catacomb Frost monster """
class Giant(Monster) :  # Hp type
    char_name = "Giant"
    Atk_base = 22
    Def_base = 7
    Hp_base = 95
    Atk_rate = 5.5
    Def_rate = 3.5
    Hp_rate = 10
    request_type = "type3"
    attack_type = "type1_2"
    attack_class = CA.Earth2
class Devil3(Monster) : # Def type
    char_name = "Devil3"
    Atk_base = 22
    Def_base = 9
    Hp_base = 80
    Atk_rate = 5.4
    Def_rate = 3.8
    Hp_rate = 9
    request_type = "type3"
    attack_type = "type1_2"
    attack_class = CA.Tornado1
class Devil4(Monster) : # Def type
    char_name = "Devil4"
    Atk_base = 23
    Def_base = 8
    Hp_base = 85
    Atk_rate = 5.4
    Def_rate = 3.7
    Hp_rate = 10
    request_type = "type3"
    attack_type = "type1_2"
    attack_class = CA.Thunder2
class Devil2_Ice(Monster) : # Atk type
    char_name = "Devil2-Ice"
    Atk_base = 24
    Def_base = 7
    Hp_base = 90
    Atk_rate = 5.9
    Def_rate = 3.4
    Hp_rate = 8
    request_type = "type3"
    attack_type = "type1_2"
    attack_class = CA.Ice1
class Dracula(Monster) :    # Hp type
    char_name = "Dracula"
    Atk_base = 23
    Def_base = 7
    Hp_base = 110
    Atk_rate = 5.6
    Def_rate = 3.5
    Hp_rate = 13
    request_type = "type3"
    attack_type = "type1_2"
    attack_class = CA.Soul2
    
""" state 6 : Vocanic Citadel """
class Cerberus(Monster) :   # Atk type
    char_name = "Cerberus"
    Atk_base = 24
    Def_base = 8
    Hp_base = 90
    Atk_rate = 5.9
    Def_rate = 3.6
    Hp_rate = 10
    request_type = "type2"
    attack_type = "type5"
    attack_class = CA.ClawFire
class Soldier(Monster) :
    Atk_base = 24
    Def_base = 8
    Hp_base = 75
    Atk_rate = 5.7
    Def_rate = 3.6
    Hp_rate = 11
    request_type = "type2"
    attack_type = "type4"
    attack_class = CA.Lance2
class Soldier1(Soldier) :
    char_name = "Soldier1"
class Soldier2(Soldier) :
    char_name = "Soldier2"
class Soldier3(Soldier) :
    char_name = "Soldier3"
class Soldier4(Soldier) :
    char_name = "Soldier4"
class Devil2(Monster) :
    char_name = "Devil2"
    Atk_base = 24
    Def_base = 7
    Hp_base = 90
    Atk_rate = 5.9
    Def_rate = 3.4
    Hp_rate = 8
    request_type = "type3"
    attack_type = "type1_2"
    attack_class = CA.Bomb5
class SnakeDragon(Monster) :
    char_name = "SnakeDragon"
    Atk_base = 23
    Def_base = 7
    Hp_base = 90
    Atk_rate = 5.7
    Def_rate = 3.5
    Hp_rate = 10
    attack_type = "type8"
    attack_class = CA.FireBreath1
    def requestField(self) :
        if self.ac_spd >= self.a_spd :
            x = self.x
            y = self.y
            request = ((x-1,y-1), (x,y-1), (x+1,y-1), (x-1,y), (x+1,y), (x-1,y+1), (x,y+1), (x+1,y+1),
                       (x-2,y-2), (x,y-2), (x+2,y-2), (x-2,y), (x+2,y), (x-2,y+2), (x,y+2), (x+2,y+2),
                       (x-3,y-3), (x,y-3), (x+3,y-3), (x-3,y), (x+3,y), (x-3,y+3), (x,y+3), (x+3,y+3),
                       (x-4,y-4), (x,y-4), (x+4,y-4), (x-4,y), (x+4,y), (x-4,y+4), (x,y+4), (x+4,y+4),
                       (x-5,y-5), (x,y-5), (x+5,y-5), (x-5,y), (x+5,y), (x-5,y+5), (x,y+5), (x+5,y+5))
                       
            return request
        return []    
class Dragon(Monster) :
    char_name = "Dragon"
    Atk_base = 24
    Def_base = 9
    Hp_base = 150
    Atk_rate = 5.8
    Def_rate = 3.6
    Hp_rate = 14
    request_type = "type9"
    attack_type = "type1_2"
    attack_class = CA.Meteorite1

""" state 7 : Lost Island """



            
monster_lib = {"Slime1":Slime1, "Slime2":Slime2, "Slime3":Slime3, "Slime4":Slime4, "Slime5":Slime5,
               "BigSlime1":BigSlime1, "BigSlime2":BigSlime2, "BigSlime3":BigSlime3, "BigSlime4":BigSlime4, "BigSlime5":BigSlime5,
               
               "Mushroom1":Mushroom1, "Flower1":Flower1, "Flower2":Flower2,
               "Bat1":Bat1, "Bat2":Bat2, "Bat3":Bat3, "Wolf1":Wolf1, "Wolf2":Wolf2, "Wolf3":Wolf3,
               "WolfGoblin":WolfGoblin, "GreenGoblin":GreenGoblin, "RedGoblin":RedGoblin,
               "Ghost1":Ghost1, "Ghost2":Ghost2, "Ghost3":Ghost3, "Doll":Doll,
               "SkeletonKnight":SkeletonKnight, "Zombie":Zombie,
               "SkeletonKing":SkeletonKing,
               
               "FireElemental1":FireElemental1, "FireElemental2":FireElemental2,
               "EarthElemental1":EarthElemental1, "EarthElemental2":EarthElemental2,
               "AquaElemental1":AquaElemental1, "AquaElemental2":AquaElemental2,
               "WindElemental1":WindElemental1, "WindElemental2":WindElemental2,
               
               "Angel1":Angel1, "Angel2":Angel2, "Angel3":Angel3, "Angel4":Angel4,
               
               "Giant":Giant, "Devil3":Devil3, "Devil4":Devil4, "Devil2_Ice":Devil2_Ice, "Dracula":Dracula,
               
               "Cerberus":Cerberus, "Soldier1":Soldier1, "Soldier2":Soldier2, "Soldier3":Soldier3, "Soldier4":Soldier4,
               "Devil2":Devil2, "SnakeDragon":SnakeDragon, "Dragon":Dragon}
hero_lib = {"Paladin":Paladin, "Lancer":Lancer, "Mage":Mage, "Elf-Ranger":ElfRanger, "Elemental-Master":ElementalMaster, "Magnus":Magnus}

""" 
Note :

Hero status range
Hp_base [55,65]
Hp_rate [4,7]
Atk_base [14,16]
Atk_rate [1.1,1.3]
Def_base [9,11]
Def_rate [1.0,1.2]

Monster status range
Hp_base [15,25]    **boss [30,35]
Hp_rate [4,6]
Atk_base [15,17]
Atk_rate [1.1,1.3]
Def_base [5,7]
Def_rate [1.0,1.2]
"""
