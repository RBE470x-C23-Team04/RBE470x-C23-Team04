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

class TestCharacter2(CharacterEntity):

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
    
    
    def findCharacterPos(self, wrld, name):
        """_summary_

        Args:
            wrld (_type_): _description_

        Returns:
            _type_: _description_
        """
        
        world_width = wrld.width()
        world_height = wrld.height()
        for x in range(0,world_width):
            for y in range(0,world_height):
                list = wrld.characters_at(x,y)
                # print(str(list))
                if list is not None:
                    for item in list:
                        if item.name == name:
                            me_character_pose = (x,y)
                            print("HERE " + str(me_character_pose))           
        return me_character_pose


    def findMonsterPos(self, wrld, name):
        """_summary_

        Args:
            wrld (_type_): _description_

        Returns:
            _type_: _description_
        """
        
        world_width = wrld.width()
        world_height = wrld.height()
        for x in range(0,world_width):
            for y in range(0,world_height):
                list = wrld.monsters_at(x,y)
                # print(str(list))
                if list is not None:
                    for item in list:
                        if item.name == name:
                            monster_pose = (x,y)
                            print("HERE " + str(monster_pose))           
        return monster_pose
        

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
    
    
    @staticmethod
    def mSpace(wrld, x, y):
        
        pass
        
    
    def heuristic(self, wrld):
        # character_to_monster = self.findMonsterPos(wrld, "stupid")
        m = next(iter(wrld.monsters.values())) #monster
        c = next(iter(wrld.characters.values())) #charcter
        dist = TestCharacter2.euclidean_distance(m[0].x,m[0].y,c[0].x,c[0].y)
        print("Distance to monster: " + str(dist))

        if (dist < 6):
            dist = 1 / dist * 200
        else:
            dist = 0
        print("Heuristic: " + str(dist)) 
        
        
        return dist
    
    
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
            
            for next in TestCharacter2.neighbors_of_8(wrld, current[0], current[1]):
                new_cost = cost_so_far[current] + TestCharacter2.euclidean_distance(current[0],current[1],next[0],next[1]) #+ TestCharacter2.mSpace(next[0],next[1])
                if next not in cost_so_far or new_cost < cost_so_far[next]:
                    cost_so_far[next] = new_cost 
                    priority = new_cost + self.heuristic(wrld)
                    frontier.put(next, priority)
                    came_from[next] = current
                    
                # print("Next: " + str(next) + ", Cost: " + str(cost_so_far[next]))
            # wrld.printit()
            print("Frontier: " + str(frontier.elements))
            self.mapScore(wrld, frontier.elements)   
        # print("A star: " + str(came_from))
                    
        return came_from
    
    
    def find_path(self, cameFrom, start, goal):
        findPath = []
        findPath.append(goal)
        while start != goal:
            cfrom = cameFrom.get(goal)
            findPath.append(cfrom)
            goal = cfrom
        return findPath
        
    
    def minimax(self, wrld, character, monster):
        pass
    
    
    def mapScore(self, wrld, score):
        elements = score
        world_width = wrld.width()
        world_height = wrld.height()
        spots = {}
        
        for x in range(0, world_width):
            for y in range(0, world_height):
                for element in elements:
                    
        
        
        
        pass
        
    
    def do(self, wrld):
        
        
        
        m = next(iter(wrld.monsters.values()))
        print("Monster at (" + str(m[0].x) + ", " + str(m[0].y) + ")")
        c = next(iter(wrld.characters.values()))
        print("Character at (" + str(c[0].x) + ", " + str(c[0].y) + ")")

        
        character_pos = self.findCharacterPos(wrld, "me")
        monster_pos = self.findMonsterPos(wrld, "stupid")
        
        
        # dx, dy = 0, 0 # starting pos
        dx, dy = character_pos[0], character_pos[1]
        start = (dx, dy)
        goal = self.findGoal(wrld)
        print("Goal " + str(goal)) 
        
        cameFrom = self.a_star(wrld, start, goal)
        pose_list = self.find_path(cameFrom, start, goal)
        # pose_list = pose_list.reverse()
        pose_list = list(reversed(pose_list))
        
        print(pose_list)
        
        
        # Clear past A* path
        world_width = wrld.width()
        world_height = wrld.height()
        for x in range(0,world_width):
            for y in range(0,world_height):
                self.set_cell_color(x, y, Fore.BLACK + Back.BLACK)
        
        # Draw A* path
        for cell in pose_list:
            self.set_cell_color(cell[0], cell[1], Fore.RED + Back.GREEN)
        
        
        print("Our Pose: " + str(dx) + ", " + str(dy))
            
        pose = pose_list[1]
        move_x = pose[0] - dx
        move_y = pose[1] - dy
        
        print("New Pose: " + str(move_x) + ", " + str(move_y))
         
        self.move(move_x, move_y)
            