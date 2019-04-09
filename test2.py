"""
Load a map stored in csv format, as exported by the program 'Tiled.'

Artwork from: http://kenney.nl
Tiled available from: http://www.mapeditor.org/

If Python and Arcade are installed, this example can be run from the command line with:
python -m arcade.examples.sprite_csv_map
"""

import arcade
import os
import random

SPRITE_SCALING = 0.5
SPRITE_SCALING_GOLD = 0.2

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
OFFSCREEN_SPACE = 500
EDGESCREEN = 0
BOTTOM_LIMIT = -OFFSCREEN_SPACE
TOP_LIMIT = SCREEN_HEIGHT + OFFSCREEN_SPACE
RIGHT_LIMIT = SCREEN_WIDTH + OFFSCREEN_SPACE
LEFT_LIMIT = EDGESCREEN
SPRITE_PIXEL_SIZE = 128
GRID_PIXEL_SIZE = (SPRITE_PIXEL_SIZE * SPRITE_SCALING)
NUMBER_OF_GOLD = 100

# How many pixels to keep as a minimum margin between the character
# and the edge of the screen.
VIEWPORT_MARGIN = 40
RIGHT_MARGIN = 40

# Physics
MOVEMENT_SPEED = 5
JUMP_SPEED = 14
GRAVITY = 0.5


# class PlayerSprite(arcade.Sprite):
    


def get_map(filename):
    """
    This function loads an array based on a map stored as a list of
    numbers separated by commas.
    """
    map_file = open(filename)
    map_array = []
    for line in map_file:
        line = line.strip()
        map_row = line.split(",")
        for index, item in enumerate(map_row):
            map_row[index] = int(item)
        map_array.append(map_row)
    return map_array


