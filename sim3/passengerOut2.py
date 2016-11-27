import fsm3 as machine
import random

officeName = ["P1", "P2", "P3", "W1", "W2", "W3", "W4", "Exit2"]

def transitionsPlatform(txt):
    probability = random.randint(0,5000)
    if (probability <= 1000):
        txt = 3
    elif (probability <= 2000):
        txt = 4
    elif (probability <= 3000):
        txt = 5
    elif (probability <= 4000):
        txt = 6
    else:
        txt = 7
    return (officeName[txt], txt)

def transitionsWaiting(txt):
    return (officeName[7], None)

def FSM():
    user = machine.fsm()
    user.addState (officeName[0], transitionsPlatform)
    user.addState (officeName[1], transitionsPlatform)
    user.addState (officeName[2], transitionsPlatform)
    user.addState (officeName[3], transitionsWaiting)
    user.addState (officeName[4], transitionsWaiting)
    user.addState (officeName[5], transitionsWaiting)
    user.addState (officeName[6], transitionsWaiting)
    user.addState (officeName[7], None, end_state=1)
    user.setStart (officeName[0])
    
    return user


# hello = FSM()
# isOver = False
# while not isOver:
#     (isOver, nextState) = hello.getNextState()
#     print nextState
