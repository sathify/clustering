
import mdp
import random, math

class Qlearner :

    def __init__(self, states, actions, alpha, gamma, world) :
        self.qtable = {}
        self.states = states
        self.actions = actions
        for s in states :
            for a in actions :
                self.qtable[(s,a)] = 0.0
        self.world = world
        self.temp = 2.0
        self.alpha = alpha
        self.gamma = gamma

        
    ### use boltzmann exploration to select an action
    def selectAction(self, state) :
        denom = sum([math.e ** (self.qtable[s]/self.temp) for s in self.qtable if s[0] == state])
        val = random.uniform(0,denom)
        total = 0.0
        for s in [item for item in self.qtable if item[0] == state] :
            total += math.e ** (self.qtable[s] / self.temp)
            if total > val :
                return s[1]

    def update(self, oldstate, action, newstate, reward) :
        actions=[self.qtable[(newstate,action)] for action in self.actions]
        bestaction = max(actions)
        self.qtable[(oldstate, action)] += self.alpha*(reward + self.gamma * bestaction - self.qtable[(oldstate, action)])
        

class World :
    def __init__(self, map) :
        self.map = map

    ### move the agent from one state to another according to the map's 
    ### transition function.
    def newState(self, statenum, action) :
        ttable = self.map.states[statenum].transitions[action]
        val = random.random()
        total = 0.0
        i = -1
        while total < val :
            i += 1
            total += ttable[i][0]
        return ttable[i][1].coords
        

    def atGoal(self, state) :
        return self.map.states[state].isGoal

    def reward(self, state) :
        if self.map.states[state].isGoal :
            return self.map.states[state].utility
        else :
            return -0.04


def learn() :
    m1 = mdp.Map()
    m1.getMapFromFile("rnGraph")
    w = World(m1)
    q = Qlearner(m1.states.keys(), ['up','down','left','right'], 
                 0.1, 0.8, w) 
    count = 0
    while True :
       oldstate = random.choice(q.states) 
       while not w.atGoal(oldstate) :
           a = q.selectAction(oldstate)
           newstate = w.newState(oldstate, a)
           r = w.reward(newstate)
           q.update(oldstate, a, newstate, r)
           oldstate = newstate
           count +=1
       print 'Iterations--->', count
       print 'found goal.'
       print q.qtable
       x=raw_input()
       
    
if __name__ == '__main__' :
    learn()