class MyGame(arcade.Window):
    """ Main application class. """

    def __init__(self):
        """
        Initializer
        """
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT)

        # Set the working directory (where we expect to find files) to the same
        # directory this .py file is in. You can leave this out of your own
        # code, but it is needed to easily run the examples using "python -m"
        # as mentioned at the top of this program.
        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)

        # Sprite lists
        self.wall_list = None
        self.player_list = None
        self.gold_list = None

        # Set up the player
        self.player_sprite = None
        self.score = 0

        self.physics_engine = None
        self.view_left = 0
        self.view_bottom = 0
        self.total_time = 0.0
        self.game_over = False

    def setup(self):
        """ Set up the game and initialize the variables. """

        # Sprite lists
        self.player_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList()
        self.gold_list = arcade.SpriteList()
        
        # Set up the player
        self.score = 0
        self.player_sprite = arcade.Sprite("graphics/adventurer/adventurer_stand.png", SPRITE_SCALING)

        # Set up the timer in secs
        self.total_time = 5.0

        # Starting position of the player
        self.player_sprite.center_x = 40
        self.player_sprite.center_y = 300
        self.player_list.append(self.player_sprite)

        # Get a 2D array made of numbers based on the map
        map_array = get_map("gold_map.csv")

        # Right edge of the map in pixels
        self.end_of_map = len(map_array[0]) * GRID_PIXEL_SIZE

        for row_index, row in enumerate(map_array):
            for column_index, item in enumerate(row):

                # For this map, the numbers represent:
                # -1 = empty
                # 32 = dirt
                if item == -1:
                    continue
                elif item == 32:
                    wall = arcade.Sprite("graphics/tiles/dirt.png", SPRITE_SCALING)

                wall.right = column_index * 64
                wall.top = (7 - row_index) * 64
                self.wall_list.append(wall)
        
         # Create the gold ore
        for i in range(NUMBER_OF_GOLD):

            gold = arcade.Sprite("graphics/ore_gold.png", SPRITE_SCALING_GOLD)

            gold.center_x = random.randrange(LEFT_LIMIT, RIGHT_LIMIT)
            gold.center_y = random.randrange(BOTTOM_LIMIT, TOP_LIMIT)

            gold.angle = random.randrange(360)
            gold.change_angle = random.randrange(-5,6)
            # Add the gold ore to the lists
            self.gold_list.append(gold)

        self.physics_engine = \
            arcade.PhysicsEnginePlatformer(self.player_sprite,
                                           self.wall_list,
                                           gravity_constant=GRAVITY)

        # Set the background color
        arcade.set_background_color(arcade.color.BLACK)

        # Set the view port boundaries
        # These numbers set where we have 'scrolled' to.
        self.view_left = 0
        self.view_bottom = 0

        self.game_over = False

    def on_draw(self):
        """
        Render the screen.
        """

        # This command has to happen before we start drawing
        arcade.start_render()

        #------Timer------#
        minutes = int(self.total_time) // 60
        seconds = int(self.total_time) % 60
        
        # Draw all the sprites.
        self.player_list.draw()
        self.gold_list.draw()
        self.wall_list.draw()

        # Put the score & time on the screen.
        # The score will follow the viewport
        output = f"Time: {minutes:02d}:{seconds:02d}"
        arcade.draw_text(output, self.view_left + 10, self.view_bottom + 50, arcade.color.WHITE, 14)

        output = f"Score: {self.score}"
        arcade.draw_text(output, self.view_left + 10, self.view_bottom + 20, arcade.color.WHITE, 14)

        if self.game_over:
            arcade.draw_text("Game Over", self.view_left + (SCREEN_WIDTH/2), self.view_bottom + (SCREEN_HEIGHT/2), arcade.color.WHITE, 40)

    def on_key_press(self, key, modifiers):
        """
        Called whenever the mouse moves.
        """
        if key == arcade.key.UP:
            if self.physics_engine.can_jump():
                self.player_sprite.change_y = JUMP_SPEED
        elif key == arcade.key.LEFT:
            self.player_sprite.change_x = -MOVEMENT_SPEED
        elif key == arcade.key.RIGHT:
            self.player_sprite.change_x = MOVEMENT_SPEED

    def on_key_release(self, key, modifiers):
        """
        Called when the user presses a mouse button.
        """
        if key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.player_sprite.change_x = 0

    def update(self, delta_time):
        """ Movement and game logic """

        if self.total_time <= 0:
            self.game_over = True

        # Call update on all sprites 
        # update player movement animation
        if not self.game_over:
            self.total_time -= delta_time
            self.physics_engine.update()

        # --- Manage Scrolling --- #

        # Track if we need to change the view port

        changed = False

        # Scroll left
        left_bndry = self.view_left + VIEWPORT_MARGIN
        if self.player_sprite.left < left_bndry:
            self.view_left -= left_bndry - self.player_sprite.left
            changed = True

        # Scroll right
        right_bndry = self.view_left + SCREEN_WIDTH - RIGHT_MARGIN
        if self.player_sprite.right > right_bndry:
            self.view_left += self.player_sprite.right - right_bndry
            changed = True

        # Scroll up
        top_bndry = self.view_bottom + SCREEN_HEIGHT - VIEWPORT_MARGIN
        if self.player_sprite.top > top_bndry:
            self.view_bottom += self.player_sprite.top - top_bndry
            changed = True

        # Scroll down
        bottom_bndry = self.view_bottom + VIEWPORT_MARGIN
        if self.player_sprite.bottom < bottom_bndry:
            self.view_bottom -= bottom_bndry - self.player_sprite.bottom
            changed = True

        # If we need to scroll, go ahead and do it.
        if changed:
            arcade.set_viewport(self.view_left,
                                SCREEN_WIDTH + self.view_left,
                                self.view_bottom,
                                SCREEN_HEIGHT + self.view_bottom)
        
        # collected contains how many gold ores the player obtained
        collected = arcade.check_for_collision_with_list(self.player_sprite, self.gold_list)

        for gold in collected:
            gold.kill()
            self.score +=1

def main():
    window = MyGame()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()