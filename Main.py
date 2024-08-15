'''
Nathan Schober
June/25/2024 - 
Game
'''

import string
import math
import time
import random
import Monster
import Player
from Element import Elements
user = "999"
floor = 1
    
def battleMenu():
    print("\n\nwhat do you wish to do")
    print("1 - attack")
    print("2 - heal")
    print("3 - run")
    print("4 - block")
    user = int(input())
    return user
def playerGen():
    print("Time to make a charater")
    print("you have a max of 10 points to assign to health, armor, and strangth")
    print("\n type -1 for a random charater or any other # to continue: ")
    temp = int(input())
    if temp == -1:
        totalpoints = 10
        health = random.randint(0,totalpoints)
        totalpoints -= health
        armor = random.randint(0,totalpoints)
        totalpoints -= armor
        streangth = totalpoints
        totalpoints -= streangth
        elmnt = "Terra"
    else:
        health = int(input("how much Health do you want: "))
        armor = int(input("how much Armor do you want: "))
        streangth = int(input("how much streangth do you want: "))
        elmnt = input("What is your preferred element\nTerra - Ignis - Aqua - Caeli - Lux - Nox\n: ")
    name = input("What is your name adventurer: ")
    P1 = Player.Player(name, health, armor, streangth, elmnt)
    return P1
def Battle():
    user = input("\n\n\nif you are ready for a fight press enter \n")
    if user == '':
        monster = Monster.Monster()
        print(1)
        monster.Generator(P1.CurrFloor())
        print(0)
        while (monster.Health() > 0) and (P1.Health() > 0):
            monster.Stats()
            print("\n")
            P1.Stats()
            elmnt = Elements()
            elementAffect = elmnt.Check(P1.CurrElmnt(), monster.CurrElmnt())
            print("Elemental attack is ", elementAffect)
            time.sleep(2)
        
            #user battle choice/effect
            user = battleMenu()
            match user:
                case 1:
                    attack = P1.Attack(monster.CurrElmnt())
                    monster.Hurt(attack)
        
                case 2:
                    P1.Heal()
    
                case 3:
                    P1.Kill()
    
                case 4:
                    P1.Block()
        
            #monster battle choice/effect
            monsterMove = random.randint(1,3)
            match monsterMove:
                case 1:
                    attack = monster.Attack(P1.CurrElmnt())
                    P1.Hurt(attack)
                    
                case 2:
                    monster.Heal()
    
                case 3:
                    monster.Block()
    
        #raises or lowers floor base on outcome of battle   
        if monster.Health() <= 0:
            P1.ChangeFloor(1)
            match elementAffect:
                case 3 :
                    P1.ExpGain(10)
                case 0 :
                    P1.ExpGain(30)
                case -1 :
                    P1.ExpGain(50)
        else:
            P1.ChangeFloor(-1)
            P1.Revive()
    else:
        return
def MainMenu(P1):
    menuOption = -1
    print("\n\ncurent Lvl: ", P1.Lvl())
    print("curent Exp: ", P1.CurrExp())
    print("current Lvl Points: ", P1.CurrPoints())
    while (menuOption < 0) or (menuOption > 4):
        print("\n1 - Fight")
        print("2 - show curent floor")
        print("3 - display inventory")
        print("4 - allocate lvl points")
        menuOption = int(input("What is your choice?"))
        
    return menuOption


#player generation
userName = input("what is your user Name?")
P1 = Player.Player("null",1,1,1)

exists = P1.FindUser(userName)
if exists:
    print("works")
else:   
    P1 = playerGen()

#main menu selection
while user != 0:
    user = MainMenu(P1)
    match user:
        case 1:
            Battle()
        case 2:
            print("current floor: ", P1.CurrFloor())
            time.sleep(2)
        case 3:
            print ("HotBar: ", P1.HotBar())
            Stash = P1.Stash()
            print(Stash)
            print("Weapons: ",Stash[0])
            print("Helms: ",Stash[1])
            print("Chests: ",Stash[2])
            print("Leggings: ",Stash[3])
            print("Items: ",Stash[4])
        
        case 4:
            P1.PointAlocate()
        
        case 5:
            print()
    
        case _:
            print("oh shit") 
    

   
    