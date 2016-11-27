import fsm2 as machine
import random

officeName = ["Entry", "Director", "Dean-Academics", "Accounts-Priority", "Bank", "Exit1", "Exam-Cell", "Exit2"]

def transitionsNoProbability(txt):
    return (officeName[txt+1], txt+1)

def transitionsProbability(txt):
    probability = random.randint(0,1000)
    if (probability <= 500):
        return (officeName[txt+1], txt+1)
    else:
        return (officeName[txt+2], txt+2)

def transitionsDirector(txt):
    return (officeName[3], 3)

def transitionsDean(txt):
    return (officeName[6], 6)

def transitionsChooseExit(txt):
    probability = random.randint(0,1000)
    if (probability <= 500):
        return (officeName[5], None)
    else:
        return (officeName[7], None)

def transitionsExit1(txt):
    return (officeName[5], None)
def transitionsExit2(txt):
    return (officeName[7], None)

def FSM():
    user = machine.fsm()
    user.addState (officeName[0], transitionsProbability)
    user.addState (officeName[1], transitionsDirector)
    user.addState (officeName[2], transitionsDean)
    user.addState (officeName[3], transitionsNoProbability)
    user.addState (officeName[4], transitionsExit1)
    user.addState (officeName[5], None, end_state=1)
    user.addState (officeName[6], transitionsChooseExit)
    user.addState (officeName[7], None, end_state=1)
    user.setStart (officeName[0])
    
    return user

# hello = fsm()
# hello.run(0)
