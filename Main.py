import arcade
import os
import Settings
import Map
import Options


"""
Todo:
-Implement AI!!!
"""


class MyGame(arcade.Window):

    def __init__(self, screen_width, screen_height, title):
        super().__init__(screen_width, screen_height, title)

        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)

        self.background = None
        self.button_list = None

        self.button_list = []
        self.map_file = "map_1.csv"
        self.ai_mode = False

        # create our 3 options to select what map to load
        map1_button = Options.OptionButton((screen_width / 2) - 120, screen_height - 450, "Map 1")
        # map1 will be our default option
        map1_button.face_color = arcade.color.ALLOY_ORANGE

        map2_button = Options.OptionButton((screen_width / 2), screen_height - 450, "Map 2")
        map3_button = Options.OptionButton((screen_width / 2) + 120, screen_height - 450, "Map 3")

        # create our 2 option to select if user or AI will control player
        user_button = Options.OptionButton((screen_width / 2) - 60, screen_height - 550, "User")
        # user is the default option
        user_button.face_color = arcade.color.ALLOY_ORANGE
        ai_button = Options.OptionButton((screen_width / 2) + 60, screen_height - 550, "AI")

        self.button_list.append(map1_button)
        self.button_list.append(map2_button)
        self.button_list.append(map3_button)
        self.button_list.append(user_button)
        self.button_list.append(ai_button)
    
        # Set the background color
        arcade.set_background_color(arcade.color.AMAZON)
        self.background = arcade.load_texture("graphics/menuBackground.png")
        self.state = "menu"

        # Map stuff
        self.map = None
        self.view_left = 0
        self.view_bottom = 0

    def setup(self):
        self.map = Map.Map(self)

        # Set the background color
        arcade.set_background_color(arcade.color.AMAZON)
        # Set the view port boundaries
        # These numbers set where we have 'scrolled' to.
        self.view_left = 0
        self.view_bottom = 0
        
    def on_mouse_press(self, x, y, button, key_modifiers):
        button_selected = Options.check_mouse_press_for_buttons(x, y, self.button_list)

        if button_selected is not None:
            button_selected.face_color = arcade.color.ALLOY_ORANGE
            # print(buttonSelected.text)

            # Update button color to reflect our selection
            # Every time the button is clicked
            for x in self.button_list:

                if button_selected.text == "Map 1":
                    # Add the file path of map 1
                    self.map_file = "map_1.csv"

                    # Deselect Map2 and Map3 buttons, only keep Map 1 selected
                    if x.text == "Map 2" or x.text == "Map 3":
                        x.pressed = False
                        x.face_color = arcade.color.LIGHT_GRAY

                if button_selected.text == "Map 2":
                    # Add the file path of map 2
                    self.map_file = "map_2.csv"

                    # Deselect Map1 and Map3 buttons, only keep Map 2 selected
                    if x.text == "Map 1" or x.text == "Map 3":
                        x.pressed = False
                        x.face_color = arcade.color.LIGHT_GRAY

                if button_selected.text == "Map 3":
                    # Add the file path of map 3
                    self.map_file = "map_3.csv"

                    # Deselect Map1 and Map2 buttons, only keep Map 2 selected
                    if x.text == "Map 1" or x.text == "Map 2":
                        x.pressed = False
                        x.face_color = arcade.color.LIGHT_GRAY

                if button_selected.text == "AI":
                    # Set the player to be the AI
                    self.ai_mode = True

                    # Deselect user button
                    if x.text == "User":
                        x.pressed = False
                        x.face_color = arcade.color.LIGHT_GRAY

                if button_selected.text == "User":
                    # set the player to be the user
                    self.ai_mode = False

                    # Deselect the AI
                    if x.text == "AI":
                        x.pressed = False
                        x.face_color = arcade.color.LIGHT_GRAY

    def draw_main_menu(self):
        # Draw main menu screen.
        arcade.draw_texture_rectangle(Settings.SCREEN_WIDTH / 2, Settings.SCREEN_HEIGHT / 2, Settings.SCREEN_WIDTH, Settings.SCREEN_HEIGHT, self.background)

    def on_draw(self):
        # This command has to happen before we start drawing
        arcade.start_render()

        # Draw all the sprites.
        if self.state == "game":
            self.map.block_list.draw()
            self.map.player_list.draw()


            output = f"Row: {self.map.player.row}\nCol: {self.map.player.col}"
            arcade.draw_text(output, self.view_left + 10, self.view_bottom + 20, arcade.color.WHITE, 14)

            output = f"Score : {self.map.player.score}"
            arcade.draw_text(output, self.view_left + 10, self.view_bottom + 50, arcade.color.WHITE, 14)

            output = f"Press ESC to quit"
            arcade.draw_text(output, self.view_left + 10, self.view_bottom + 550, arcade.color.BLACK, 14)


        elif self.state == "menu":
            self.draw_main_menu()
            # Draw the buttons
            for button in self.button_list:
                button.draw()
        
        else:
            self.draw_game_over()

    def draw_game_over(self):
        arcade.set_background_color(arcade.color.BLACK)

        output = f"Final Score : {self.map.player.score}"
        arcade.draw_text(output, 250, 350, arcade.color.WHITE, 34)

        output = f"Press Esc to go to Main Menu"
        arcade.draw_text(output, 200, 250, arcade.color.WHITE, 24)

    def on_key_press(self, key, modifiers):
        # Handle inputs during the Menu state
        if self.state == "menu":
            if key == arcade.key.ENTER or key == arcade.key.RETURN:
                self.state = "game"
                self.setup()

        # Handle inputs during the Game state
        elif self.state == "game":

            if key == arcade.key.ESCAPE:
                self.end_game()

            if self.ai_mode is False:
                if key == arcade.key.LEFT:
                    self.map.player.move_left()
                elif key == arcade.key.RIGHT:
                    self.map.player.move_right()
                elif key == arcade.key.DOWN:
                    self.map.player.dig_down()

        # Handle inputs during the Game Over state
        elif self.state == "game over":
            if key == arcade.key.ESCAPE:
                self.state = "menu"

    def update(self, delta_time):
        # only update the game when the STATE is "game"
        if self.state == "game":

            if self.ai_mode is True:
                self.map.player.update_ai(delta_time)

            # --- Manage Scrolling ---
            # Track if we need to change the view port
            changed = False

            # Scroll left
            left_bndry = self.view_left + Settings.VIEWPORT_MARGIN
            if self.map.player.left < left_bndry:
                self.view_left -= left_bndry - self.map.player.left
                changed = True

            # Scroll right
            right_bndry = self.view_left + Settings.SCREEN_WIDTH - Settings.RIGHT_MARGIN
            if self.map.player.right > right_bndry:
                self.view_left += self.map.player.right - right_bndry
                changed = True

            # Scroll up
            top_bndry = self.view_bottom + Settings.SCREEN_HEIGHT - Settings.VIEWPORT_MARGIN
            if self.map.player.top > top_bndry:
                self.view_bottom += self.map.player.top - top_bndry
                changed = True

            # Scroll down
            bottom_bndry = self.view_bottom + Settings.VIEWPORT_MARGIN
            if self.map.player.bottom < bottom_bndry:
                self.view_bottom -= bottom_bndry - self.map.player.bottom
                changed = True

            # If we need to scroll, go ahead and do it.
            if changed:
                arcade.set_viewport(self.view_left, Settings.SCREEN_WIDTH + self.view_left, self.view_bottom, Settings.SCREEN_HEIGHT + self.view_bottom)

        # Set viewport to this anytime we're not in-game
        else:
            arcade.set_viewport(0, Settings.SCREEN_WIDTH, 0, Settings.SCREEN_HEIGHT)

    def end_game(self):
        for i in range(len(self.map.map_grid)):
            self.map.map_grid[i].clear()
        self.map.map_grid.clear()
        self.state = "game over"
            

def main():
    game = MyGame(Settings.SCREEN_WIDTH, Settings.SCREEN_HEIGHT, Settings.SCREEN_TITLE)
    arcade.run()


if __name__ == "__main__":
    main()
