import fsm3 as machine
import random

officeName = ["Entry", "Reception", "Dean-Affairs", "Accounts-Priority", "Exit1", "Exit2"]

def transitionsNoProbability(txt):
    return (officeName[txt+1], txt+1)

def transitionsChooseExit(txt):
    probability = random.randint(0,1000)
    if (probability <= 500):
        return (officeName[4], None)
    else:
        return (officeName[5], None)

def FSM():
    user = machine.fsm()
    user.addState (officeName[0], transitionsNoProbability)
    user.addState (officeName[1], transitionsNoProbability)
    user.addState (officeName[2], transitionsNoProbability)
    user.addState (officeName[3], transitionsChooseExit)
    user.addState (officeName[4], None, end_state=1)
    user.addState (officeName[5], None, end_state=1)
    user.setStart (officeName[0])
    
    return user

# hello = fsm()
# hello.run(0)
