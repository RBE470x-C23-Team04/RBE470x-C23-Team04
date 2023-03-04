# This is necessary to find the main code
import sys, os
sys.path.insert(0, os.path.abspath('../../bomberman'))
sys.path.insert(1, '..')


# Import necessary stuff
import random
# from bomberman.game import *
# import bomberman.game as Game 
from game import Game
from monsters.stupid_monster import StupidMonster
from testcharacter import bank1
from testcharacter import visited_points

# TODO This is your code!
sys.path.insert(2, '../../team04')
from testcharacter import TestCharacter

# Create the game
# random.seed(123) # TODO Change this if you want different random choices
# g = Game.fromfile('map.txt')
# g.add_monster(StupidMonster("stupid", # name
#                             "S",      # avatar
#                             3, 9      # position
# ))

# # TODO Add your character
# g.add_character(TestCharacter("me", # name
#                               "C",  # avatar
#                               0, 0  # position
# ))

# # Run!
# g.go()


# self.we = .3    # weight for Exit
# self.wma = -.5  # weight for Monster A
# self.wmb = -.5  # weight for Monster B
# self.wb = -.3   # weight for Bomb
# self.wx = -.2   # weight for Explosion

# print("End Score " + str(g.world.scores['me']))
print("self.we = " + str(bank1.we))
print("self.wma = " + str(bank1.wma))
print("self.wmb = " + str(bank1.wmb))
print("self.wb = " + str(bank1.wb))
print("self.wx = " + str(bank1.wx))

# print("Visited points")
# for p in range(len(visited_points.movement)):
#     print(visited_points.movement[p])


for i in range(1,100):
    random.seed(123)
    
    g = Game.fromfile('map.txt')
    
    g.add_monster(StupidMonster("stupid", # name
                                "S",      # avatar
                                3, 9      # position
    ))

    g.add_character(TestCharacter("me", # name
                                "C",  # avatar
                                0, 0  # position
    ))

    # Run!
    print("NEW GAME: " + str(i))
    print("self.we = " + str(bank1.we))
    print("self.wma = " + str(bank1.wma))
    print("self.wmb = " + str(bank1.wmb))
    print("self.wb = " + str(bank1.wb))
    print("self.wx = " + str(bank1.wx))
    
    bwe = bank1.we
    bwma = bank1.wma
    bwmb = bank1.wmb
    bwb = bank1.wb
    bwx = bank1.wx
    
    g.go(1)
    
    print("End Score " + str(g.world.scores['me']))
    print("self.we = " + str(bank1.we))
    print("self.wma = " + str(bank1.wma))
    print("self.wmb = " + str(bank1.wmb))
    print("self.wb = " + str(bank1.wb))
    print("self.wx = " + str(bank1.wx))
    print("END GAME: " + str(i))
    
    if (bank1.we == bwe and bank1.wma == bwma and bank1.wmb == bwma
        and bank1.wb == bwb and bank1.wx == bwx):
        print("WE DONE")
        print("End Score " + str(g.world.scores['me']))
        break
            














# # Set inputs:
# seed_range_lower = 1
# seed_range_higher = 1000

# prevScore = 0
# currScore = 0
# maxScore = 0

# success_cnt = 0
# killed_itself = 0
# killed_by_stupid = 0
# seed_outcome = {}
# seed_count = seed_range_higher - seed_range_lower + 1

# # Disable
# def blockPrint():
#     sys.stdout = open(os.devnull, 'w')

# # Restore
# def enablePrint():
#     sys.stdout = sys.__stdout__
    
# # enablePrint()
# # blockPrint()

# for i in range(seed_range_lower,seed_range_higher+1):
#     random.seed(i)

#     print("Seed #: " + str(i))
    
#     g = Game.fromfile('map.txt')
#     g.add_monster(StupidMonster("stupid", # name
#                                 "S",      # avatar
#                                 3, 9      # position
#     ))

#     # TODO Add your character
#     g.add_character(TestCharacter("me", # name
#                                   "C",  # avatar
#                                   0, 0  # position
#     ))
    
#     # print("Seed " + str(i))
    
#     blockPrint()
#     g.go(1)
#     # enablePrint()
    
#     events = g.events
#     print("Amount of events " + str(len(events)))
    
#     for event in range(0,len(events)): # go through all events. Search for character, me, found the exit
#         # print("event " + str(g.events[0]))
#         if (str(g.events[event]) == "me found the exit"):
#             success_cnt = success_cnt + 1   # increase success counter
#             print("Success Count: " + str(success_cnt))
#         seed_outcome[event+i] = str(g.events[event]) # add event to seed_outcome
#             # print("Seed " + str(i) + str(g.events[0]))
#         print("Event Number: " + str(event+1) + " - " + str(events[event]))
#         # print("Event " + str(seed_outcome[event]))
#         if (str(g.events[event]) == "me killed itself"):
#             killed_itself = killed_itself + 1
#         if (str(g.events[event]) == "me was killed by stupid"):
#             killed_by_stupid = killed_by_stupid + 1
    
    
#     print("Seed Outcome(s): ", end='')
#     seed_events = []
#     for n in range(0,len(g.events)):
#         # print(str(g.events[n]), sep=', ', end='', flush=True)
#         # print(str(g.events[n]), sep=', ', end='')
#         seed_events.append(str(events[n]))
#     print(str(seed_events), sep=', ', end='', flush=True)
    
#     seed_outcome[i] = seed_events # append list of outcomes for a seed to the seed outcome's list

#     # print(str(g.events), sep=', ', end='', flush=True)
#     # print("Seed Outcome: " + str(seed_outcome[i]))
#     print("")
#     print("")
    
    
    
#     enablePrint()
    
#     # print("Mod check" + str(5%2))
    
#     # percent = int(((i*100)/seed_count))
#     percent = ((i*100)/seed_count)
#     # if ((percent % 10) == 0):
#     print("Progress: " + str(percent) + "%")
    
#     # blockPrint()
    
    
# for ii in range(seed_range_lower,seed_range_higher+1):
#     print("Seed " + str(ii) + " " + str(seed_outcome[ii]))

# enablePrint()
# print("")
# print("Out of " + str(seed_count) + " seeds. Me found the exit " + str(success_cnt) + " time(s).")
# print("Me killed by self "+ str(killed_itself) + " time(s).")
# print("Me killed by stupid " + str(killed_by_stupid) + " time(s).")

