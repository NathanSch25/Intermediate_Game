#import random
import Element
from dotenv import load_dotenv, find_dotenv
import os
from pymongo import MongoClient
load_dotenv(find_dotenv())
MONGODB_PWD = "#######"

#password = os.environ.get("MONGODB_PWD")
connection_string = f"mongodb+srv://nathanschober25:{MONGODB_PWD}@vio.ei7bb.mongodb.net/?retryWrites=true&w=majority&appName=Vio"
client = MongoClient(connection_string)
dbs = client["Vio"]
player_cluster = dbs.player

class Player:
    """ player_cluster format{
    "user_name": "",
    "max_health": 1,
    "curr_health": 1,
    "max_armor": 1,
    "curr_armor": 1,
    "base_strength": 1,
    "curr_strength": 1,
    "element": "",
    "curr_exp": 1,
    "lvl": 1,
    "curr_floor": 1,
    "inventory": [[][][][][]],
    "lvl_points": 1
        inventory items: [name, lvl, type]
    }
    """
    def __init__(self, name = "",maxHealth = 1, maxArmor = 1, baseStreangth = 1,element = "Terra",lvl = 1, currExp = 0):
        self.name = name
        # self.health = maxHealth
        # self.maxHealth = maxHealth
        # self.armor = maxArmor
        # self.maxArmor = maxArmor
        # self.element = element
        # self.basestreangth = baseStreangth
        # self.lvl = lvl
        # self.currExp = currExp
        # self.lvlPoints = 0
        # self.currFloor = 1
        self.inventory = Inventory()
        if self.name != "null":
            document = {
            "user_name": name,
            "max_health": maxHealth,
            "curr_health": maxHealth,
            "max_armor": maxArmor,
            "curr_armor": maxArmor,
            "base_strength": baseStreangth,
            "curr_strength": baseStreangth,
            "element": element,
            "curr_exp": currExp,
            "lvl": lvl,
            "curr_floor": 1,
            "inventory": [[None],[None],[None],[None],[None]],
            "lvl_points": 0
            }
            player_cluster.insert_one(document)
               
#geters
    def FindUser(self, userName):
        if player_cluster.find_one({"user_name": userName}):
            return True
        else:
            return False        
    def Lvl(self):
        #player_cluster.find_one({"user_name": self.name})
        columns = {"lvl": 1}
        lvl = player_cluster.find_one({"user_name": self.name}, columns)
        lvl = lvl["lvl"]
        return lvl
    def CurrExp(self):
        columns = {"curr_exp": 1}
        exp = player_cluster.find_one({"user_name": self.name}, columns) 
        exp = exp["curr_exp"]
        return exp  
    def CurrPoints(self):
        columns = {"lvl_points": 1}
        points = player_cluster.find_one({"user_name": self.name}, columns) 
        points = points["lvl_points"]
        return points    
    def Health(self):
        columns = {"curr_health": 1}
        health = player_cluster.find_one({"user_name": self.name}, columns)
        health = health["curr_health"]
        return health  
    def str(self):
        columns = {"base_strength": 1}
        strength = player_cluster.find_one({"user_name": self.name}, columns)
        strength = strength("base_strength")
        return strength
    def CurrFloor(self):
        columns = {"curr_floor": 1}
        floor = player_cluster.find_one({"user_name": self.name}, columns)
        floor = floor["curr_floor"]
        return floor
    def CurrElmnt(self):
        columns = {"element": 1}
        element = player_cluster.find_one({"user_name": self.name}, columns)
        element = element["element"]
        return element
    
    def Stash(self):
        return (self.inventory).Stash()
    def HotBar(self):
        return (self.inventory).HotBar()
    def Inventory(self):
        print("HotBar: ", (self.inventory).HotBar())
        return (self.inventory).Stash() 
#mutators
    def IncHealth(self, inc):
        columns = {"max_health": 1}
        max = player_cluster.find_one({"user_name": self.name}, columns)
        max = max["max_health"]
        columns = {"curr_health": 1}
        curr = (player_cluster.find_one({"user_name": self.name}, columns))
        curr = curr["curr_health"]
        
        if ((curr + inc) <= max):
            player_cluster.update_one({"user_name": self.name}, {"$inc": {"curr_health": inc}})
        else:
            player_cluster.update_one({"user_name": self.name}, {"$set": {"curr_health": max}})
    def IncArmor(self, inc):
        columns = {"max_armor": 1}
        max = player_cluster.find_one({"user_name": self.name}, columns)
        max = max["max_armor"]
        columns = {"curr_armor": 1}
        curr = (player_cluster.find_one({"user_name": self.name}, columns))
        curr = curr["curr_armor"]
        
        if ((curr + inc) <= max):
            player_cluster.update_one({"user_name": self.name}, {"$inc": {"curr_armor": inc}})
        else:
            player_cluster.update_one({"user_name": self.name}, {"$set": {"curr_armor": max}})
    def Incstr(self, inc):
        player_cluster.update_one({"user_name": self.name}, {"$inc": {"curr_streangth": inc}})
    def ExpGain(self, inc):
        player_cluster.update_one({"user_name": self.name}, {"$inc": {"curr_exp": inc}})
        collumn = {"curr_exp": 1}
        curr = player_cluster.find_one({"user_name": self.name}, collumn)
        curr = curr["curr_exp"]
        
        if curr >= 100:
            player_cluster.update_one({"user_name": self.name}, {"$inc": {"lvl": 1}})
            player_cluster.update_one({"user_name": self.name}, {"$set": {"curr_exp": 0}})
            player_cluster.update_one({"user_name": self.name}, {"$inc": {"lvl_points": 1}})
    def ChangeFloor(self, inc):
        player_cluster.update_one({"user_name": self.name}, {"$inc": {"curr_floor": inc}})      
    def Kill(self):
        player_cluster.update_one({"user_name": self.name}, {"$set": {"curr_health": 0}}) 
    def ChangeElmnt(self, newElmnt):
        player_cluster.update_one({"user_name": self.name}, {"$set": {"element": newElmnt}})          
    
    def AddItem(self, item):
       (self.inventory).AddItem(item)
    def RemoveItem(self, item):
       (self.inventory).RemoveItem(item)  

