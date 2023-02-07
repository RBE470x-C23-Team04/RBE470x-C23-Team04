# This is necessary to find the main code
import sys, os
sys.path.insert(0, '../../bomberman')
sys.path.insert(1, '..')

# Import necessary stuff
import random
from game import Game
from monsters.stupid_monster import StupidMonster

# TODO This is your code!
sys.path.insert(1, '../team04')
from testcharacter import TestCharacter

# Create the game
# random.seed(832) # TODO Change this if you want different random choices
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

# Run!
# g.go()



### Uncomment below to run the variant with various seeds.

# Set inputs:
seed_range_lower = 1
seed_range_higher = 1000


success_cnt = 0
seed_outcome = {}
seed_count = seed_range_higher - seed_range_lower + 1

# Disable
def blockPrint():
    sys.stdout = open(os.devnull, 'w')

# Restore
def enablePrint():
    sys.stdout = sys.__stdout__
    
# enablePrint()
blockPrint()

for i in range(seed_range_lower,seed_range_higher+1):
    random.seed(i)

    print("Seed #: " + str(i))
    
    g = Game.fromfile('map.txt')
    g.add_monster(StupidMonster("stupid", # name
                                "S",      # avatar
                                3, 9      # position
    ))

    # TODO Add your character
    g.add_character(TestCharacter("me", # name
                                  "C",  # avatar
                                  0, 0  # position
    ))
    
    # print("Seed " + str(i))
    
    # blockPrint()
    g.go(1)
    # enablePrint()
    
    events = g.events
    print("Amount of events " + str(len(events)))
    
    for event in range(0,len(events)): # go through all events. Search for character, me, found the exit
        # print("event " + str(g.events[0]))
        if (str(g.events[event]) == "me found the exit"):
            success_cnt = success_cnt + 1   # increase success counter
            print("Success Count: " + str(success_cnt))
        seed_outcome[event+i] = str(g.events[event]) # add event to seed_outcome
            # print("Seed " + str(i) + str(g.events[0]))
        print("Event Number: " + str(event+1) + " - " + str(events[event]))
        # print("Event " + str(seed_outcome[event]))
    
    
    print("Seed Outcome(s): ", end='')
    seed_events = []
    for n in range(0,len(g.events)):
        # print(str(g.events[n]), sep=', ', end='', flush=True)
        # print(str(g.events[n]), sep=', ', end='')
        seed_events.append(str(events[n]))
    print(str(seed_events), sep=', ', end='', flush=True)
    
    seed_outcome[i] = seed_events # append list of outcomes for a seed to the seed outcome's list

    # print(str(g.events), sep=', ', end='', flush=True)
    # print("Seed Outcome: " + str(seed_outcome[i]))
    print("")
    print("")
    
    
    
    enablePrint()
    
    # print("Mod check" + str(5%2))
    
    # percent = int(((i*100)/seed_count))
    percent = ((i*100)/seed_count)
    # if ((percent % 10) == 0):
    print("Progress: " + str(percent) + "%")
    
    blockPrint()
    
    
for ii in range(seed_range_lower,seed_range_higher+1):
    print("Seed " + str(ii) + " " + str(seed_outcome[ii]))

enablePrint()
print("")
print("Out of " + str(seed_count) + " seeds. Me found the exit " + str(success_cnt) + " time(s).")
