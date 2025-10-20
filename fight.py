def attack(atker, defender):
    dmg = atker.atk
    dmg = dmg/((defender.def_ratio + 100)/100)
    defender.pv =  defender.pv - dmg