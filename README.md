# MiningRush AI Project


## Authors:
Erine Estrella
David Toledo
Walid Elmir
Michael Perez

## Built With
* [Python 3](https://www.python.org/downloads/) - Programming language
* [Arcade](http://arcade.academy/index.html) - External libarary 
* [Visual Studio Code](https://code.visualstudio.com/download) - IDE
* [Kenney Assets](https://kenney.nl/)
  * [Tiles](https://kenney.nl/assets/voxel-pack) 
  * [Character Sprite](https://kenney.nl/assets/platformer-characters-1)

## Important Files
- Main 
  - Main file that runs the game
  - Initializes all Arcade elements, including the window and game loop
  - Handles all user inputs
  - Draws all game elements to the screen
- Block
  - Block tile object used during gameplay
  - Contains information about the row/column it's at, as well as what kind of block it is
  - AI uses this info to determine where it wants to go
- ArtificialPlayer
  - AI player object that plays through the level on its own
  - Uses BFS to determine where its next goal is
  - Can perform three moves: move left, move right, and dig down
- Player
  - Player object that can receive inputs to play through a level manually
  - Can perform three moves: move left, move right, and dig down
- Map
  - Object that contains 2D array of Block objects that constitutes a level
  - Generated from CSV files, containing integer values depicting what type of block the coordinate is
- Background
  - Similarly to the Map file, the object that constains a 2D array of Block objects 
  - Sole purpose is to create a map that serves as the background of the current level
  - Generated from CSV files with integer values that represent what type of tile the coordinate is
- Options
- Settings 
  - Simple configuration file tha adjusts pixel size, window size, etc

## Getting Started

### Installing on Windows Machine

### 1. Install Python from the official [Python website](https://www.python.org/downloads/)
    
  You have the option to download two different versions: 
  Version 3.x.x or version 2.x.x. The Arcade library requires 
  Python beginning with 3.x.x.

  When installing Python, make sure to click the check box
  that says `Add Python 3.x to PATH` and choose the Customize 
  installation option. 

  The defaults on the next screen are fine. 

  On the next screen, click the check box that says `Install python 
  for all users`. 

### 2. Install The Arcade Library

  Click the Window button on the lower left of the screen (or hit
  the window button on your keyboard) and type `command prompt`
  to search for the command prompt application. 

  Right click on the command prompt app and **run it as Administrator**. 

  Next, in the command prompt, type `pip install arcade`.

### 3. Install a Development Environment

  - **PyCharm**
  - **Sublime** (anaconda is a great sublime plug-in for Python
    development)
  - **Visual Studio Code** (What we used)
      - To get Visual code to run python, install the following 
        extensions: 
          - Code Runner
          - Python 
          - Python Extension pack
          - Python for VSCode
    
### Deployment - Running the Game

Open the MiningRush project inside the IDE. 

Run the Main.py file. 

### If using Visual Studio Code

  * After installing the code runner extension, there should be a play 
  button located at the top right side of the screen. If that doesn't 
  work, do the following:

  * Within the Main.py file, right click. Select "Run Python File in 
  Terminal". (Group was occasionally having issues with the play 
  button). 

### Installing on Linux Machine

### 1. The Arcade library is 3.6+ only. 

  You'll need to install Python 3 and use it instead of the built-in Python 2.x. 
  Usually on Linux and Mac, you can type `python3` instead of `python` once 
  installed. Same with `pip3` instead of `pip` to install packages to Python 3.x.

  Install Python 3 and some image dependencies: 

    apt update && sudo apt install -y python3-dev python3-pip libjpeg-dev zlib1g-dev python-gst-1.0

  Check that you have at least Python 3.6 with: 

    python3 -V
  
  If not the correct version, use the following [link](https://tecadmin.net/install-python-3-6-ubuntu-linuxmint/).


## Further help 

If there are any issues with installation, check the official [Arcade website](http://arcade.academy) for further 
instructions. 

## References
* [Arcade Academy](http://arcade.academy/installation.html) - Instructions reference


    




