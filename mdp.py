
### code for representing/solving an MDP
### Most of this is complete. You should only need to complete the valueIteration and policyIteration methods.

import random

class State :

    def __init__(self, coordString=None) :
        self.utility = 0
        self.reward = 0.0
        ### an action maps to a list of probability/state pairs
        self.transitions = {}
        self.actions = []
        self.policy = None
        self.coords = coordString
        self.isGoal = False

    def computeEU(self, action) :
        return sum([trans[0] * trans[1].utility 
                    for trans in self.transitions[action]])

    def selectBestAction(self) :
        best = max([(self.computeEU(a), a) for a in self.actions])
        return best[1]

    def __eq__(self, other) :
        return self.coords == other.coords

    def __hash__(self) :
        return self.coords.__hash__()


class Map :

    def __init__(self) :
        self.states = {}
        self.error = 0.01
        self.gamma = 0.8

    def getState(self, name) :
        try :
            return self.states[name]
        except KeyError :
            return None

### you do this one. returns the number of iterations.
    def valueIteration(self) :
        delta= self.error * (1-self.gamma)/ self.gamma
        count=0
        ### initialize random utilities
        for s in self.states.values():
            if not s.isGoal:
                s.utility=random.random()            
                 
        while True:
            temp={}
            for state in self.states:
                if not self.states[state].isGoal:
                    ### New Utilities and policies
                    newPolicy=self.states[state].selectBestAction()
                    util =self.states[state].computeEU(newPolicy)
                    temp[state]=(self.states[state].reward + self.gamma * util, newPolicy)           
                    
            ### Update our original states with new utilities and get max value to see the change
            maxdeltas=[]
            for s in temp:
                maxdeltas.append(abs(self.states[s].utility - temp[s][0]))
                self.states[s].utility=temp[s][0]
                self.states[s].policy=temp[s][1]
    
            newdelta = max(maxdeltas)
            ### stop if there is very little change in all the deltas.
            count+=1
            if newdelta < delta:
                break    
                
        return count


### you do this one. returns number of iterations.       
    def policyIteration(self) :
     ### creating random policies for each state
        for s in self.states.values():
            if not s.isGoal:
                s.policy=random.choice(s.actions)
        count=0
        while True:
            oldlist=[s.policy for s in self.states.values()]
            tempStates={}
        
            ### Compute all the utilities
            for state in self.states:
                if not self.states[state].isGoal:
                    util = self.states[state].computeEU(self.states[state].policy)
                    tempStates[state]=self.states[state].reward + self.gamma* util
            
            ### Update original states
            for s in tempStates:
                self.states[s].utility=tempStates[s]
        
            ### Compute new policies from the new utilities
            for s in self.states.values():
                if not s.isGoal:
                    s.policy=s.selectBestAction()
           
            newlist=[s.policy for s in self.states.values()]
            ### if there is no change in all the policies we can stop            
            count+=1
            if oldlist==newlist:
                return count



    def getMapFromFile(self, fname) :
        with open(fname) as infile :
            for line in infile :
                if line.startswith("#") or len(line) < 2 :
                    pass
                elif line.startswith("gamma") :
                    self.gamma = float(line.split(":")[1])
                elif line.startswith("error") :
                    self.error = float(line.split(":")[1])
                elif line.startswith("reward") :
                    reward = float(line.split(":")[1])
                elif line.startswith("goals") :
                    gs = line.split(":")[1]
                    values = gs.split()
                    for i in range(0,len(values),2) :
                        self.states[values[i]] = State(values[i])
                        self.states[values[i]].isGoal = True
                        self.states[values[i]].utility = float(values[i+1])
                        self.states[values[i]].reward = float(values[i+1])
                ### state transitions
                else :
                    values = line.split()
                    if values[0] not in self.states :
                        self.states[values[0]] = State(values[0])
                        self.states[values[0]].isGoal = False
                        self.states[values[0]].reward = reward
                    action = values[1]
                    self.states[values[0]].actions.append(action)
                    transitions = []
                    for x in values[2:] :
                        prob, name = x.split(":") 
                        if not self.getState(name) :
                            self.states[name] = State(name)
                            self.states[name].isGoal = False
			    self.states[name].reward = reward
                        transitions.append((float(prob), self.getState(name)))
                    self.states[values[0]].transitions[action] = transitions


if __name__=='__main__':
    map=Map()
    map.getMapFromFile('rnGraph')
    Correct=[None,None,'right','right','right','up','up','right','up','left','up']
    
    print 'valueIteration: Iterations ->',map.valueIteration()
    list = [(s.coords, s.utility, s.policy) for s in map.states.values()]
    for item in list: print item
    print'------------------------------'
    print 'Policy Iteration: Iterations ->',map.policyIteration()
    list = [(s.coords, s.utility, s.policy) for s in map.states.values()]
    for item in list: print item
    
    
