import arcade
import os
import Settings
import Map
import Options


"""
Todo:
-Refurbish main menu so that the player can choose between three different map level files
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
        self.mapFile = "map_1.csv"
        self.player = "User"

        #create our 3 options to select what map to load
        map1_button = Options.OptionButton((screen_width / 2) - 120, screen_height - 450, "Map 1")
        #map1 will be our defult option
        map1_button.face_color = arcade.color.ALLOY_ORANGE

        map2_button = Options.OptionButton((screen_width / 2),screen_height - 450, "Map 2")
        map3_button = Options.OptionButton((screen_width / 2) + 120,screen_height - 450, "Map 3")

        #create our 2 option to select if user or AI will control player
        user_button = Options.OptionButton((screen_width / 2) - 60, screen_height - 550, "User")
        #user is the default option
        user_button.face_color = arcade.color.ALLOY_ORANGE
        ai_button = Options.OptionButton((screen_width / 2) + 60,screen_height - 550, "AI")
        
        
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

        #self.map = Map.Map("map_1.csv")
        self.map = Map.Map(self.mapFile)


        # Set the background color
        arcade.set_background_color(arcade.color.AMAZON)

        # Set the view port boundaries
        # These numbers set where we have 'scrolled' to.
        self.view_left = 0
        self.view_bottom = 0

    def set_selection(self):
        #perform the selection of the button option
        print("clicked on play_button")
        
    def on_mouse_press(self, x, y, button, key_modifiers):
        buttonSelected = Options.check_mouse_press_for_buttons(x, y, self.button_list)

        if buttonSelected != None:
            buttonSelected.face_color = arcade.color.ALLOY_ORANGE
            #print(buttonSelected.text)

            #update button color to reflect our selection
            #everytime the button is clicked
            for x in self.button_list:
                if buttonSelected.text == "Map 1":
                    #add the file path of map 1
                    self.mapFile = "map_1.csv"
                
                    #unselect Map2 and Map3 buttons, only keep Map 1 selected
                    if x.text == "Map 2" or x.text == "Map 3":
                        x.pressed = False
                        x.face_color = arcade.color.LIGHT_GRAY
                if buttonSelected.text == "Map 2":
                    #add the file path of map 2
                    self.mapFile = "map_2.csv"

                    #unselect Map1 and Map3 buttons, only keep Map 2 selected
                    if x.text == "Map 1" or x.text == "Map 3":
                        x.pressed = False
                        x.face_color = arcade.color.LIGHT_GRAY
                if buttonSelected.text == "Map 3":
                    #add the file path of map 3
                    self.mapFile = "map_1.csv"
                
                    #unselect Map1 and Map2 buttons, only keep Map 2 selected
                    if x.text == "Map 1" or x.text == "Map 2":
                        x.pressed = False
                        x.face_color = arcade.color.LIGHT_GRAY
                if buttonSelected.text == "AI":
                    #set the player to be the AI
                    self.player = "AI"
                
                    #unselect user button
                    if x.text == "User":
                        x.pressed = False
                        x.face_color = arcade.color.LIGHT_GRAY
                if buttonSelected.text == "User":
                    #set the player to be the user
                    self.player = "User"

                    #unselect the AI
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
        """
        Draw "Game Over" Screen
        """
        arcade.set_background_color(arcade.color.BLACK)

        output = f"Final Score : {self.map.player.score}"
        arcade.draw_text(output, 250, 350, arcade.color.WHITE, 34)

        output = f"Press Esc to go to Main Menu"
        arcade.draw_text(output, 200, 250, arcade.color.WHITE, 24)

    def on_key_press(self, key, modifiers):

        # Start game if ENTER is pressed on the main menu
        if self.state == "menu" and (key == arcade.key.ENTER or key == arcade.key.RETURN):
            self.setup()
            self.state = "game"

        # Show results screen if ESC is hit during the game
        elif self.state == "game" and key == arcade.key.ESCAPE:
            for i in range(len(self.map.map_grid)):
                self.map.map_grid[i].clear()
            self.map.map_grid.clear()
            self.state = "game over"

        # Return to main menu if ESC is hit during the results screen
        elif self.state == "game over" and key == arcade.key.ESCAPE:
            self.state = "menu"

        # Handle player inputs during the game
        if self.state == "game":

            if key == arcade.key.LEFT:
                self.map.player.move_left()

            elif key == arcade.key.RIGHT:
                self.map.player.move_right()

            elif key == arcade.key.DOWN:
                self.map.player.dig_down()

    def update(self, delta_time):

        # only update the game when the STATE is "game"
        if self.state == "game":

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
        else:
            arcade.set_viewport(0, Settings.SCREEN_WIDTH, 0, Settings.SCREEN_HEIGHT)
            



def main():
    game = MyGame(Settings.SCREEN_WIDTH, Settings.SCREEN_HEIGHT, Settings.SCREEN_TITLE)
    arcade.run()


if __name__ == "__main__":
    main()