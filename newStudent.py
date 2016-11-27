import fsm1 as machine
import random

officeName = ["Entry", "Reception", "Exam-Cell", "Dean-Affairs", "Accounts-Student", "Bank", "COW", "Exit1", "Exit2"]

def transitionsNoProbability(txt):
    return (officeName[txt+1], txt+1)

def transitionsProbability(txt):
    probability = random.randint(0,1000)
    if (probability <= 500):
        return (officeName[txt+1], txt+1)
    else:
        return (officeName[txt+2], txt+2)

def transitionsExit1(txt):
    return (officeName[7], None)
def transitionsExit2(txt):
    return (officeName[8], None)

def FSM():
    user = machine.fsm()
    user.addState (officeName[0], transitionsNoProbability)
    user.addState (officeName[1], transitionsNoProbability)
    user.addState (officeName[2], transitionsProbability)
    user.addState (officeName[3], transitionsNoProbability)
    user.addState (officeName[4], transitionsProbability)
    user.addState (officeName[5], transitionsExit1)
    user.addState (officeName[6], transitionsExit2)
    user.addState (officeName[7], None, end_state=1)
    user.addState (officeName[8], None, end_state=1)
    user.setStart (officeName[0])
    
    return user


# hello = fsm()
# isOver = False
# while not isOver:
#     (isOver, nextState) = hello.getNextState()
#     print nextState
