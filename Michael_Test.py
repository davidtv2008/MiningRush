import arcade
import os
import Block


"""
Todo:
-Add gold which increases score
-Add results screen when the player hits escape during the game, which tells the player how much gold they got and
sends them back to the main menu
-Refurbish main menu so that the player can choose between three different map level files
-Implement AI!!!
"""


SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Mining Rush Test"

SPRITE_SCALING = 0.3
SPRITE_PIXEL_SIZE = 128
SCALED_PIXEL_SIZE = (SPRITE_PIXEL_SIZE * SPRITE_SCALING)

VIEWPORT_MARGIN = 256
RIGHT_MARGIN = 256

STATE = "menu"


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
    def __init__(self, screen_width, screen_height, title):
        super().__init__(screen_width, screen_height, title)

        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)

        self.background = None

        # Set the background color
        arcade.set_background_color(arcade.color.AMAZON)
        self.background = arcade.load_texture("graphics/menuBackground.png")

        self.state = "menu"

        # Sprite lists
        self.player_list = None
        self.block_list = None

        # Set up the player
        self.player = None
        self.player_row = 0
        self.player_col = 0

        # Map stuff
        self.map_grid = []
        self.map_width = 0
        self.map_height = 0
        self.view_left = 0
        self.view_bottom = 0

    def setup(self):

        # print("setup")
        # Sprite lists
        self.player_list = arcade.SpriteList()
        self.block_list = arcade.SpriteList()

        # main menu background
        # Get a 2D array made of numbers based on the map
        map_array = get_map("testmapcsv_Platforms.csv")

        # Generate map grid based on map_array
        for row in range(len(map_array)):
            new_row = []

            for col in range(len(map_array[row])):

                # Air
                if map_array[row][col] == -1:
                    new_block = Block.Block("graphics/Tiles/air.png", SCALED_PIXEL_SIZE, SPRITE_SCALING, row, col, "air")
                    new_row.append(new_block)

                # Player
                elif map_array[row][col] == 42:
                    self.player = arcade.Sprite("graphics/adventurer/adventurer_stand.png", SPRITE_SCALING)
                    self.player.right = (col * SCALED_PIXEL_SIZE) - 6
                    self.player.bottom = -(row + 1) * SCALED_PIXEL_SIZE
                    self.player_list.append(self.player)
                    self.player_row = row
                    self.player_col = col
                    new_block = Block.Block("graphics/Tiles/air.png", SCALED_PIXEL_SIZE, SPRITE_SCALING, row, col, "air")
                    new_row.append(new_block)

                # dirt
                elif map_array[row][col] == 32:
                    new_block = Block.Block("graphics/Tiles/dirt.png", SCALED_PIXEL_SIZE, SPRITE_SCALING, row, col, "dirt")
                    new_row.append(new_block)

                # gravel_dirt
                elif map_array[row][col] == 57:
                    new_block = Block.Block("graphics/Tiles/gravel_dirt.png", SCALED_PIXEL_SIZE, SPRITE_SCALING, row, col, "gravel_dirt")
                    new_row.append(new_block)

                # dirt_grass
                elif map_array[row][col] == 34:
                    new_block = Block.Block("graphics/Tiles/dirt_grass.png", SCALED_PIXEL_SIZE, SPRITE_SCALING, row, col, "dirt_grass")
                    new_row.append(new_block)

                # dirt_sand
                elif map_array[row][col] == 40:
                    new_block = Block.Block("graphics/Tiles/dirt_sand.png", SCALED_PIXEL_SIZE, SPRITE_SCALING, row, col, "dirt_sand")
                    new_row.append(new_block)

                # stone
                elif map_array[row][col] == 11:
                    new_block = Block.Block("graphics/Tiles/stone.png", SCALED_PIXEL_SIZE, SPRITE_SCALING, row, col, "stone")
                    new_row.append(new_block)

                elif map_array[row][col] == 92:
                    new_block = Block.Block("graphics/Tiles/gold_nugget.png", SCALED_PIXEL_SIZE, SPRITE_SCALING, row, col, "gold_nugget")
                    new_row.append(new_block)

                # stone_gold
                elif map_array[row][col] == 35:
                    new_block = Block.Block("graphics/Tiles/stone_gold.png", SCALED_PIXEL_SIZE, SPRITE_SCALING, row, col, "stone_gold")
                    new_row.append(new_block)

            self.map_grid.append(new_row)

        self.map_width = len(self.map_grid)
        self.map_height = len(self.map_grid[0])

        # Set sprite positions of all the blocks in map_grid
        for row in range(len(self.map_grid)):
            for col in range(len(self.map_grid[row])):
                self.map_grid[row][col].right = col * SCALED_PIXEL_SIZE
                self.map_grid[row][col].top = -row * SCALED_PIXEL_SIZE
                self.block_list.append(self.map_grid[row][col])

        # Set the background color
        arcade.set_background_color(arcade.color.AMAZON)

        # Set the view port boundaries
        # These numbers set where we have 'scrolled' to.
        self.view_left = 0
        self.view_bottom = 0

    def draw_main_menu(self):
        # Draw main menu screen.
        arcade.draw_texture_rectangle(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, SCREEN_WIDTH, SCREEN_HEIGHT, self.background)
        
    def on_draw(self):

        # This command has to happen before we start drawing
        arcade.start_render()

        # Draw all the sprites.
        if self.state == "game":
            # print("game start")
            self.block_list.draw()
            self.player_list.draw()

            output = f"Row: {self.player_row}\nCol: {self.player_col}"
            arcade.draw_text(output, self.view_left + 10, self.view_bottom + 20, arcade.color.WHITE, 14)
        elif self.state == "menu":
            # print("menu start")
            self.draw_main_menu()

    def on_key_press(self, key, modifiers):
        
        if self.state == "game" and key == arcade.key.ESCAPE:
            for i in range(len(self.map_grid)):
                self.map_grid[i].clear()
            self.map_grid.clear()
            self.state = "menu"
        
        elif self.state == "menu" and (key == arcade.key.ENTER or key == arcade.key.RETURN):
            self.setup()
            self.state = "game"
                    
        elif key == arcade.key.LEFT:
            self.player_move_left()

        elif key == arcade.key.RIGHT:
            self.player_move_right()

        # Dig down
        elif key == arcade.key.DOWN:
            self.player_dig_down()

    def update(self, delta_time):

        # only update the game when the STATE is "game"
        if self.state == "game":

            # Move the player based on the user's input
            self.player_list.update()

            # Make sure the player can ever only move one tile at a time
            self.player.change_x = 0
            self.player.change_y = 0

            # --- Manage Scrolling ---

            # Track if we need to change the view port

            changed = False

            # Scroll left
            left_bndry = self.view_left + VIEWPORT_MARGIN
            if self.player.left < left_bndry:
                self.view_left -= left_bndry - self.player.left
                changed = True

            # Scroll right
            right_bndry = self.view_left + SCREEN_WIDTH - RIGHT_MARGIN
            if self.player.right > right_bndry:
                self.view_left += self.player.right - right_bndry
                changed = True

            # Scroll up
            top_bndry = self.view_bottom + SCREEN_HEIGHT - VIEWPORT_MARGIN
            if self.player.top > top_bndry:
                self.view_bottom += self.player.top - top_bndry
                changed = True

            # Scroll down
            bottom_bndry = self.view_bottom + VIEWPORT_MARGIN
            if self.player.bottom < bottom_bndry:
                self.view_bottom -= bottom_bndry - self.player.bottom
                changed = True

            # If we need to scroll, go ahead and do it.
            if changed:
                arcade.set_viewport(self.view_left, SCREEN_WIDTH + self.view_left, self.view_bottom, SCREEN_HEIGHT + self.view_bottom)
        else:
            arcade.set_viewport(0, SCREEN_WIDTH, 0, SCREEN_HEIGHT)

    def get_block(self, row, col):
        if row < 0 or row >= self.map_height or col < 0 or col >= self.map_width:
            return None
        return self.map_grid[row][col]

    def destroy_map_block(self, row, col):
        block_to_destroy = self.get_block(row, col)
        if block_to_destroy is None:
            print("Target block to destroy is out of bounds!")
            return
        block_to_destroy.destroy_block()

    def player_move_left(self):
        # Check if we can move into the space to the left of us
        target_block = self.get_block(self.player_row, self.player_col - 1)

        if target_block.block_type is "air" or target_block.block_type is "gold_nugget":

            if target_block.block_type is "gold_nugget":
                target_block.destroy_block()

            self.player.change_x = -SCALED_PIXEL_SIZE
            self.player_col -= 1
            self.check_if_player_should_fall()

        else:
            # Check if we can climb up what's blocking us
            climb_block_check = self.get_block(self.player_row - 1, self.player_col - 1)

            if climb_block_check.block_type is "air" or climb_block_check.block_type is "gold_nugget":

                if climb_block_check.block_type is "gold_nugget":
                    climb_block_check.destroy_block()

                self.player.change_x = -SCALED_PIXEL_SIZE
                self.player.change_y = SCALED_PIXEL_SIZE
                self.player_row -= 1
                self.player_col -= 1

    def player_move_right(self):
        # Check if we can move into the space to the right of us
        target_block = self.get_block(self.player_row, self.player_col + 1)

        if target_block.block_type is "air" or target_block.block_type is "gold_nugget":

            if target_block.block_type is "gold_nugget":
                target_block.destroy_block()

            self.player.change_x = SCALED_PIXEL_SIZE
            self.player_col += 1
            self.check_if_player_should_fall()

        else:
            # Check if we can climb up what's blocking us
            climb_block_check = self.get_block(self.player_row - 1, self.player_col + 1)

            if climb_block_check.block_type is "air" or climb_block_check.block_type is "gold_nugget":

                if climb_block_check.block_type is "gold_nugget":
                    climb_block_check.destroy_block()

                self.player.change_x = SCALED_PIXEL_SIZE
                self.player.change_y = SCALED_PIXEL_SIZE
                self.player_row -= 1
                self.player_col += 1

    def player_dig_down(self):
        block_to_dig = self.get_block(self.player_row + 1, self.player_col)

        if block_to_dig.block_type is "stone":
            self.destroy_map_block(self.player_row + 1, self.player_col)
            self.player.change_y = -SCALED_PIXEL_SIZE
            self.player_row += 1
            self.check_if_player_should_fall()

    def check_if_player_should_fall(self):
        block_to_check = self.get_block(self.player_row + 1, self.player_col)
        if block_to_check.block_type is "air" or block_to_check.block_type is "gold_nugget":
            self.make_player_fall()

    def make_player_fall(self):
        next_block = self.get_block(self.player_row + 1, self.player_col)
        while next_block.block_type is "air" or next_block.block_type is "gold_nugget":

            if next_block.block_type is "gold_nugget":
                next_block.destroy_block()

            self.player.change_y -= SCALED_PIXEL_SIZE
            self.player_row += 1
            next_block = self.get_block(self.player_row + 1, self.player_col)


def main():
    game = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    arcade.run()


if __name__ == "__main__":
    main()
