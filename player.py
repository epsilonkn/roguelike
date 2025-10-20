class Player():

    def __init__(self):
        self.max_pv = 50
        self.pv = 50
        self.atk = 10
        self.speed = 2
        self.atk_speed = 1
        self.atk_range = 35
        self.lvl = 1
        self.sprite = None
        self.inventory = []
        self.weapon = None
        self.torso = None
        self.def_ratio = 0


    def getAttr(self, attr):
        match attr :
            case "pv" :
                return self.pv
            case "atk" :
                return self.atk
            case "speed" :
                return self.speed
            case "atk_speed" :
                return self.atk_speed
            case "lvl" :
                return self.lvl
            
    
    def addWeapon(self, weapon):
        self.weapon = weapon
        self.atk = weapon.atk
        self.atk_speed = weapon.atk_speed
        self.atk_range = weapon.atk_range

    def addTorso(self, torso):
        self.torso = torso
        self.def_ratio += torso.defense
            
    
    def setAttr(self, attr, val):
        match attr :
            case "pv" :
                self.pv = val
            case "atk" :
                self.atk = val
            case "speed" :
                self.speed = val
            case "atk_speed" :
                self.atk_speed = val

    
    def getInventory(self):
        return self.inventory
    
    def addToInventory(self, item):
        self.inventory.append(item)

    def delFromInventory(self, item):
        del self.inventory[self.inventory.index(item)]