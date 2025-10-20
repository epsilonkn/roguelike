class Player():

    def __init__(self):
        self.max_pv = 50
        self.pv = 50
        self.speed = 2

        self.atk = 10
        self.atk_speed = 1
        self.atk_range = 35
        self.comp1 = None
        self.comp2 = None
        self.weapon = None
        self.lvl = 1

        self.sprite = None
        self.inventory = []

        self.torso = None
        self.head = None
        self.legs = None
        self.arms = None
        self.gloves = None
        self.def_ratio = 0

            
    
    def addWeapon(self, weapon):
        self.weapon = weapon
        self.atk = weapon.atk
        self.atk_speed = weapon.atk_speed
        self.atk_range = weapon.atk_range

    def addTorso(self, torso):
        self.torso = torso
        self.def_ratio += torso.defense


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
            
    
    def getInventory(self):
        return self.inventory
    
    def addToInventory(self, item):
        self.inventory.append(item)

    def delFromInventory(self, item):
        del self.inventory[self.inventory.index(item)]