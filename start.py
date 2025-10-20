import math
import random
import arcade
from fight import *
from enemy import *
from Item import *
from Competence import *
from player import Player

# --- Constantes du jeu ---
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 700
SCREEN_TITLE = "Caméra centrée sur le joueur (ZQSD)"
PLAYER_SPEED = 3

GAUCHE = arcade.key.Q
DROITE =arcade.key.D
HAUT = arcade.key.Z
BAS = arcade.key.S
ATK = arcade.key.KEY_1
COMP1 = arcade.key.KEY_2
COMP2 = arcade.key.KEY_3
ESQUIVE = arcade.key.SPACE


class MyGame(arcade.Window):
    """Classe principale du jeu"""
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE, resizable=True)

        # --- Caméras ---
        self.camera = arcade.Camera2D()       # Caméra du monde
        self.gui_camera = arcade.Camera2D()   # Caméra pour le HUD (interface)

        # --- Joueur ---
        self.player_sprite = None
        self.enemy = None
        self.player_texture = ":resources:images/animated_characters/male_person/malePerson_idle.png"
        self.enemy_texture = ":resources:images/enemies/slimeBlue.png"
        self.enemy2_texture = ":resources:images/enemies/bee.png"

        self.tick = 0
        self.atk_tick = 0
        self.comp1_tick = 0
        self.comp2_tick = 0

        self.comp1_active = 0
        self.comp2_active = 0

        self.lost = False

        # --- Entrées clavier ---
        self.keys_pressed = {"z": False, "q": False, "s": False, "d": False, "atk" : False, "comp1" : False, "comp2" : False, "dodge" : False}

    def setup(self):
        """Initialisation du jeu"""

        self.spritel = arcade.SpriteList()
        self.enemyl = arcade.SpriteList()
        self.entityl = []


        self.player = Player()
        self.player.addWeapon(Weapon("sword", 10, 100, 2, 40))
        self.player.addTorso(Armor("plastron", 1, "commun", 50))
        self.player.comp1 = Attaque_Rapide()

        self.player_sprite = arcade.Sprite(self.player_texture, 0.5)
        self.spritel.append(self.player_sprite)

        for _ in range(3):
            self.create_entity("wolf")
        for _ in range(2):
            self.create_entity("pillar")

    
        self.player_sprite.center_x = 400
        self.player_sprite.center_y = 400

        # Fond de couleur
        arcade.set_background_color(arcade.color.DARK_GRAY)

    # --- Dessin ---
    def on_draw(self):
        self.clear()

        # --- Caméra du monde ---
        self.camera.use()

        # Dessiner un "terrain" simple
        arcade.draw_lbwh_rectangle_filled(0, 0, 2000, 2000,arcade.color.DARK_BLUE)

        arcade.draw_circle_outline(self.player_sprite.center_x, self.player_sprite.center_y, self.player.atk_range, arcade.color.ASH_GREY, 2)

        bar_width = 50
        bar_height = 8

        for entity, sprite in self.entityl :
            if entity.pv <= 0:
                self.kill_entity(entity, sprite )
                continue

            health_ratio = entity.pv / entity.max_pv
            bar_x = sprite.center_x -(bar_width/2)
            bar_y = sprite.center_y + 15
            arcade.draw_lbwh_rectangle_filled(bar_x, bar_y, bar_width, bar_height, arcade.color.RED)
            arcade.draw_lbwh_rectangle_filled(bar_x, bar_y, bar_width * health_ratio, bar_height, arcade.color.GREEN)
            arcade.Text(f"{entity.name} lvl {entity.lvl}", bar_x, bar_y + 10, arcade.color.BLACK, 12).draw()

        self.spritel.draw()
        self.enemyl.draw()

        self.stop_comp()


        # --- Caméra GUI ---
        self.gui_camera.use()
        self.draw_hud()

    def draw_hud(self):
        """Affiche la barre de vie, l’arme et le cooldown"""

        arcade.draw_lbwh_rectangle_filled(0, 0, SCREEN_WIDTH, 120, arcade.color.BLACK)

        health_ratio = self.player.pv / self.player.max_pv
        if health_ratio <= 0 : 
            arcade.draw_text("YOU DIED", SCREEN_WIDTH/2 -100, SCREEN_HEIGHT/2, arcade.color.RED_DEVIL, 60, width = 200)
            health_ratio = 0

        bar_width = 400
        bar_height = 20
        bar_x = SCREEN_WIDTH/2 - bar_width/2
        bar_y = 80

        arcade.draw_lbwh_rectangle_filled(bar_x, bar_y, bar_width, bar_height, arcade.color.RED)
        arcade.draw_lbwh_rectangle_filled(bar_x, bar_y, bar_width * health_ratio, bar_height, arcade.color.APPLE_GREEN)
        arcade.draw_lbwh_rectangle_outline(bar_x, bar_y, bar_width, bar_height, arcade.color.BLACK, 2)


        bar_width = 40
        bar_height = 40

        #---------------------------------------- main weapon cooldown ----------------------------------------


        bar_x = SCREEN_WIDTH/2 - 170
        bar_y = 30
        arcade.draw_text(f"{self.player.weapon.name}", bar_x, bar_y - 15, arcade.color.WHITE, 12)

        waiting_time = self.atk_tick - self.tick if  self.atk_tick - self.tick >= 0 else 0
        cooldown = waiting_time/(60/self.player.atk_speed)

        arcade.draw_lbwh_rectangle_filled(bar_x, bar_y, bar_width, bar_height, arcade.color.DARK_GRAY)
        arcade.draw_lbwh_rectangle_filled(bar_x,bar_y, bar_width, bar_height* cooldown, arcade.color.CYAN)

        arcade.draw_lbwh_rectangle_outline(bar_x, bar_y, bar_width, bar_height, arcade.color.BLACK, 2)


        #---------------------------------------- comp 1 cooldown ----------------------------------------


        bar_x = SCREEN_WIDTH/2 - 70
        bar_y = 30
        arcade.draw_text(f"{self.player.comp1.name if self.player.comp1 else "competence 1"}", bar_x, bar_y - 15, arcade.color.WHITE, 12)

        waiting_time = self.comp1_tick - self.tick if  self.comp1_tick - self.tick >= 0 else 0
        cooldown = waiting_time/(60/self.player.atk_speed)

        arcade.draw_lbwh_rectangle_filled(bar_x, bar_y, bar_width, bar_height, arcade.color.DARK_GRAY)
        arcade.draw_lbwh_rectangle_filled(bar_x,bar_y, bar_width, bar_height* cooldown, 
                                          arcade.color.CYAN if self.comp1_active == True else arcade.color.RED_ORANGE)

        arcade.draw_lbwh_rectangle_outline(bar_x, bar_y, bar_width, bar_height, arcade.color.BLACK, 2)


        #---------------------------------------- comp 2 cooldown ----------------------------------------


        bar_x = SCREEN_WIDTH/2 + 30
        bar_y = 30
        arcade.draw_text(f"{self.player.comp2.name if self.player.comp2 else "competence 2"}", bar_x, bar_y - 15, arcade.color.WHITE, 12)

        waiting_time = self.comp2_tick - self.tick if  self.comp2_tick - self.tick >= 0 else 0
        cooldown = waiting_time/(60/self.player.atk_speed)

        arcade.draw_lbwh_rectangle_filled(bar_x, bar_y, bar_width, bar_height, arcade.color.DARK_GRAY)
        arcade.draw_lbwh_rectangle_filled(bar_x,bar_y, bar_width, bar_height* cooldown, 
                                          arcade.color.CYAN if self.comp1_active == True else arcade.color.RED_ORANGE)

        arcade.draw_lbwh_rectangle_outline(bar_x, bar_y, bar_width, bar_height, arcade.color.BLACK, 2)


        #---------------------------------------- dodge cooldown ----------------------------------------


        bar_x = SCREEN_WIDTH/2 + 130
        bar_y = 30
        arcade.draw_text("Esquive", bar_x, bar_y - 15, arcade.color.WHITE, 12)

        waiting_time = self.atk_tick - self.tick if  self.atk_tick - self.tick >= 0 else 0
        cooldown = waiting_time/(60/self.player.atk_speed)

        arcade.draw_lbwh_rectangle_filled(bar_x, bar_y, bar_width, bar_height, arcade.color.DARK_GRAY)
        arcade.draw_lbwh_rectangle_filled(bar_x,bar_y, bar_width, bar_height* cooldown, arcade.color.CYAN)

        arcade.draw_lbwh_rectangle_outline(bar_x, bar_y, bar_width, bar_height, arcade.color.BLACK, 2)


    def stop_comp(self):
        if self.player.comp1 and self.comp1_active and self.comp1_tick < self.tick :
            self.player.comp1.stop(self.player)
            self.comp1_active = False
        if self.player.comp2 and self.comp2_active and self.comp2_tick < self.tick :
            self.player.comp2.stop(self.player)
            self.comp2_active = False

    def _comp_ok(self, comp):
        competence = self.player.comp1 if comp == 1 else self.player.comp2
        if competence :
            return 1 if competence.cooldown < self.tick else 0
        else :
            return 0

    def on_update(self, delta_time: float):
        if self.lost :
            return
        dx = 0
        dy = 0
        if self.keys_pressed["z"]:
            dy += PLAYER_SPEED
        if self.keys_pressed["s"]:
            dy -= PLAYER_SPEED
        if self.keys_pressed["q"]:
            dx -= PLAYER_SPEED
        if self.keys_pressed["d"]:
            dx += PLAYER_SPEED
        if self.keys_pressed["atk"] and self.atk_tick < self.tick:
            self.atk_tick = self.tick + (60/self.player.atk_speed)
            self.player_attack()

        if self.keys_pressed["comp1"] and self._comp_ok(1):
            cooldown = self.tick + (60*self.player.comp1.default_cooldown + 60*self.player.comp1.duration)
            self.comp1_tick = self.tick + 60*self.player.comp1.duration
            self.comp1_active = True
            self.player.comp1.activate(self.player, cooldown)

        if self.keys_pressed["comp2"] and self._comp_ok(2):
            cooldown = self.tick + (60*self.player.comp2.default_cooldown + 60*self.player.comp2.duration)
            self.comp2_tick = self.tick + 60*self.player.comp2.duration
            self.comp1_active = False
            self.player.comp2.activate(self.player, cooldown)

        self.player_sprite.center_x += dx
        self.player_sprite.center_y += dy

        # Centrer la caméra sur le joueur
        self.camera.position = (self.player_sprite.center_x, self.player_sprite.center_y)


        for entity, sprite in self.entityl:
            self.follow_player(sprite, entity)
            if(entity.atk_cooldown < self.tick):
                entity.atk_cooldown = self.tick + 60*(1/entity.atk_speed)
                self.enemy_attack(entity, sprite)
            if self.player.pv <= 0 :
                self.lost = True 

        self.tick +=1


    def create_entity(self, type, gen_zone= [0,0,300,300]):
        """create an entity of the desired type

        Args:
            type (_type_): describe the type of the entity
            gen_zone (list, optional): describes a rectangle in with the entity will appear, defined to [x_min, y_min, x_max, y_max]. Defaults to [0,0,100,100].
        """
        match type:
            case "wolf":
                enemy = Wolf(40, 20, 1, 50,1)
                enemy_sprite = arcade.Sprite(self.enemy_texture, 0.5)

            case "pillar":
                enemy = Scavenger(40, 20, 1, 50,1)
                enemy.addWeapon(Weapon("sword", 10, 80, 1, 20))
                enemy_sprite = arcade.Sprite(self.enemy2_texture, 0.5)

        self.enemyl.append(enemy_sprite)
        self.entityl.append([enemy, enemy_sprite])
        enemy_sprite.center_x = random.randint(gen_zone[0], gen_zone[2])
        enemy_sprite.center_y = random.randint(gen_zone[1], gen_zone[3])
        while arcade.check_for_collision_with_list(enemy_sprite, self.enemyl) != [] :
            enemy_sprite.center_x = random.randint(gen_zone[0], gen_zone[2])
            enemy_sprite.center_y = random.randint(gen_zone[1], gen_zone[3])


    def follow_player(self, sprite, entity):
        dest_x = self.player_sprite.center_x
        dest_y = self.player_sprite.center_y

        x_diff = dest_x - sprite.center_x
        y_diff = dest_y - sprite.center_y
        angle = math.atan2(y_diff, x_diff)

        change_x = math.cos(angle) * entity.speed
        change_y = math.sin(angle) * entity.speed
        sprite.center_x += change_x
        sprite.center_y += change_y 
        collisions = arcade.check_for_collision_with_list(sprite, self.enemyl)
        collisions += arcade.check_for_collision_with_list(sprite, self.spritel)
        if (collisions):
            sprite.center_x -= change_x
            sprite.center_y -= change_y
             

    def get_knockback(self,sprite, atker_sprite, knockback):
        dest_x = sprite.center_x + (sprite.center_x - atker_sprite.center_x)
        dest_y = sprite.center_y + (sprite.center_y - atker_sprite.center_y)

        x_diff = dest_x - sprite.center_x
        y_diff = dest_y - sprite.center_y
        angle = math.atan2(y_diff, x_diff)

        change_x = math.cos(angle) * knockback
        change_y = math.sin(angle) * knockback
        
        sprite.center_x += change_x
        sprite.center_y += change_y
        while arcade.check_for_collision_with_list(sprite, self.enemyl) != [] :
            sprite.center_x += change_x
            sprite.center_y += change_y

    def player_attack(self):
        for entity, sprite in self.entityl :
            if(arcade.get_distance_between_sprites(sprite, self.player_sprite) <= self.player.atk_range):
                attack(self.player, entity)
                if (self.player.weapon):
                    if (self.player.weapon.knockback != 0):
                        self.get_knockback(sprite, self.player_sprite, self.player.weapon.knockback)


    def enemy_attack(self, enemy, sprite):
        if (arcade.get_distance_between_sprites(sprite, self.player_sprite) <= enemy.atk_range):
            attack(enemy, self.player)
            if (enemy.weapon):
                if (enemy.weapon.knockback != 0):
                    self.get_knockback(self.player_sprite, sprite, enemy.weapon.knockback)

    def kill_entity(self, entity, sprite):
        del self.entityl[self.entityl.index([entity, sprite])]
        del entity
        self.enemyl.remove(sprite)
        del sprite

    # --- Gestion du clavier ---
    def on_key_press(self, key, modifiers):
        if key == HAUT:
            self.keys_pressed["z"] = True
        elif key == BAS:
            self.keys_pressed["s"] = True
        elif key == GAUCHE:
            self.keys_pressed["q"] = True
        elif key == DROITE:
            self.keys_pressed["d"] = True
        elif key == ATK:
            self.keys_pressed["atk"] = True
        elif key == COMP1:
            self.keys_pressed["comp1"] = True
        elif key == COMP2:
            self.keys_pressed["comp2"] = True
        elif key == ESQUIVE:
            self.keys_pressed["dodge"] = True

    def on_key_release(self, key, modifiers):
        if key == HAUT:
            self.keys_pressed["z"] = False
        elif key == BAS:
            self.keys_pressed["s"] = False
        elif key == GAUCHE:
            self.keys_pressed["q"] = False
        elif key == DROITE:
            self.keys_pressed["d"] = False
        elif key == ATK:
            self.keys_pressed["atk"] = False
        elif key == COMP1:
            self.keys_pressed["comp1"] = False
        elif key == COMP2:
            self.keys_pressed["comp2"] = False
        elif key == ESQUIVE:
            self.keys_pressed["dodge"] = False


# --- Lancer le jeu ---
if __name__ == "__main__":
    game = MyGame()
    game.setup()
    arcade.run()
