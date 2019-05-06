import arcade
import Settings
import Player
import ArtificialPlayer
import Block

class Background:
    def __init__(self, game):
        self.game = game

        self.background_file_name = game.background_file
        self.map_width = 0
        self.map_height = 0
        self.map_grid = []

        # Sprite lists
        self.block_list = arcade.SpriteList()

        self.generate_map()

    def __str__(self):
        return self.background_file_name

    # generate_map populates the map_grid of this class object instance
    def generate_map(self):
        map_array = self.get_map(self.background_file_name)

        # Generate map grid based on map_array
        for row in range(len(map_array)):
            new_row = []

            for col in range(len(map_array[row])):

                # Air
                if map_array[row][col] == -1:
                    new_block = Block.Block("graphics/Tiles/air.png", Settings.SCALED_PIXEL_SIZE, Settings.SPRITE_SCALING, row, col, "air")
                    new_row.append(new_block)

                # grass_tan
                elif map_array[row][col] == 84:
                    new_block = Block.Block("graphics/Tiles/grass_tan.png", Settings.SCALED_PIXEL_SIZE, Settings.SPRITE_SCALING, row, col, "grass_tan")
                    new_row.append(new_block)

                # greystone
                elif map_array[row][col] == 10:
                    new_block = Block.Block("graphics/Tiles/greystone.png", Settings.SCALED_PIXEL_SIZE, Settings.SPRITE_SCALING, row, col, "greystone")
                    new_row.append(new_block)

                # rock
                elif map_array[row][col] == 108:
                    new_block = Block.Block("graphics/Tiles/rock.png", Settings.SCALED_PIXEL_SIZE, Settings.SPRITE_SCALING, row, col, "rock")
                    new_row.append(new_block)

                # trunk_bottom
                elif map_array[row][col] == 120:
                    new_block = Block.Block("graphics/Tiles/trunk_bottom.png", Settings.SCALED_PIXEL_SIZE, Settings.SPRITE_SCALING, row, col, "trunk_bottom")
                    new_row.append(new_block)

                # trunk_mid
                elif map_array[row][col] == 112:
                    new_block = Block.Block("graphics/Tiles/trunk_mid.png", Settings.SCALED_PIXEL_SIZE, Settings.SPRITE_SCALING, row, col, "trunk_mid")
                    new_row.append(new_block)
                
                # leaves_transparent
                elif map_array[row][col] == 50:
                    new_block = Block.Block("graphics/Tiles/leaves_transparent.png", Settings.SCALED_PIXEL_SIZE, Settings.SPRITE_SCALING, row, col, "leaves_transparent")
                    new_row.append(new_block)
                
                # leaves
                elif map_array[row][col] == 27:
                    new_block = Block.Block("graphics/Tiles/leaves.png", Settings.SCALED_PIXEL_SIZE, Settings.SPRITE_SCALING, row, col, "leaves")
                    new_row.append(new_block)

                # grass4
                elif map_array[row][col] == 85:
                    new_block = Block.Block("graphics/Tiles/grass4.png", Settings.SCALED_PIXEL_SIZE, Settings.SPRITE_SCALING, row, col, "grass4")
                    new_row.append(new_block)                    

                # wheat_stage1
                elif map_array[row][col] == 86:
                    new_block = Block.Block("graphics/Tiles/wheat_stage1.png", Settings.SCALED_PIXEL_SIZE, Settings.SPRITE_SCALING, row, col, "wheat_stage1")
                    new_row.append(new_block) 
            self.map_grid.append(new_row)

        self.map_width = len(self.map_grid[0])
        self.map_height = len(self.map_grid)

        # Set sprite positions of all the blocks in map_grid
        for row in range(len(self.map_grid)):
            for col in range(len(self.map_grid[row])):
                self.map_grid[row][col].right = col * Settings.SCALED_PIXEL_SIZE
                self.map_grid[row][col].top = -row * Settings.SCALED_PIXEL_SIZE
                self.block_list.append(self.map_grid[row][col])

    # get_map is a helper function used by generate_map, which returns a 2D array of the read CSV file
    def get_map(self, filename):
        """
        This function loads an array based on a map stored as a list of
        numbers separated by commas.
        """
        background_file = open(filename)
        map_array = []
        for line in background_file:
            line = line.strip()
            map_row = line.split(",")
            for index, item in enumerate(map_row):
                map_row[index] = int(item)
            map_array.append(map_row)
        return map_array

    # get_block returns the Block object within map_grid using the supplied row and col (or None if it found nothing)
    def get_block(self, row, col):
        if row < 0 or row >= self.map_height or col < 0 or col >= self.map_width:
            return None
        return self.map_grid[row][col]


