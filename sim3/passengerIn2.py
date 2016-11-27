import fsm1 as machine
import random

officeName = ["Entry2", "W1", "W2", "W3", "W4", "P1", "P2", "P3"]

def transitionsNoProbability(txt):
    return (officeName[txt+1], txt+1)

def transitionsEntry(txt):
    probability = random.randint(0,7000)
    if (probability <= 1000):
        return (officeName[txt+1], txt+1)
    elif (probability <= 2000):
        return (officeName[txt+2], txt+2)
    elif (probability <= 3000):
        return (officeName[txt+3], txt+3)
    elif (probability <= 4000):
        return (officeName[txt+4], txt+4)
    elif (probability <= 5000):
        return (officeName[txt+5], None)
    elif (probability <= 6000):
        return (officeName[txt+6], None)
    else:
        return (officeName[txt+7], None)

def transitionsWaiting(txt):
    probability = random.randint(0,300)
    if (probability <= 1000):
        txt = 5
    elif (probability <= 2000):
        txt = 6
    else:
        txt = 7
    return (officeName[txt], None)

def FSM():
    user = machine.fsm()
    user.addState (officeName[0], transitionsEntry)
    user.addState (officeName[1], transitionsWaiting)
    user.addState (officeName[2], transitionsWaiting)
    user.addState (officeName[3], transitionsWaiting)
    user.addState (officeName[4], transitionsWaiting)
    user.addState (officeName[5], None, end_state=1)
    user.addState (officeName[6], None, end_state=1)
    user.addState (officeName[7], None, end_state=1)
    user.setStart (officeName[0])
    
    return user


# hello = FSM()
# isOver = False
# while not isOver:
#     (isOver, nextState) = hello.getNextState()
#     print nextState
