import time
import random

class Elements:
    def __init__(self):
        return
        
    def Strong(self):
        return(3)
    def Weak(self):
        return(-1)
    
    def Check(self, playerElmnt, MonsterElmnt):
        match playerElmnt:
            case "Terra":
                match MonsterElmnt:
                    case "Terra":
                        return 0
                    case "Ignis":
                        return  self.Strong()
                    case "Aqua":
                        return 0
                    case "Caeli":
                        return 0
                    case "Lux":
                        return 0
                    case "Nox":
                        return 0
            case "Ignis":
                match MonsterElmnt:
                    case "Terra":
                        return self.Weak()
                    case "Ignis":
                        return self.Weak()
                    case "Aqua":
                        return 0
                    case "Caeli":
                        return self.Strong()
                    case "Lux":
                        return 0
                    case "Nox":
                        return self.Strong()
            case "Aqua":
                match MonsterElmnt:
                    case "Terra":
                        return 0
                    case "Ignis":
                        return 0
                    case "Aqua":
                        return 0
                    case "Caeli":
                        return 0
                    case "Lux":
                        return 0
                    case "Nox":
                        return 0
            case "Caeli":
                match MonsterElmnt:
                    case "Terra":
                        return self.Weak()
                    case "Ignis":
                        return 0
                    case "Aqua":
                        return 0
                    case "Caeli":
                        return 0
                    case "Lux":
                        return 0
                    case "Nox":
                        return 0
            case "Lux":
                match MonsterElmnt:
                    case "Terra":
                        return 0
                    case "Ignis":
                        return 0
                    case "Aqua":
                        return 0
                    case "Caeli":
                        return 0
                    case "Lux":
                        return 0
                    case "Nox":
                        return self.Strong()
            case "Nox":
                match MonsterElmnt:
                    case "Terra":
                        return 0
                    case "Ignis":
                        return 0
                    case "Aqua":
                        return 0
                    case "Caeli":
                        return 0
                    case "Lux":
                        return self.Weak()
                    case "Nox":
                        return 0