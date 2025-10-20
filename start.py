import math
import random
import arcade
from fight import *
from enemy import *
from Item import *
from player import Player

# --- Constantes du jeu ---
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Caméra centrée sur le joueur (ZQSD)"
PLAYER_SPEED = 3


class MyGame(arcade.Window):
    """Classe principale du jeu"""
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        # --- Caméras ---
        self.camera = arcade.Camera2D()       # Caméra du monde
        self.gui_camera = arcade.Camera2D()   # Caméra pour le HUD (interface)

        # --- Joueur ---
        self.player_sprite = None
        self.enemy = None
        self.player_texture = ":resources:images/animated_characters/male_person/malePerson_idle.png"
        self.enemy_texture = ":resources:images/enemies/slimeBlue.png"

        self.tick = 0
        self.atk_tick = 0

        # --- Entrées clavier ---
        self.keys_pressed = {"z": False, "q": False, "s": False, "d": False, "atk" : False}

    def setup(self):
        """Initialisation du jeu"""

        self.spritel = arcade.SpriteList()
        self.enemyl = arcade.SpriteList()
        self.entityl = []


        self.player = Player()
        self.player.addWeapon(Weapon("sword", 10, 100, 2, 40))
        self.player.addTorso(Armor("plastron", 1, "commun", 50))

        self.player_sprite = arcade.Sprite(self.player_texture, 0.5)
        self.spritel.append(self.player_sprite)

        for _ in range(5):
            self.create_entity("wolf")

    
        self.player_sprite.center_x = 400
        self.player_sprite.center_y = 400

        # Fond de couleur
        arcade.set_background_color(arcade.color.BLACK)

    # --- Dessin ---
    def on_draw(self):
        self.clear()

        # --- Caméra du monde ---
        self.camera.use()

        # Dessiner un "terrain" simple
        arcade.draw_lbwh_rectangle_filled(0, 0, 2000, 2000,arcade.color.DARK_BLUE)

        bar_width = 50
        bar_height = 8
        bar_x = self.player_sprite.center_x -(bar_width/2)
        bar_y = self.player_sprite.center_y + 15  # juste au-dessus du sprite

        # Calcul de la proportion de vie
        health_ratio = self.player.pv / self.player.max_pv

        arcade.draw_circle_outline(self.player_sprite.center_x, self.player_sprite.center_y, self.player.atk_range, arcade.color.ASH_GREY, 2)

        arcade.draw_lbwh_rectangle_filled(bar_x, bar_y, bar_width, bar_height, arcade.color.RED)
        arcade.draw_lbwh_rectangle_filled(bar_x,bar_y,bar_width * health_ratio,bar_height,arcade.color.GREEN)

        for entity, sprite in self.entityl :

            if entity.pv <= 0:
                self.kill_entity(entity, sprite )
                continue
            health_ratio = entity.pv / entity.max_pv
            bar_x = sprite.center_x -(bar_width/2)
            bar_y = sprite.center_y + 15
            arcade.draw_lbwh_rectangle_filled(bar_x, bar_y, bar_width, bar_height, arcade.color.RED)
            arcade.draw_lbwh_rectangle_filled(bar_x, bar_y, bar_width * health_ratio, bar_height, arcade.color.GREEN)

        # Dessiner le joueur
        self.spritel.draw()
        self.enemyl.draw()

        # --- Caméra GUI ---
        self.gui_camera.use()


    # --- Mise à jour ---
    def on_update(self, delta_time: float):
        # Déplacement selon les touches
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
            self.atk_tick = self.tick + 60*(1/self.player.atk_speed)
            self.player_attack()

        self.player_sprite.center_x += dx
        self.player_sprite.center_y += dy

        # Centrer la caméra sur le joueur
        self.camera.position = (self.player_sprite.center_x, self.player_sprite.center_y)


        for entity, sprite in self.entityl:
            self.follow_player(sprite, entity)

        self.tick +=1


    def create_entity(self, type, gen_zone= [0,0,300,300]):
        """create an entity of the desired type

        Args:
            type (_type_): describe the type of the entity
            gen_zone (list, optional): describes a rectangle in with the entity will appear, defined to [x_min, y_min, x_max, y_max]. Defaults to [0,0,100,100].
        """
        match type:
            case"wolf":
                enemy = wolf(40, 20, 1,1)
                enemy_sprite = arcade.Sprite(self.enemy_texture, 0.5)
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
             

    def get_knockback(self,sprite, knockback):
        dest_x = sprite.center_x + (sprite.center_x - self.player_sprite.center_x)
        dest_y = sprite.center_y + (sprite.center_y - self.player_sprite.center_y)

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
                        self.get_knockback(sprite, self.player.weapon.knockback)


    def kill_entity(self, entity, sprite):
        del self.entityl[self.entityl.index([entity, sprite])]
        del entity
        self.enemyl.remove(sprite)
        del sprite

    # --- Gestion du clavier ---
    def on_key_press(self, key, modifiers):
        if key == arcade.key.Z:
            self.keys_pressed["z"] = True
        elif key == arcade.key.S:
            self.keys_pressed["s"] = True
        elif key == arcade.key.Q:
            self.keys_pressed["q"] = True
        elif key == arcade.key.D:
            self.keys_pressed["d"] = True
        if key == arcade.key.SPACE:
            self.keys_pressed["atk"] = True

    def on_key_release(self, key, modifiers):
        if key == arcade.key.Z:
            self.keys_pressed["z"] = False
        elif key == arcade.key.S:
            self.keys_pressed["s"] = False
        elif key == arcade.key.Q:
            self.keys_pressed["q"] = False
        elif key == arcade.key.D:
            self.keys_pressed["d"] = False
        if key == arcade.key.SPACE:
            self.keys_pressed["atk"] = False


# --- Lancer le jeu ---
if __name__ == "__main__":
    game = MyGame()
    game.setup()
    arcade.run()
