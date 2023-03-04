# This is necessary to find the main code
import sys
sys.path.insert(0, '../../bomberman')
sys.path.insert(1, '..')

# Import necessary stuff
from game import Game
# from bank import Bank

# bank1 = Bank(0)

# TODO This is your code!
sys.path.insert(1, '../team04')
from testcharacter import TestCharacter


# Create the game
g = Game.fromfile('team04/project2/map.txt')

# TODO Add your character
g.add_character(TestCharacter("me", # name
                              "C",  # avatar
                              0, 0  # position
))

# Run!
g.go(0)
