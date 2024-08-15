import random
import Element

class Monster:
    def __init__(self, name = "tom",maxHealth = 1,maxArmor = 1,streangth = 1,element = "Terra",lvl = 1):
        self.name = name
        self.health = maxHealth
        self.maxHealth = maxHealth
        self.armor = maxArmor
        self.maxArmor = maxArmor
        self.element = element
        self.baseStreangth = streangth
        self.lvl = lvl
    def Generator(self, floor):
        self.lvl = floor
        self.health = random.randint(2,5) + self.lvl
        self.maxHealth = self.health
        self.armor = random.randint(2,5) + self.lvl
        self.maxArmor = self.armor
        self.baseStreangth = random.randint(2,5) + self.lvl
        temp = random.randint(1,6)
        match temp:
            case 1:
                self.element = 'Terra'
            case 2:
                self.element = 'Ignis'
            case 3:
                self.element = 'Aqua'
            case 4:
                self.element = 'Caeli'
            case 5:
                self.element = 'Lux'
            case 6:
                self.element = 'Nox'
#Getters    
    def Health(self):
        return(self.health)
    def Inventory(self):
        return self.Inventory    
        return(self.health)    
    def str(self):
        return self.baseStreangth
    def CurrElmnt(self):
        return self.element
    
#mutators
    def IncHealth(self, inc):
        self.maxHealth += inc
    def IncArmor(self, inc):
        self.maxArmor += inc
    def Incstr(self, inc):
        self.baseStreangth += inc
        self.currExp += inc
        if self.currExp == 100:
            self.lvl += 1
            self.currExp = 0
            self.lvlPoints += 1       
    def Kill(self):
        self.health = 0 
    def ChangeElmnt(self, newElmnt):
        self.element = newElmnt
        
#Fight code   
    def Stats(self):
        print(self.name, " health is: ", self.health)
        print(self.name, " armor is: ", self.armor)
        print(self.name, " streangth is: ", self.baseStreangth)
        print(self.name, " Elemental afinity is: ", self.element)
    def Hurt(self, damage):
        self.armor = self.armor - damage
        if self.armor <= 0:
            temp = 0
            while self.armor < 0:
                self.armor = self.armor + 1
                temp = temp + 1
            self.health = self.health - temp        
    def Heal(self):
        self.health += self.lvl
        if self.health > self.maxHealth:
            self.health = self.maxHealth
        #print(self.maxHealth)           
    def Block(self):
         self.armor = self.armor + self.lvl         
    def Attack(self, opponentElmnt):
        elmnt = Element.Elements()
        return elmnt.Check(self.CurrElmnt(), opponentElmnt) + self.baseStreangth