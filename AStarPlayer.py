import arcade
import Settings


class AStarPlayer(arcade.Sprite):
    def __init__(self, map_obj, row, col):
        super().__init__("graphics/adventurer/advanced_robot_stand.png", Settings.SPRITE_SCALING)
        self.map = map_obj
        self.row = row
        self.col = col

        self.right = (self.col * Settings.SCALED_PIXEL_SIZE) - 6
        self.bottom = -(self.row + 1) * Settings.SCALED_PIXEL_SIZE

        self.score = 0

        # AI stuff
        self.move_timer_length = 0.5
        self.move_timer = self.move_timer_length
        self.instruction_list = []

        # A* stuff
        self.open = []
        self.closed = []

    def initiate_a_star(self):
        self.generate_instruction_list()

    def generate_instruction_list(self):
        start = [self.row, self.col]
        print(self.map.map_grid[self.row][self.col])

        self.open.append(start)
        count = 0

        '''while len(self.open) > 0 and count < 10:
            next_step = self.select_most_likely_next_step()
            self.closed.append(self.open.pop(0))

            count += 1'''

    def select_most_likely_next_step(self):
        print("Finding most likely next step")
        return [2, 2]

    def update_ai(self, delta_time):
        self.move_timer -= delta_time
        if self.move_timer <= 0:
            self.move_timer += self.move_timer_length

            if len(self.instruction_list) > 0:
                # do instruction
                self.instruction_list.pop()

            else:
                self.map.game.end_game()

    def move_left(self):
        # Check if we can move into the space to the left of us
        target_block = self.map.get_block(self.row, self.col - 1)

        if target_block is not None:

            if target_block.block_type is "air" or target_block.block_type is "gold_nugget":

                if target_block.block_type is "gold_nugget":
                    target_block.destroy_block()
                    self.score += 1

                self.col -= 1
                self.update_player_position()
                self.check_if_player_should_fall()

            else:
                # Check if we can climb up what's blocking us
                climb_block_check = self.map.get_block(self.row - 1, self.col - 1)

                if climb_block_check is not None and (climb_block_check.block_type is "air" or climb_block_check.block_type is "gold_nugget"):

                    if climb_block_check.block_type is "gold_nugget":
                        climb_block_check.destroy_block()
                        self.score += 1

                    self.row -= 1
                    self.col -= 1
                    self.update_player_position()

    def move_right(self):
        # Check if we can move into the space to the right of us
        target_block = self.map.get_block(self.row, self.col + 1)

        # Only None if we're out of bounds
        if target_block is not None:

            if target_block.block_type is "air" or target_block.block_type is "gold_nugget":

                if target_block.block_type is "gold_nugget":
                    target_block.destroy_block()
                    self.score += 1

                self.col += 1
                self.update_player_position()
                self.check_if_player_should_fall()

            else:
                # Check if we can climb up what's blocking us
                climb_block_check = self.map.get_block(self.row - 1, self.col + 1)

                if climb_block_check is not None and (climb_block_check.block_type is "air" or climb_block_check.block_type is "gold_nugget"):

                    if climb_block_check.block_type is "gold_nugget":
                        climb_block_check.destroy_block()
                        self.score += 1

                    self.row -= 1
                    self.col += 1
                    self.update_player_position()

    def dig_down(self):
        block_to_dig = self.map.get_block(self.row + 1, self.col)

        if block_to_dig is not None:

            if block_to_dig.block_type is "stone":
                self.map.destroy_map_block(self.row + 1, self.col)
                self.row += 1
                self.update_player_position()
                self.check_if_player_should_fall()

            elif block_to_dig.block_type is "stone_gold":
                self.map.destroy_map_block(self.row + 1, self.col)
                self.score += 5
                self.row += 1
                self.update_player_position()
                self.check_if_player_should_fall()

    def check_if_player_should_fall(self):
        block_to_check = self.map.get_block(self.row + 1, self.col)

        if block_to_check is not None:
            if block_to_check.block_type is "air" or block_to_check.block_type is "gold_nugget":
                self.make_player_fall()

    def make_player_fall(self):
        next_block = self.map.get_block(self.row + 1, self.col)

        while next_block is not None and (next_block.block_type is "air" or next_block.block_type is "gold_nugget"):

            if next_block.block_type is "gold_nugget":
                next_block.destroy_block()
                self.score += 1

            self.row += 1
            self.update_player_position()
            next_block = self.map.get_block(self.row + 1, self.col)

    # This function updates the robot's sprite to their new position
    def update_player_position(self):
        self.right = (self.col * Settings.SCALED_PIXEL_SIZE) - 6
        self.bottom = -(self.row + 1) * Settings.SCALED_PIXEL_SIZE
