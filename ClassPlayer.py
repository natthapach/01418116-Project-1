import ClassCharacter as CC
class Player :
    fileRoot = "file\\"
    state_key_checker = ("map1", "map2", "map3", "map4", "map5", "map6", "map7")
    hero_key_checker = ("Paladin", "Lancer", "Elf-Ranger", "Mage","Elemental-Master","Magnus")
    def __init__(self, file_name) :
        self.file_name = file_name
        self.file = open(self.fileRoot + file_name, "r")
        self.money = 0
        self.state_unlock = {}
        self.hero_unlock = {}
        self.hp_potions = [0,0,0,0,0]
        self.decode()
    def decode(self) :
        money_line = []
        potion_line = []
        state_unlock_key = []
        state_unlock_value = []
        hero_unlock_key = []
        hero_unlock_value = []
        heroes_status = []
        
        self.file.seek(0)
        for line in self.file :
            ls = line[:-1].split(",")
            if ls[0] == "money" :
                money_line = ls
            elif ls[0] == "potion" :
                potion_line = ls
            elif ls[0] == "state_unlock_key" :
                state_unlock_key = ls
            elif ls[0] == "state_unlock_value" :
                state_unlock_value = ls
            elif ls[0] == "hero_unlock_key" :
                hero_unlock_key = ls
            elif ls[0] == "hero_unlock_value" :
                hero_unlock_value = ls
            elif ls[0] in self.hero_key_checker :
                heroes_status.append(ls)
                
        self.money = int(money_line[1])
        for i in range(1, len(potion_line)) :
            self.hp_potions[i] = int(potion_line[i])
    
        for i in range(1, len(state_unlock_key)) :
            if state_unlock_key[i] in self.state_key_checker :
                # check the key is exist
                value = eval(state_unlock_value[i].title())
                self.state_unlock[state_unlock_key[i]] = value
        for i in range(1, len(hero_unlock_key)) :
            if hero_unlock_key[i] in self.hero_key_checker :
                value = eval(hero_unlock_value[i].title())
                self.hero_unlock[hero_unlock_key[i]] = value
        for status in heroes_status :
            hero = status[0]
            CC.hero_lib[hero].getStatus(status)
        self.file.close()
    def encode(self) :
        self.file = open(self.fileRoot + self.file_name, "w")
        money_line = "money," + str(self.money) + "\n"
        potion_line = "potion," + ",".join([str(i) for i in self.hp_potions[1:]]) + "\n"
        state_key_line = "state_unlock_key," + ",".join(self.state_key_checker) + "\n"
        state_value_line = "state_unlock_value,"
        for key in self.state_key_checker :
            state_value_line += str(self.state_unlock[key]) + ","
        state_value_line += "\n"
        hero_key_line = "hero_unlock_key," + ",".join(self.hero_key_checker) + "\n"
        hero_value_line = "hero_unlock_value,"
        for key in self.hero_key_checker :
            hero_value_line += str(self.hero_unlock[key]) + ","
        hero_value_line += "\n"
        hero_lines = []
        for hero in self.hero_key_checker :
            line = CC.hero_lib[hero].getEncode() + "\n"
            hero_lines.append(line)
        encode_lines = [money_line, potion_line, state_key_line, state_value_line, hero_key_line, hero_value_line]
        encode_lines.extend(hero_lines)
        self.file.writelines(encode_lines)
        self.file.close()
if __name__ == "__main__" :
    f = open("file\save1.csv", "r+")
    p1 = Player(f)