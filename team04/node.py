# This is necessary to find the main code
import sys
sys.path.insert(0, '../bomberman')
# Import necessary stuff
from entity import CharacterEntity
from colorama import Fore, Back
from priority_queue import PriorityQueue
from world import World
from sensed_world import SensedWorld
import math

class Node:
    
    def __init__(self, value):
        
        self.value = value
        self.moveNone = None
        self.moveN = None
        self.moveNE = None
        self.moveE = None
        self.moveSE = None
        self.moveS = None
        self.moveSW = None
        self.moveW = None
        self.moveNW = None
        self.placeBomb = None
    
    # Initialize Nodes to None  
    def newNode(v):
        
        temp = Node(v)
        return temp
    
    # Get expectimax
    def expectimax(self, node, is_max):
        
        # Condition for Terminal node
        if (node.moveNone == None and node.moveN == None
            and node.moveNE == None and node.moveE == None
            and node.moveSE == None and node.moveS == None
            and node.moveSW == None and node.moveW == None
            and node.moveNW == None and node.placeBomb == None):
            return node.value
        
        # Maximizer node. Choose the max from the sub-trees
        if (is_max):
            return max(self.expectimax(node.moveNone, False), self.expectimax(node.moveNone, False),
                       self.expectimax(node.moveNone, False), self.expectimax(node.moveNone, False),
                       self.expectimax(node.moveNone, False), self.expectimax(node.moveNone, False),
                       self.expectimax(node.moveNone, False), self.expectimax(node.moveNone, False))
        
        # Chance node. Returns the average of the sub-trees
        else:
            return ()