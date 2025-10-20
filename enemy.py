class Enemy():

    def __init__(self, pv, atk, speed, atk_speed, atk_range, lvl):
        self.max_pv = pv
        self.pv = pv
        self.atk = atk
        self.speed = speed
        self.atk_speed = atk_speed
        self.atk_range = atk_range
        self.atk_cooldown = 0
        self.lvl = lvl
        self.sprite = None
        self.detection_zone = 200
        self.def_ratio = 0
        self.weapon = None
        self.torso = None
        self.head = None
        self.legs = None
        self.arms = None
        self.gloves = None


    def addTorso(self, torso):
        self.torso = torso
        self.def_ratio += torso.defense
    
    def addWeapon(self, weapon):
        self.weapon = weapon
        self.atk = weapon.atk
        self.atk_speed = weapon.atk_speed
        self.atk_range = weapon.atk_range

    
    def addHead(self, head):
        self.head = head
        self.def_ratio += head.defense

    
    def addLegs(self, legs):
        self.legs = legs
        self.def_ratio += legs.defense


    def addArms(self, arms):
        self.arms = arms
        self.def_ratio += arms.defense


    def addGloves(self, gloves):
        self.gloves = gloves
        self.def_ratio += gloves.defense


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
            case "detection_zone":
                return self.detection_zone
            
    
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



class Wolf(Enemy):

    def __init__(self, pv, atk, atk_speed, atk_range, lvl):
        super().__init__(pv, atk, 2, atk_speed, atk_range, lvl)
        self.name = "Loup"



class Scavenger(Enemy):

    def __init__(self, pv, atk, atk_speed, atk_range, lvl):
        super().__init__(pv, atk, 1.5, atk_speed, atk_range, lvl)
        self.name = "Pillars"



class Zombie(Enemy):

    def __init__(self, pv, atk, atk_speed, atk_range, lvl):
        super().__init__(pv, atk, 0.8, atk_speed, atk_range, lvl)
        self.name = "Zombie"
            
