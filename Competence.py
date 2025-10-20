class Competence():

    def __init__(self):
        self.name = ""

    def __str__(self):
        return self.name


class Attaque_Rapide(Competence):

    def __init__(self):
        self.default_cooldown = 15
        self.cooldown = 0
        self.duration = 5
        self.name = "Attaque rapide"
        self.acceleration = 2
    
    def activate(self, player, cooldown):
        player.atk_speed = player.atk_speed*2
        self.cooldown = cooldown

    def stop(self, player):
        player.atk_speed = player.atk_speed/2