#fight Code
    def Hurt(self, damage):
        collumn = {"curr_armor": 1}
        armor = player_cluster.find_one({"user_name": self.name}, collumn)
        armor = armor["curr_armor"]
        
        armor -= damage
        if armor <= 0:
            player_cluster.update_one({"user_name": self.name}, {"$set": {"curr_armor": 0}})
            temp = 0
            while armor != 0:
                armor = armor + 1
                temp = temp + 1
            player_cluster.update_one({"user_name": self.name}, {"$inc": {"curr_health": (-abs(temp))}}) 
    def Stats(self):
        collumn = {"curr_health": 1}
        health = player_cluster.find_one({"user_name": self.name}, collumn)
        health = health["curr_health"]
        collumn = {"curr_armor": 1}
        armor = player_cluster.find_one({"user_name": self.name}, collumn)
        armor = armor["curr_armor"]
        collumn = {"base_strength": 1}
        strength = player_cluster.find_one({"user_name": self.name}, collumn) 
        strength = strength["base_strength"]
        collumn = {"element": 1}
        element = player_cluster.find_one({"user_name": self.name}, collumn)
        element = element["element"]
        
        print(self.name, " health is", health)
        print(self.name, " armor is", armor)
        print(self.name, " streangth is", strength)
        print(self.name, " Elemental afinity is: ", element)        
    def Attack(self, opponentElmnt):
        collumn = {"element": 1}
        element = player_cluster.find_one({"user_name": self.name}, collumn)
        element = element["element"]
        collumn = {"base_strength": 1}
        strength = player_cluster.find_one({"user_name": self.name}, collumn) 
        strength = strength["base_strength"] 
        
        elmnt = Element.Elements()
        return elmnt.Check(element, opponentElmnt) + strength   
    def Heal(self):
        collumn = {"max_health": 1}
        max = player_cluster.find_one({"user_name": self.name}, collumn)
        max = max["max_health"]
        collumn = {"lvl": 1}
        lvl = player_cluster.find_one({"user_name": self.name}, collumn) 
        lvl = lvl["lvl"] 
        player_cluster.update_one({"user_name": self.name}, {"$inc": {"curr_health": lvl}})
        collumn = {"curr_health": 1}
        curr = player_cluster.find_one({"user_name": self.name}, {"user_name": self.name}, collumn)
        curr = curr["curr_health"]
        
        if curr > max:
            player_cluster.update_one({"user_name": self.name}, {"$set": {"curr_health": max}})          
    def Revive(self):
        collumn = {"max_health": 1}
        max = player_cluster.find({"user_name": self.name}, collumn)
        player_cluster.update_one({"user_name": self.name}, {"$set": {"curr_health": max}})
    def Block(self):
        collumn = {"lvl": 1}
        lvl = player_cluster.find({"user_name": self.name}, collumn)
        lvl = lvl["lvl"]
        player_cluster.update_one({"user_name": self.name}, {"inc": {"curr_armor": lvl}})
        
class Inventory:
    #Types == Weapon, Helmet, Chest, Leggings, Item
    ''' item format in cluster{
        "name": "",
        "type": "",
        "lvl_needed": 1,
        "element": "",
        "base_dmg": 1,
        "armor_buff": 1,
        "health_buff": 1,
        "element_buff": 1,
        "damage_buff": 1,
        "description": "",
        "active": True
    }
    
    '''
    def __init__(self):
        self.stash = [[None], [None], [None], [None], [None]]
        self.hotBar = [None, None, None, None, None]
    
    def Stash(self):
        return self.stash
    def HotBar(self):
        return self.hotBar
    
    
    def AddItem(self, item):
        match item[0]:
            case "Weapon":
                ((self.stash)[0]).append(item)
            case "Helmet":
                ((self.stash)[1]).append(item)
            case "Chest":
                ((self.stash)[2]).append(item)
            case "Leggings":
                ((self.stash)[3]).append(item)
            case "Item":
                ((self.stash)[4]).append(item)
    def RemoveItem(self, item):
        match item[0]:
            case "Weapon":
                for i in (self.stash)[0]:
                    if i == item[1]:
                        (self.stash)[0].pop(i)
            case "Helmet":
                for i in (self.stash)[1]:
                    if i == item[1]:
                        (self.stash)[1].pop(i)
            case "Chest":
                for i in (self.stash)[2]:
                    if i == item[1]:
                        (self.stash)[2].pop(i)
            case "Leggings":
                for i in (self.stash)[3]:
                    if i == item[1]:
                        (self.stash)[3].pop(i)
            case "Item":
                for i in (self.stash)[4]:
                    if i == item[1]:
                        (self.stash)[4].pop(i)



