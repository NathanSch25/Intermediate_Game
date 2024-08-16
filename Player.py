#import random
import Element
from dotenv import load_dotenv, find_dotenv
import os
from pymongo import MongoClient
load_dotenv(find_dotenv())
#temperorary
password = ""

#establising connection to DB
#password = os.environ.get("MONGODB_PWD")
connection_string = f"mongodb+srv://nathanschober25:{password}@vio.ei7bb.mongodb.net/?retryWrites=true&w=majority&appName=Vio"
client = MongoClient(connection_string)
dbs = client["Vio"]

#assigning clusters to global variables
player_cluster = dbs.player
item_cluster = dbs.Items

#universal functions
def GetItemStat(itemName, feild):
    columns = {feild: 1}
    item = item_cluster.find_one({"user_name": itemName}, columns)
    item = item[feild]
    return item 
def GetPlayerStat(playerName, feild):
    columns = {feild: 1}
    Stat = player_cluster.find_one({"user_name": playerName}, columns)
    Stat = Stat[feild]
    return Stat

#classes
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
    "inventory": [["hotBar"]["Stash"]],
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
            "inventory": [[None],[None]],
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
        return GetPlayerStat(self.name, "lvl")
    def CurrExp(self):
        return GetPlayerStat(self.name, "curr_exp")  
    def CurrPoints(self):
        return GetPlayerStat(self.name, "lvl_points")    
    def Health(self):
        return GetPlayerStat(self.name, "curr_health") 
    def str(self):
        return GetPlayerStat(self.name, "base_strength")
    def CurrFloor(self):
        return GetPlayerStat(self.name, "curr_floor")
    def CurrElmnt(self):
        return GetPlayerStat(self.name, "element")
    
    def Stash(self):
        return (self.inventory).Stash()
    def HotBar(self):
        return (self.inventory).HotBar()
    def Inventory(self):
        print("HotBar: ", (self.inventory).HotBar())
        return (self.inventory).Stash() 
#mutators
    def IncHealth(self, inc):
        max = GetPlayerStat(self.name, "max_health")
        curr = GetPlayerStat(self.name, "curr_health")
        
        if ((curr + inc) <= max):
            player_cluster.update_one({"user_name": self.name}, {"$inc": {"curr_health": inc}})
        else:
            player_cluster.update_one({"user_name": self.name}, {"$set": {"curr_health": max}})
    def IncArmor(self, inc):
        max = GetPlayerStat(self.name, "max_armor")
        curr = GetPlayerStat(self.name, "curr_armor")
        
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
        armor = max = GetPlayerStat(self.name, "curr_armor")
        
        armor -= damage
        if armor <= 0:
            player_cluster.update_one({"user_name": self.name}, {"$set": {"curr_armor": 0}})
            temp = 0
            while armor != 0:
                armor = armor + 1
                temp = temp + 1
            player_cluster.update_one({"user_name": self.name}, {"$inc": {"curr_health": (-abs(temp))}}) 
    def Stats(self):
        health = GetPlayerStat(self.name, "curr_health")
        armor = GetPlayerStat(self.name, "curr_armor")
        strength = GetPlayerStat(self.name, "base_strength")
        element = GetPlayerStat(self.name, "element")
        
        print(self.name, " health is", health)
        print(self.name, " armor is", armor)
        print(self.name, " streangth is", strength)
        print(self.name, " Elemental afinity is: ", element)        
    def Attack(self, opponentElmnt):
        element = GetPlayerStat(self.name, "element") 
        strength = GetPlayerStat(self.name, "base_strength") 
        
        elmnt = Element.Elements()
        return elmnt.Check(element, opponentElmnt) + strength   
    def Heal(self):
        max = GetPlayerStat(self.name, "max_health")
        lvl = GetPlayerStat(self.name, "lvl")
        player_cluster.update_one({"user_name": self.name}, {"$inc": {"curr_health": lvl}})
        curr = GetPlayerStat(self.name, "curr_health")
        
        if curr > max:
            player_cluster.update_one({"user_name": self.name}, {"$set": {"curr_health": max}})          
    def Revive(self):
        max = GetPlayerStat(self.name, "max_health")
        player_cluster.update_one({"user_name": self.name}, {"$set": {"curr_health": max}})
    def Block(self):
        lvl = GetPlayerStat(self.name, "lvl")
        player_cluster.update_one({"user_name": self.name}, {"inc": {"curr_armor": lvl}})
        
class ItemSearch:
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
        "description": ""
    }
    '''
    def __init__(self, name):
        self.name = name
    
    #Getters
    def type(self):
        return GetItemStat(self.name, "type")
    def lvl_needed(self):
        return GetItemStat(self.name, "lvl_needed")
    def element(self):
        return GetItemStat(self.name, "element")
    def base_dmg(self):
        return GetItemStat(self.name, "base_dmg")
    def armor_buff(self):
        return GetItemStat(self.name, "armor_buff")
    def health_buff(self):
        return GetItemStat(self.name, "health_buff")
    def element_buff(self):
        return GetItemStat(self.name, "element_buff")
    def damage_buff(self):
        return GetItemStat(self.name, "damage_buff")
    def description(self):
        return GetItemStat(self.name, "description")
    
    #mutators
    def CreateItem(self):
        document = {         
            "name": str(input("name: ")),
            "type": str(input("type (Weapon, Helmet, Chest, Leggings, Item): ")),
            "lvl_needed": int(input("lvl needed: ")),
            "element": str(input("element: ")),
            "base_dmg": int(input("base damage: ")),
            "armor_buff": int(input("armor buff: ")),
            "health_buff": int(input("health buff: ")),
            "element_buff": int(input("element_buff: ")),
            "damage_buff": int(input("damage_buff: ")),
            "description": str(input("description: "))
        }
        item_cluster.insert_one(document)


