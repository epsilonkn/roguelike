import arcade

# --- Constantes du jeu ---
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Caméra centrée sur le joueur (ZQSD)"

PLAYER_SPEED = 5


class MyGame(arcade.Window):
    """Classe principale du jeu"""
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        # --- Caméras ---
        self.camera = arcade.Camera2D()       # Caméra du monde
        self.gui_camera = arcade.Camera2D()   # Caméra pour le HUD (interface)

        # --- Joueur ---
        self.player = None
        self.player_texture = ":resources:images/animated_characters/male_person/malePerson_idle.png"

        # --- Entrées clavier ---
        self.keys_pressed = {"z": False, "q": False, "s": False, "d": False}

    def setup(self):
        """Initialisation du jeu"""
        self.spritel = arcade.SpriteList()
        self.player = arcade.Sprite(self.player_texture, 0.5)
        self.spritel.append(self.player)
        self.player.center_x = 200
        self.player.center_y = 200

        # Fond de couleur
        arcade.set_background_color(arcade.color.DARK_SLATE_GRAY)

    # --- Dessin ---
    def on_draw(self):
        self.clear()

        # --- Caméra du monde ---
        self.camera.use()

        # Dessiner un "terrain" simple
        arcade.draw_lbwh_rectangle_filled(0, 0, 2000, 2000,(0,0,0))

        # Dessiner le joueur
        self.spritel.draw()

        # --- Caméra GUI ---
        self.gui_camera.use()
        arcade.draw_text("Déplace-toi avec ZQSD", 10, 10, arcade.color.WHITE, 16)

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

        self.player.center_x += dx
        self.player.center_y += dy

        # Centrer la caméra sur le joueur
        self.camera.position = (self.player.center_x, self.player.center_y)

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

    def on_key_release(self, key, modifiers):
        if key == arcade.key.Z:
            self.keys_pressed["z"] = False
        elif key == arcade.key.S:
            self.keys_pressed["s"] = False
        elif key == arcade.key.Q:
            self.keys_pressed["q"] = False
        elif key == arcade.key.D:
            self.keys_pressed["d"] = False


# --- Lancer le jeu ---
if __name__ == "__main__":
    game = MyGame()
    game.setup()
    arcade.run()
