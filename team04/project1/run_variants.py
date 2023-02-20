# This is necessary to find the main code
import sys, os, math
sys.path.insert(0, '../bomberman')
sys.path.insert(1, '../project1')
# Import necessary stuff
from entity import CharacterEntity
from colorama import Fore, Back
from priority_queue import PriorityQueue
from world import World
from sensed_world import SensedWorld

# from .variant1
# from . import variant1
# from . import variant2
# from . import variant3
## or
# import variant1
# import variant2
## or
from variant1 import Game, TestCharacter
from variant2 import random, Game, TestCharacter, StupidMonster, SelfPreservingMonster
from variant3 import random, Game, TestCharacter, StupidMonster, SelfPreservingMonster
from variant4 import random, Game, TestCharacter, StupidMonster, SelfPreservingMonster
from variant5 import random, Game, TestCharacter, StupidMonster, SelfPreservingMonster

def some_func():
    print("Testing variant 1")
    
if __name__ == '__main__':
    some_func()
    self.variant1.g(1)

