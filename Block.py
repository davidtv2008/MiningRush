import arcade


class Block(arcade.Sprite):
    def __init__(self, sprite_file, size, scale, row, col, block_type):
        super().__init__(sprite_file)
        self.append_texture(arcade.load_texture("graphics/Tiles/air.png", 0, 0, 0, 0, False, False, scale))
        self.width = size
        self.height = size
        self.row = row
        self.col = col
        self.block_type = block_type

        # A* stuff
        if block_type == "air":
            self.cost = 3
        elif block_type == "gold_nugget":
            self.cost = 2
        elif block_type == "stone_gold":
            self.cost = 1

        self.depth = 0
        self.parent = None

    def __str__(self):
        return str(self.row) + ", " + str(self.col) + ": " + self.block_type

    # destroy_block turns this Block object into air
    def destroy_block(self):
        self.block_type = "air"
        self.set_texture(1)
