class Enemy():

    def __init__(self, pv, atk, speed, atkSpeed, lvl):
        self.max_pv = pv
        self.pv = pv
        self.atk = atk
        self.speed = speed
        self.atk_speed = atkSpeed
        self.lvl = lvl
        self.sprite = None
        self.detection_zone = 200
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



class wolf(Enemy):

    def __init__(self, pv, atk, atkSpeed, lvl):
        super().__init__(pv, atk, 2, atkSpeed, lvl)



class scavenger(Enemy):

    def __init__(self, pv, atk, atkSpeed, lvl):
        super().__init__(pv, atk, 1, atkSpeed, lvl)



class zombie(Enemy):

    def __init__(self, pv, atk, atkSpeed, lvl):
        super().__init__(pv, atk, 0.8, atkSpeed, lvl)
            
