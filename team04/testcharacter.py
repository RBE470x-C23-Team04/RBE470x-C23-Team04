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
        # return 1            
        return me_character_pose
        
        # pose = []
        
        # pose = wrld.me(self)
        # print(pose)
        # return pose
        
        


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
    def neighbors_of_16(wrld, x, y):
        """_summary_

        Args:
            wrld (_type_): _description_
            x (_type_): _description_
            y (_type_): _description_
        """
        
        allNeighbors = []
        
        mapWidth = wrld.width()
        mapHeight = wrld.height()
        
        retNeighbors = []
        
        for xi in range(-2,2):
            for yi in range(-2,2):
                allNeighbors.append(x+xi, y+yi)
        print("Neightbors of 16: " + str(allNeighbors))
        
        for neighbor in allNeighbors:
            if(neighbor[0] >= 0) and (neighbor[0] < mapwidth) and (neighbor[1] >= 0) and (neighbor[1] < mapheight):
                if not wrld.wall_at(neighbor[0],neighbor[1]):
                    #add the items to ret list
                    retNeighbors.append(neighbor)
                    
        print("retNeighbors: " + str(retNeighbors))
                
        
    
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
        
    def minimax(self, wrld, new_wrld, new_wrld2, pose_list):
        print("worlds")
        wrld.printit()
        new_wrld.printit()
        new_wrld2.printit()
        print("minimax!")
    
        mini = {}
        pos = self.findCharacterPos(wrld, "me")
        
        for i in TestCharacter.neighbors_of_8(wrld, pos[0], pos[1]):
            monsters = new_wrld.monsters_at(i[0],i[1])
            monsters2 = new_wrld2.monsters_at(i[0],i[1])

            explosion = new_wrld.explosion_at(i[0],i[1])
            explosion2 = new_wrld2.explosion_at(i[0],i[1])

            bomb = wrld.bomb_at(i[0],i[1])

            empty = new_wrld.empty_at(i[0],i[1])

            score = 0
            if(monsters != None or monsters2 != None):
                #self.place_bomb()
                score -= 100
            if i in pose_list:
                score += 10
            if (explosion != None): #or explosion2 != None): #or bomb != None or explosion2 != None or bomb2 != None):
                 score -= 50
            if(bomb == None):
                score += 90

            #elif(empty):
                #score += 30
            
            mini[i] = score
        print("mini: " + str(mini))

        max = 0
        go = (0,0)
        for i in mini:
            if mini[i] > max:
                max = mini[i]
                go = i
        print("Go to " + str(go))
        if(go == (0,0)):
            self.move(0,0)
        else:
            dx = go[0] - pos[0]
            dy = go[1] - pos[1]
            self.move(dx,dy)


    def do(self, wrld):
        #m = next(iter(wrld.monsters.values()))
        # if not foundGoal:
        #     goal = self.findGoal(wrld)
        
        # print("ME: " + str(wrld.me(self)))
        
        our_pos = self.findCharacterPos(wrld, "me")
        
        

        # i = input("HELLO?")
        
        # dx, dy = 0, 0 # starting pos
        dx, dy = our_pos[0], our_pos[1]
        start = (dx, dy)
        goal = self.findGoal(wrld)
        #print("Goal " + str(goal)) 
        
        

        
        cameFrom = self.a_star(wrld, start, goal)
        pose_list = self.find_path(cameFrom, start, goal)
        # pose_list = pose_list.reverse()
        pose_list = list(reversed(pose_list))
        
        #print(pose_list)
        monster = False
        sw = SensedWorld.next(wrld)
        new_wrld = sw[0]

        sw2 = SensedWorld.next(new_wrld)
        new_wrld2 = sw2[0]

        if(new_wrld.monsters_at(dx,dy) != None or new_wrld2.monsters_at(dx,dy) != None):
            self.minimax(wrld, new_wrld, new_wrld2, pose_list)
            monster = True

        for next in self.neighbors_of_16(wrld, dx, dy):
            monsters = new_wrld.monsters_at(next[0],next[1])
            monsters2 = new_wrld2.monsters_at(next[0],next[1])

            #explosion = new_wrld.explosion_at(next[0],next[1])
            #explosion2 = new_wrld2.explosion_at(next[0],next[1])

            #bomb = new_wrld.bomb_at(next[0],next[1])
            #bomb2 = new_wrld2.bomb_at(next[0],next[1])

            empty = wrld.empty_at(next[0],next[1])
            #empty2 = new_wrld2.empty_at(next[0],next[1])

            if(monsters != None or monsters2 != None or empty == False): #or empty2 == False):# or explosion != None or bomb != None): or explosion2 != None or bomb2 != None):
                self.minimax(wrld,new_wrld, new_wrld2, pose_list)
                monster = True

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
        if monster == False:
            pose = pose_list[1]
            move_x = pose[0] - dx
            move_y = pose[1] - dy
            
            print("New Pose: " + str(move_x) + ", " + str(move_y))
         
            self.move(move_x, move_y)
      
            
            
        
           
        
