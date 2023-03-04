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
from node import Node
from bank import bank1


class TestCharacter(CharacterEntity):

    
    def findGoal(self, wrld):
        """Run once to find world exit.

        Args:
            wrld (_type_): present game state

        Returns:
            goal (tuple): (x,y) cell of Exit
        """
        world_width = wrld.width()
        world_height = wrld.height()
        for x in range(0,world_width):
            for y in range(0,world_height):
                if wrld.exit_at(x,y):
                    goal = (x,y)
                    foundGoal = True
        return goal
    
    
    def findMonsterPos(self, wrld, name):
        """Find the cell of a given name monster.
        
        Args:
            wrld (_type_): present game state
        Returns:
            monster_pose (tuple): (x,y)
        """
        monster_pose = (-1,-1)
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


    def findCharacterPos(self, wrld, name):
        """Find the cell of a given name character.

        Args:
            wrld (_type_): present game state

        Returns:
            me_character_pose (tuple): (x,y)
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
                            character_pose = (x,y)
                            print("HERE " + str(character_pose))            
        return character_pose
        
        
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

        return out


    @staticmethod
    def neighbors_of_8(wrld, x, y):
        """Returns a list of valid open cells around a given tuple (x,y)
        of radius 1

        Args:
            wrld (_type_): present game state
            x (int): X coordinate of cell
            y (int): Y coordinate of cell
        """
        ##create the array of all 4 possible values (x,y)
        allNeighbors = [(x+1, y+1), (x, y+1), (x-1, y+1), (x+1, y), (x-1, y), (x+1, y-1), (x, y-1), (x-1, y-1), (x,y)]

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
        """Returns a list of valid open cells around a given tuple (x,y)
        of radius 2 (does not include neighbors of 8)

        Args:
            wrld (_type_): present game state
            x (int): X coordinate of cell
            y (int): Y coordinate of cell
        """
        
        allNeighbors = [(x-2, y-2), (x-2, y-1), (x-2, y), (x-2, y+1), (x-2, y+2), (x-1, y-2), (x-1, y+2), (x, y-2),
                        (x+1, y-2), (x+1, y+2), (x+2, y-2), (x+2, y-1), (x+2, y), (x+2, y+1), (x+2, y+2), (x, y+2)]
        
        mapWidth = wrld.width()
        mapHeight = wrld.height()
        
        retNeighbors = []
        
        for xi in range(-2,2):
            for yi in range(-2,2):
                allNeighbors.append((x+xi, y+yi))
        #print("Neightbors of 16: " + str(allNeighbors))
        
        for neighbor in allNeighbors:
            if(neighbor[0] >= 0) and (neighbor[0] < mapWidth) and (neighbor[1] >= 0) and (neighbor[1] < mapHeight):
                if not wrld.wall_at(neighbor[0],neighbor[1]):
                    #add the items to ret list
                    retNeighbors.append(neighbor)
                    
        #print("retNeighbors: " + str(retNeighbors))
        return retNeighbors


    @staticmethod
    def neighbors_of_bomb(wrld, x, y):
        """Returns a list of four open cells up/down/left/right around 
        a bomb of radius 1

        Args:
            wrld (_type_): present game state
            x (int): X coordinate of cell
            y (int): Y coordinate of cell

        Returns:
            retNeightbors (list): four open cells around a bomb
        """
        mapWidth = wrld.width()
        mapHeight = wrld.height()
        neighbors = [(x+1, y), (x-1, y), (x, y+1), (x, y-1)]
        retNeighbors = []
        for neighbor in neighbors:
            if(neighbor[0] >= 0) and (neighbor[0] < mapWidth) and (neighbor[1] >= 0) and (neighbor[1] < mapHeight):
                if not wrld.wall_at(neighbor[0],neighbor[1]):
                    #add the items to ret list
                    retNeighbors.append(neighbor)
        return retNeighbors
        
    
    def a_star(self, wrld, start, goal):
        """A* Path Planning

        Args:
            wrld (_type_): present game state
            start (tuple): (x,y)
            goal (tuple): (x,y)

        Returns:
            cameFrom (dict): Dictionary of points with keys of values
        """
        
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
        """Next step of A*.
        Takes the cameFrom dictionary and forms a path while appending
        start (x,y) at the beginning and goal (x,y) at the end

        Args:
            cameFrom (dict): dictionary from A*
            start (tuple): (x,y) Starting cell
            goal (tuple): (x,y) Exit cell

        Returns:
            findPath (dict): Path - (x,y) points to follow
        """
        cameFromKey = list(cameFrom.keys())
        if(goal not in cameFromKey):
            goal = cameFromKey[2]
            print("goal" + str(goal))
            

        findPath = []
        findPath.append(goal)
        while start != goal:
            cfrom = cameFrom.get(goal)
            findPath.append(cfrom)
            goal = cfrom
        return findPath


    def isMonsterNear(self, wrld, new_wrld, point):
        """Detects if a monster will enter a valid neightbor of 8 of point
        given on the next game state.

        Args:
            wrld (_type_): present game state
            new_wrld (_type_): next game state
            point (tuple): (x,y) (usually present character cell)

        Returns:
            state (boolean): True if monster becomes near
        """
        x = point[0]
        y = point[1]
        
        state = False
        
        for i in TestCharacter.neighbors_of_8(wrld, x, y):
            if (new_wrld.monsters_at(i[0],i[1]) != None):
                state = True
                print("Monster nearby " + str(i))
                
        return state


    def minimax(self, wrld, new_wrld, new_wrld2, pose_list):
        """Decides which direction the character should go based on the 
        highest value of a cell within neightbors of 8.

        Args:
            wrld (_type_): present game state
            new_wrld (_type_): next game state
            new_wrld2 (_type_): next+1 game state
            pose_list (list): List of path from findPath after A*
        """
        
        print("minimax!")

        mini = {}
        pos = self.findCharacterPos(wrld, "me")
        bomb_radius = []
        if(wrld.bomb_at(pos[0],pos[1])):
            bomb_radius = TestCharacter.neighbors_of_bomb(wrld, pos[0], pos[1])
            print("bomb radius " + str(bomb_radius))
  
        
        for i in TestCharacter.neighbors_of_8(wrld, pos[0], pos[1]):
            monsters = new_wrld.monsters_at(i[0],i[1])
            monsters2 = new_wrld2.monsters_at(i[0],i[1])

            explosion3 = wrld.explosion_at(i[0],i[1])
            explosion = new_wrld.explosion_at(i[0],i[1])
            explosion2 = new_wrld2.explosion_at(i[0],i[1])
            
            bom = wrld.bomb_at(i[0],i[1])
            bomb = new_wrld.bomb_at(i[0],i[1])
            bomb2 = new_wrld2.bomb_at(i[0],i[1])

            score = 0
            if(monsters or monsters2): #self.isMonsterNear(wrld, new_wrld, i)):
                self.place_bomb()
                score -= 30
            if i in pose_list:
                score += 10
            if (explosion or explosion2 or explosion3): 
                print("explosion " + str(i))
                score -= 50
            if(bomb or bomb2 or bom):
                score -= 200
            if(wrld.wall_at(i[0],i[1])):
                score -= 50
            if(wrld.bomb_at(pos[0],pos[1])):
                if(i in bomb_radius):
                    score -= 110
            # if(self.trap(wrld,i[0],i[1])):
            #     score-=20
            # if(not self.wallAround(wrld,i[0],i[1])):
            #     score += 20
            
            
            mini[i] = score
        #print("mini: " + str(mini))

        go = self.QLearn(wrld,new_wrld,new_wrld2,mini)

        # max = -1000
        # go = (0,0)
        # for i in mini:
        #     if mini[i] > max:
        #         max = mini[i]
        #         go = i
        # print("Go to " + str(go))
       
        dx = go[0] - pos[0]
        dy = go[1] - pos[1]
        self.move(dx,dy)


    def checkWall(self,wrld,dx,dy):
        """Checks if there is a wall at given x, y values.

        Args:
            wrld (_type_): present game state
            dx (int): X coordinate
            dy (int): Y coordinate

        Returns:
            (boolean): True if wall at given x, y values
        """
        mapWidth = wrld.width()
        if(dx-1 <= -1):
            if(wrld.wall_at(dx,dy+1) and wrld.wall_at(dx+1,dy+1)):
                return True
        elif(dx+2 > mapWidth):
            if(wrld.wall_at(dx,dy+1) and wrld.wall_at(dx-1,dy+1)):
                return True
        else:
            if(wrld.wall_at(dx,dy+1) and wrld.wall_at(dx+1,dy+1) and wrld.wall_at(dx-1,dy+1)):
                return True
        return False


    def findBomb(self,wrld,x,y):
        """Count amount of bombs in a neighbors of 8 and at current
        (x,y) cell.

        Args:
            wrld (_type_): present game state
            x (int): X coordinate
            y (int): Y coordinate

        Returns:
            fb (int): Total count of bombs
        """
        fb = 0
        if(wrld.bomb_at(x,y)):
            fb = 1
        for i in TestCharacter.neighbors_of_8(wrld,x,y):
            if(wrld.bomb_at(i[0],i[1])):
                fb = 1
        return fb


    def findExplosion(self,wrld, new_wrld, new_wrld2,x,y):
        """Count of explosions in world states of current, next, and 
        following.

        Args:
            wrld (_type_): present game state
            new_wrld (_type_): next game state
            new_wrld2 (_type_): following game state
            x (int): X coordinate
            y (int): Y coordinate

        Returns:
            fx (int): Total count of explosions
        """
        fx = 0
        explosion3 = wrld.explosion_at(x,y)
        explosion = new_wrld.explosion_at(x,y)
        explosion2 = new_wrld2.explosion_at(x,y)
        if(explosion3 or explosion2 or explosion):
            fx += 1
        for i in TestCharacter.neighbors_of_8(wrld,x,y):
            explosion3 = wrld.explosion_at(i[0],i[1])
            explosion = new_wrld.explosion_at(i[0],i[1])
            explosion2 = new_wrld2.explosion_at(i[0],i[1])
            if(explosion3 or explosion2 or explosion):
                fx += 1
        return fx


    def getMonsters(self,wrld):
        """Get a dictionary of all monsters with their name as key and 
        their (x,y) cell as item.

        Args:
            wrld (_type_): present game state

        Returns:
            currMonPos (dict): Dictionary of all monsters present
        """
        monsters = ["aggressive", "stupid","selfpreserving"]
        currMonPos = {}
        for i in monsters:
            if(self.findMonsterPos(wrld,i) != (-1,-1)):
                currMonPos[i] = self.findMonsterPos(wrld,i)
        return currMonPos


    def QLearn(self,wrld,new_wrld, new_wrld2,mini):
        """Approximate Q-Learning Algorithm

        Args:
            wrld (_type_): present game state
            new_wrld (_type_): next game state
            new_wrld2 (_type_): following game state
            mini (dict): Dictionary of scores

        Returns:
            go (x,y): Which (x,y) cell for the character to go to
        """
        alpha = .01
        gamma = .01
        monsters = self.getMonsters(wrld)
        our_pos = self.findCharacterPos(wrld, "me")
        goal = self.findGoal(wrld)

        monsterPoses = list(monsters.values())
        monsterNames = list(monsters.keys())
        print(monsters)
        if(len(monsterNames)>0):
            monsterA = self.findMonsterPos(wrld,monsterNames[0])
        if(len(monsterNames)>1):
            monsterB = self.findMonsterPos(wrld,monsterNames[1])

        we = bank1.we
        wma = bank1.wma
        wmb = bank1.wmb
        wb = bank1.wb
        wx = bank1.wx

        fei = 1/(1+self.euclidean_distance(our_pos[0], our_pos[1], goal[0], goal[1]))
        if(len(monsterNames)>0):
            fmai = 1/(1+self.euclidean_distance(our_pos[0], our_pos[1], monsterA[0], monsterA[1]))
        else:
            fmai = 0
        if(len(monsterNames)>1):
            fmbi = 1/(1+self.euclidean_distance(our_pos[0], our_pos[1], monsterB[0], monsterB[1]))
        else:
            fmbi = 0
        fbi = self.findBomb(wrld, our_pos[0], our_pos[1])
        fxi = self.findExplosion(wrld,new_wrld,new_wrld2, our_pos[0], our_pos[1])
        print("fxi: " + str(fxi))
        Qi = we*fei + wma*fmai + wmb*fmbi + wb*fbi + wx*fxi

        QPrime = {}
        for k,v in mini.items():
            fe = 1/(1+self.euclidean_distance(k[0], k[1], goal[0], goal[1]))
            if(len(monsterNames)>0):
                fma = 1/(1+self.euclidean_distance(k[0], k[1], monsterA[0], monsterA[1]))
            else:
                fma = 0
            if(len(monsterNames)>1):
                fmb = 1/(1+self.euclidean_distance(k[0], k[1], monsterB[0], monsterB[1]))
            else:
                fmb = 0
            fb = self.findBomb(wrld, k[0], k[1])
            fx = self.findExplosion(wrld,new_wrld,new_wrld2, k[0], k[1])

            Qval = we*fe + wma*fma + wmb*fmb + wb*fb + wx*fx
            QPrime[k] = Qval

        print("Qvals: " + str(QPrime))
        keys = list(QPrime.keys())
        max = QPrime[keys[0]]
        go = keys[0]
        for i in QPrime:
            if QPrime[i] > max:
                max = QPrime[i]
                go = i

        r = -10
        print("r: " + str(r) + ", max: " + str(max*gamma) + ", Qi: " + str(Qi))
        delta = (r + gamma*max) - Qi

        bank1.we = we + (alpha*delta*fei)
        bank1.wma = wma + (alpha*delta*fmai)
        bank1.wmb = wmb + (alpha*delta*fmbi)
        bank1.wb = wb + (alpha*delta*fbi)
        bank1.wx = wx + (alpha*delta*fxi)
     

        print("we: " + str(bank1.we) + ", wma: " + str(bank1.wma)+ ", wmb: " + str(bank1.wmb) + ", wb: " + str(bank1.wb) + ", wx: " + str(bank1.wx))
        print("go: " + str(go))
        return go

        
    def do(self, wrld):
        """Main character function

        Args:
            wrld (_type_): present game state
        """
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
        print(dx,dy) 
       
        

        
        cameFrom = self.a_star(wrld, start, goal)
        #print("comefrom" + str(cameFrom))
        pose_list = self.find_path(cameFrom, start, goal)
        # pose_list = pose_list.reverse()
        pose_list = list(reversed(pose_list))
        #print("path" + str(pose_list))
        
        #if(wrld.wall_at(pose_list[1][0], pose_list[1][1])):
            #self.place_bomb()



        #print(pose_list)
        monster = False
        sw = SensedWorld.next(wrld)
        new_wrld = sw[0]

        sw2 = SensedWorld.next(new_wrld)
        new_wrld2 = sw2[0]


        if(new_wrld.monsters_at(dx,dy) or new_wrld2.monsters_at(dx,dy)):
            self.minimax(wrld, new_wrld, new_wrld2, pose_list)
            monster = True

        

        for next in self.neighbors_of_16(wrld, dx, dy):
            monsters = new_wrld.monsters_at(next[0],next[1])
            monsters2 = new_wrld2.monsters_at(next[0],next[1])
          
            explosion = new_wrld.explosion_at(next[0],next[1])
            explosion2 = new_wrld2.explosion_at(next[0],next[1])

            bomb = new_wrld.bomb_at(next[0],next[1])

            if(monsters or monsters2 or bomb or explosion or explosion2): #or self.wallAround(wrld,next[0],next[1])):
                self.minimax(wrld,new_wrld, new_wrld2, pose_list)
                monster = True
                break

        if(self.checkWall(wrld,dx,dy) and monster == False):
            print("bomb")
            self.place_bomb()
            self.minimax(wrld,new_wrld, new_wrld2, pose_list)

        # Clear past A* path
        world_width = wrld.width()
        world_height = wrld.height()
        for x in range(0,world_width):
            for y in range(0,world_height):
                self.set_cell_color(x, y, Fore.BLACK + Back.BLACK)
        
        # Draw A* path
        for cell in pose_list:
            self.set_cell_color(cell[0], cell[1], Fore.RED + Back.GREEN)
        
        
        #print("Our Pose: " + str(dx) + ", " + str(dy))
        if monster == False:
            pose = pose_list[1]
            move_x = pose[0] - dx
            move_y = pose[1] - dy
            
            #print("New Pose: " + str(move_x) + ", " + str(move_y))
            #new_wrld.me(self).move(move_x,move_y)
            self.move(move_x, move_y)
                  
