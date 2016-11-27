import fsm as machine
import random

officeName = ["Entry", "Exam-Cell", "COW", "Bank", "Accounts-Student", "Exit1", "Exit2"]

def transitionsNoProbability(txt):
    return (officeName[txt+1], txt+1)

def transitionsProbability(txt):
    probability = random.randint(0,1000)
    if (probability <= 500):
        return (officeName[txt+1], txt+1)
    else:
        return (officeName[txt+2], txt+2)

def transitionBank(txt):
    probability = random.randint(0,1000)
    if (probability <= 500):
        return (officeName[txt+1], txt+1)
    else:
        return (officeName[txt+2], None)

def transitionAcc(txt):
    probability = random.randint(0,1000)
    if (probability <= 500):
        return (officeName[txt+1], None)
    else:
        return (officeName[txt+2], None)       

def FSM():
    user = machine.fsm()
    user.addState (officeName[0], transitionsNoProbability)
    user.addState (officeName[1], transitionsNoProbability)
    user.addState (officeName[2], transitionsProbability)
    user.addState (officeName[3], transitionBank)
    user.addState (officeName[4], transitionAcc)
    user.addState (officeName[5], None, end_state=1)
    user.addState (officeName[6], None, end_state=1)
    user.setStart (officeName[0])
    
    return user

# hello = fsm()
# hello.run(0)
