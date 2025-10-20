class Item():

    def __init__(self, name = ""):
        self.name = name


    def __str__(self):
        return self.name


class Armor(Item):

    def __init__(self, name, level, grade, defense):
        super().__init__(name)
        self.lvl = level
        self.grade = grade
        self.defense = defense


class Weapon(Item):

    def __init__(self, name, atk, atk_range, atk_speed, knockback):
        super().__init__(name)
        self.atk = atk
        self.atk_range = atk_range
        self.atk_speed = atk_speed
        self.knockback = knockback



class HeavyWeapon(Weapon):

    def __init__(self, name, atk, atk_range, atk_speed, knockback, knockout):
        super().__init__(name, atk, atk_range, atk_speed, knockback)
        self.knockout = knockout