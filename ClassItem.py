import pygame, random, math
import ClassCharacter as CC
import ClassAttack as CA
from pygame.locals import *

class Item :
    imageRoot = "image\item\\"
    obj_type = "Item"
    def __init__(self, x=0, y=0) :
        self.x = x
        self.y = y
        self.expire = False
    def getDisplayPos(self, cell_size=32) :
        return (self.x * cell_size, (self.y+1)*cell_size - self.height)
class DropHero(Item) :
    def __init__(self, pos, hero_able_use) :
        x,y = pos
        Item.__init__(self, x, y)
        rand_index = random.randrange(len(hero_able_use))
        hero = hero_able_use.pop(rand_index)
        self.drop_hero = CC.hero_lib[hero]()
        self.target = "Hero"
        self.figure = pygame.image.load(self.imageRoot + "drop_hero.png")
        self.height = self.figure.get_height()
    def work(self, team) :
        if team[-1].direction == "up" :
            x = team[-1].x
            y = team[-1].y + 1 
        elif team[-1].direction == "down" :
            x = team[-1].x
            y = team[-1].y - 1
        elif team[-1].direction == "left" :
            x = team[-1].x + 1
            y = team[-1].y 
        elif team[-1].direction == "right" :
            x = team[-1].x - 1
            y = team[-1].y
        self.drop_hero.direction = team[-1].direction
        self.drop_hero.x = x
        self.drop_hero.y = y
        team.append(self.drop_hero)
        del self.drop_hero
        self.expire = True
class HpPotion :
    heal_rate = 0.0
    def work(self, team) :
        dmgs = []
        for member in team :
            dmg = math.ceil(member.Hp*self.heal_rate)
            new_hp = member.hp + dmg
            if new_hp > member.Hp :
                new_hp = member.Hp
            member.hp = new_hp
            dmg = CA.Damage("Heal", dmg, member.getDisplayPos())
            dmgs.append(dmg)
        return dmgs
class HpPotion1(HpPotion) :
    heal_rate = 0.1
class HpPotion2(HpPotion) :
    heal_rate = 0.15
class HpPotion3(HpPotion) :
    heal_rate = 0.2
class HpPotion4(HpPotion) :
    heal_rate = 0.25