#class Team :
    #def __init__(self, characters) :
        #self.characters = characters
        #self.amount = len(characters)
        #self.expire = False
        #x = self[0].x
        #y = self[0].y
        #for i in range(1,len(self)) :
            #self[i].x = x-i
            #self[i].y = y
    #def __getitem__(self, i) :
        #return self.characters[i]
    #def __repr__(self) :
        #return str(self.characters)
    #def __len__(self) :
        #return self.amount
    #def pop(self, i) :
        #self.characters.pop(i)
        #self.amount -= 1
        #if self.amount == 0 :
            #self.expire = True
    #def ridExpire(self) :
        #i = 0
        #while i < self.amount :
            #if self[i].expire or self[i].hp <= 0 :
                #self.pop(i)
                #continue
            #i += 1
    #def move(self) :
        #for i in range(self.amount-1,0,-1) :
            #self[i].x = self[i-1].x
            #self[i].y = self[i-1].y
            #self[i].direction = self[i-1].direction
        #self[0].move()         
#class HeroTeam(Team) :
    #def __init__(self, characters, hero_able_use) :
        #Team.__init__(self, characters)
        #self.hero_able = hero_able_use
    #def reborn(self) :
        #for i in range(len(self)) :
            #self.characters[i].__init__()
            #self.x -= i
    #def join(self, new) :
        #self.characters.append(new)
        #self.amount += 1    
    #def pop(self, i) :
        #self.characters.pop(i)
            