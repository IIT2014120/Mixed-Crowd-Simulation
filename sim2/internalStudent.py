import fsm1 as machine
import random

# office = {'Admin': (200, 150, 100), 'CC3': (100, 450, 50), 'Ground': (400, 300, 125),
#               'HQ': (550, 100, 20), 'Cafeteria': (500, 50, 25)}

#     doors = {'Main-Gate': (150, 0, 0), 'Pocket-Gate': (400, 0, 0)}

officeName = ["Pocket-Gate", "HQ", "Ground", "CC3"]

def transitionsNoProbability(txt):
    return (officeName[txt+1], txt+1)

def transitionsProbability(txt):
    probability = random.randint(0,1000)
    if (probability <= 500):
        return (officeName[txt+1], txt+1)
    else:
        return (officeName[txt+2], txt+2)

def transitionsExit1(txt):
    return (officeName[0], None)

def FSM():
    user = machine.fsm()
    user.addState (officeName[0], transitionsProbability, end_state=1)
    user.addState (officeName[1], transitionsNoProbability)
    user.addState (officeName[2], transitionsNoProbability)
    user.addState (officeName[3], transitionsExit1)
    user.setStart (officeName[0])
    
    return user


# hello = FSM()
# isOver = False
# while not isOver:
#     (isOver, nextState) = hello.getNextState()
#     print nextState
