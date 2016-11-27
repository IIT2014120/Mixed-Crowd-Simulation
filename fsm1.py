class fsm:
    'A finite state machine template class http://www.python-course.eu/finite_state_machine.php'
    def __init__(self, states_list = []):
        self.handlers = {}
        self.startState = None
        self.endStates = []
        self.current = None
        self.stateList = states_list

    def addState(self, name, handler, end_state=0):
        name = name.upper()
        self.stateList.append(name.upper())
        self.handlers[name] = handler
        if end_state:
            self.endStates.append(name)

    def setStart(self, name):
        self.startState = name.upper()
        self.current = self.stateList.index(name.upper())

    def run(self, cargo):
        try:
            handler = self.handlers[self.startState]
        except:
            raise InitializationError("must call .set_start() before .run()")
        if not self.endStates:
            raise  InitializationError("at least one state must be an end_state")
    
        while True:
            (newState, cargo) = handler(cargo)
            print(newState)
            if newState.upper() in self.endStates:
                print("reached ", newState)
                break 
            else:
                handler = self.handlers[newState.upper()]

    def getStateList (self):
        return self.stateList

    def getNextState(self):
        try:
            handler = self.handlers[self.stateList[self.current]]    
        except Exception as ex:
            print self.current, self.stateList
            raise    
        (newState, self.current) = handler(self.current)

        if newState.upper() in self.endStates:
            return (True, newState)
        else:
            return (False, newState)
