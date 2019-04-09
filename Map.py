import arcade
import Settings
import Player
import Block


class Map:
    def __init__(self, map_file_name):
        self.map_file_name = map_file_name
        self.map_width = 0
        self.map_height = 0
        self.map_grid = []

        self.player = None

        # Sprite lists
        self.player_list = arcade.SpriteList()
        self.block_list = arcade.SpriteList()

        self.generate_map()

    def __str__(self):
        return self.map_file_name

    # generate_map populates the map_grid of this class object instance
    def generate_map(self):
        map_array = self.get_map(self.map_file_name)

        # Generate map grid based on map_array
        for row in range(len(map_array)):
            new_row = []

            for col in range(len(map_array[row])):

                # Air
                if map_array[row][col] == -1:
                    new_block = Block.Block("graphics/Tiles/air.png", Settings.SCALED_PIXEL_SIZE, Settings.SPRITE_SCALING, row, col, "air")
                    new_row.append(new_block)

                # Player
                elif map_array[row][col] == 42:
                    self.player = Player.Player(self, row, col)
                    self.player_list.append(self.player)
                    new_block = Block.Block("graphics/Tiles/air.png", Settings.SCALED_PIXEL_SIZE, Settings.SPRITE_SCALING, row, col, "air")
                    new_row.append(new_block)

                # dirt
                elif map_array[row][col] == 32:
                    new_block = Block.Block("graphics/Tiles/dirt.png", Settings.SCALED_PIXEL_SIZE, Settings.SPRITE_SCALING, row, col, "dirt")
                    new_row.append(new_block)

                # gravel_dirt
                elif map_array[row][col] == 57:
                    new_block = Block.Block("graphics/Tiles/gravel_dirt.png", Settings.SCALED_PIXEL_SIZE, Settings.SPRITE_SCALING, row, col, "gravel_dirt")
                    new_row.append(new_block)

                # dirt_grass
                elif map_array[row][col] == 34:
                    new_block = Block.Block("graphics/Tiles/dirt_grass.png", Settings.SCALED_PIXEL_SIZE, Settings.SPRITE_SCALING, row, col, "dirt_grass")
                    new_row.append(new_block)

                # dirt_sand
                elif map_array[row][col] == 40:
                    new_block = Block.Block("graphics/Tiles/dirt_sand.png", Settings.SCALED_PIXEL_SIZE, Settings.SPRITE_SCALING, row, col, "dirt_sand")
                    new_row.append(new_block)

                # stone
                elif map_array[row][col] == 11:
                    new_block = Block.Block("graphics/Tiles/stone.png", Settings.SCALED_PIXEL_SIZE, Settings.SPRITE_SCALING, row, col, "stone")
                    new_row.append(new_block)

                elif map_array[row][col] == 92:
                    new_block = Block.Block("graphics/Tiles/gold_nugget.png", Settings.SCALED_PIXEL_SIZE, Settings.SPRITE_SCALING, row, col, "gold_nugget")
                    new_row.append(new_block)

                # stone_gold
                elif map_array[row][col] == 35:
                    new_block = Block.Block("graphics/Tiles/stone_gold.png", Settings.SCALED_PIXEL_SIZE, Settings.SPRITE_SCALING, row, col, "stone_gold")
                    new_row.append(new_block)

            self.map_grid.append(new_row)

        self.map_width = len(self.map_grid)
        self.map_height = len(self.map_grid[0])

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
        map_file = open(filename)
        map_array = []
        for line in map_file:
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

    # destroy_map_block turns the Block object within map_grid using the supplied row and col into air
    def destroy_map_block(self, row, col):
        block_to_destroy = self.get_block(row, col)
        if block_to_destroy is None:
            print("Target block to destroy is out of bounds!")
            return
        block_to_destroy.destroy_block()
