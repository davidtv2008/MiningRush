import arcade
import Settings


class ArtificialPlayer(arcade.Sprite):
    def __init__(self, map_obj, row, col):
        super().__init__("graphics/adventurer/robot_stand.png", Settings.SPRITE_SCALING)
        self.map = map_obj
        self.row = row
        self.col = col

        self.right = (self.col * Settings.SCALED_PIXEL_SIZE) - 6
        self.bottom = -(self.row + 1) * Settings.SCALED_PIXEL_SIZE

        self.score = 0

        # AI stuff
        self.move_timer_length = 0.3
        self.move_timer = self.move_timer_length
        self.instruction_list = []
        self.map_array = self.map.get_map(self.map.map_file_name)

        self.generate_instruction_list()
        # self.visited = self.map_array

    def generate_instruction_list(self):
        start = None
        end = None

        if self.map.map_file_name == "map_3.csv":
            start = [4, 2]
            end = [20, 9]
        if self.map.map_file_name == "map_2.csv":
            start = [1, 1]
            end = [13, 5]
        if self.map.map_file_name == "map_1.csv":
            start = [1, 1]
            end = [7, 5]

        self.instruction_list = self.bfs(self.map_array, start, end)
        self.instruction_list.reverse()

    def update_ai(self, delta_time):
        self.move_timer -= delta_time
        if self.move_timer <= 0:
            self.move_timer += self.move_timer_length
            
            if self.map_array[self.row+1][self.col] == 35:
                self.dig_down()
                return
            
            if len(self.instruction_list) > 0:
                instruction1 = self.instruction_list[len(self.instruction_list) - 1]
                instruction2 = self.instruction_list[len(self.instruction_list) - 2]

                if instruction1[0] == instruction2[0] and instruction1[1] < instruction2[1]:
                    self.move_right()
                elif instruction1[0] == instruction2[0] and instruction1[1] > instruction2[1]:
                    self.move_left()
                
                elif instruction1[0] > instruction2[0] and instruction1[1] > instruction2[1]:
                    self.move_left()
                elif instruction1[0] > instruction2[0] and instruction1[1] < instruction2[1]:
                    self.move_right()
                
                elif instruction1[0] < instruction2[0] and instruction1[1] == instruction2[1]:
                    self.dig_down()

                self.instruction_list.pop()

            else:
                self.map.game.end_game()

    def bfs(self, maze, start, end):
        
        queue = [start]
        visited = []
        
        while len(queue) != 0:
            if queue[0] == start:
                path = [queue.pop(0)]  # Required due to a quirk with tuples in Python
            else:
                path = queue.pop(0)
            front = path[-1]
            if front[0] == end[0] and front[1] == end[1]:
                return path
            elif front not in visited:
                adjacent_spaces = self.get_adjacent_spaces(maze, front, visited)
                for adjacent_space in adjacent_spaces:
                    new_path = list(path)
                    new_path.append(adjacent_space)
                    queue.append(new_path)
                visited.append(front)
        return None

    def get_adjacent_spaces(self, maze, space, visited):
        # Returns all legal spaces surrounding the current space
        # :param space: tuple containing coordinates (row, col)
        # :return: all legal spaces
        spaces = list()
        # spaces.append((space[0]-1, space[1]+1))# Climb
        # spaces.append((space[0]+1, space[1]-1))# Climb
        spaces.append((space[0]+1, space[1]))  # Down
        spaces.append((space[0], space[1]-1))  # Left
        spaces.append((space[0], space[1]+1))  # Right

        final = list()
        for i in spaces:
            if maze[i[0]][i[1]] != 34 and maze[i[0]][i[1]] != 32 and maze[i[0]][i[1]] != 40 and maze[i[0]][i[1]] != 57 and i not in visited:
                final.append(i)
        return final

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
