# This is necessary to find the main code
import sys
sys.path.insert(0, '../bomberman')
# Import necessary stuff
from entity import CharacterEntity
from colorama import Fore, Back
from priority_queue import PriorityQueue
# from world import World
# from sensed_world import SensedWorld
import math

class TestCharacter(CharacterEntity):

    # def __init__(self,name,avatar,x_pos,y_pos):
    #     '''
    #     '''
    #     print("A")
        
    #     # wrld = SenseWorld.from_world(w)       
        
    #     # self.goal = self.findGoal(wrld)
    
    
    def findGoal(self, wrld):
        '''
        Run once to find world exit.
        '''
        world_width = wrld.width()
        world_height = wrld.height()
        for x in range(0,world_width):
            for y in range(0,world_height):
                if wrld.exit_at(x,y):
                    goal = (x,y)
                    foundGoal = True
        return goal


    @staticmethod
    def euclidean_distance(x1, y1, x2, y2):
        """
        Calculates the Euclidean distance between two points.
        :param x1 [int or float] X coordinate of first point.
        :param y1 [int or float] Y coordinate of first point.
        :param x2 [int or float] X coordinate of second point.
        :param y2 [int or float] Y coordinate of second point.
        :return   [float]        The distance.
        """

        out = math.sqrt((x2-x1)**2 + (y2-y1)**2)
        #print(f'{x1-x2}')
        return out
    
    @staticmethod
    def neighbors_of_8(wrld, x, y):
        """_summary_

        Args:
            wrld (_type_): _description_
            x (_type_): _description_
            y (_type_): _description_
        """
        ##create the array of all 4 possible values (x,y)
        allNeighbors = [(x+1, y+1), (x, y+1), (x-1, y+1), (x+1, y), (x-1, y), (x+1, y-1), (x, y-1), (x-1, y-1)]

        ##check through that list to ensure they are all in the map.
        #get the size of the ocupancy grid
        mapwidth = wrld.width()
        mapheight = wrld.height()
        #recurse through the list of neighbors to determine if they are in the space
        retNeighbors = []
        for neighbor in allNeighbors:
            #check if the tuple is inbounds
            #check x
            if(neighbor[0] >= 0) and (neighbor[0] < mapwidth) and (neighbor[1] >= 0) and (neighbor[1] < mapheight):
                if not wrld.wall_at(neighbor[0],neighbor[1]):
                    #add the items to ret list
                    retNeighbors.append(neighbor)

        return retNeighbors
        
    
    def a_star(self, wrld, start, goal):
        '''
        '''
        
        frontier = PriorityQueue()
        frontier.put(start, 0)
        came_from = {}
        cost_so_far = {}
        came_from[start] = None
        cost_so_far[start] = 0
        
        while not frontier.empty():
            current = frontier.get()
            
            if current == goal:
                break
            
            for next in TestCharacter.neighbors_of_8(wrld, current[0], current[1]):
                new_cost = cost_so_far[current] + TestCharacter.euclidean_distance(current[0],current[1],next[0],next[1])
                if next not in cost_so_far or new_cost < cost_so_far[next]:
                    cost_so_far[next] = new_cost
                    priority = new_cost
                    frontier.put(next, priority)
                    came_from[next] = current
                    
        return came_from
    
    
    def find_path(self, cameFrom, start, goal):
        findPath = []
        findPath.append(goal)
        while start != goal:
            cfrom = cameFrom.get(goal)
            findPath.append(cfrom)
            goal = cfrom
        return findPath
        
    
    def do(self, wrld):
        
        # if not foundGoal:
        #     goal = self.findGoal(wrld)
        
        
        dx, dy = 0, 0 # starting pos
        start = (dx, dy)
        goal = self.findGoal(wrld)
        print("Goal " + str(goal)) 
        
        cameFrom = self.a_star(wrld, start, goal)
        pose_list = self.find_path(cameFrom, start, goal)
        # pose_list = pose_list.reverse()
        pose_list = list(reversed(pose_list))
        
        print(pose_list)
        
        for cell in pose_list:
            self.set_cell_color(cell[0], cell[1], Fore.RED + Back.RED)
        
        # for x in range(wrld.width()):
        #     self.set_cell_color(x, 0, Fore.RED + Back.RED)
        
        # for c in input("How would you like to move (w=up,a=left,s=down,d=right,b=bomb)? "):
        #     if 'w' == c:
        #         dy -= 1
        #     if 'a' == c:
        #         dx -= 1
        #     if 's' == c:
        #         dy += 1
        #     if 'd' == c:
        #         dx += 1
        #     if 'b' == c:
        #         bomb = True
        for pose in pose_list:
            print("Pose: " + str(dx) + ", " + str(dy))
            # i = input("Hold")
            
            move_x = pose[0] - dx
            move_y = pose[1] - dy
            
            self.move(move_x, move_y)
            wrld.printit()
            
            
        
           
        pass
