
import numpy as np
import random as rand


class QLearner(object):

    def __init__(self, \
        num_states=100, \
        num_actions = 4, \
        alpha = 0.2, \
        gamma = 0.9, \
        rar = 0.5, \
        radr = 0.99, \
        dyna = 0, \
        verbose = False):

        self.verbose = verbose
        self.s = 0
        self.a = 0
        self.num_states = num_states
        self.num_actions = num_actions

        self.alpha = alpha
        self.gamma = gamma
        self.rar = rar
        self.radr = radr
        self.dyna = dyna

        self.Q = np.zeros((self.num_states, self.num_actions))

    def querysetstate(self, s):
        """
        @summary: Update the state without updating the Q-table
        @param s: The new state
        @returns: The selected action
        """
        ## set current state to s
        self.s = s

        ## no random action
        if (self.Q[s, 0] == self.Q[s, 1] and self.Q[s, 0] == self.Q[s, 2]):
            action = self.a
        else:
            action = self.Q[s, :].argmax()

        ## set current action to a
        self.a = action

        if self.verbose: print "s =", s,"a =",action
        return action

    def query(self,s_prime,r):
        """
        @summary: Update the Q table and return an action
        @param s_prime: The new state
        @param r: The ne state
        @returns: The selected action
        """

        ## update the Q table
        ## Q'[s, a] = (1 - alpha)*Q[s, a] + alpha * (r + gamma*Q[s', argmaxQ[s', a'])
        #print "Q[", self.s, self.a, "]"
        self.Q[self.s, self.a] = (1 - self.alpha)*self.Q[self.s, self.a] + \
                                 self.alpha * (r + self.gamma*self.Q[s_prime, self.Q[s_prime, :].argmax()])

        ## if random number < rar, take random action
        ran_float = np.random.random()
        if (ran_float <= self.rar):
            action = rand.randint(0, self.num_actions - 1)
        else:
            if (self.Q[s_prime, 0] == self.Q[s_prime, 1] and self.Q[s_prime, 0] == self.Q[s_prime, 2]):
                action = self.a
            else:
                action = self.Q[s_prime, :].argmax()

        ## update rar
        self.rar = self.rar * self.radr

        ## update current state and action
        self.s = s_prime
        self.a = action
        ##print self.Q[0:100, ]

        if self.verbose: print "s =", s_prime,"a =",action,"r =",r
        ##print "s =", s_prime, "a =", action, "r =", r
        return action


    def author(self):
        return 'hli651'

if __name__=="__main__":
    print "Remember Q from Star Trek? Well, this isn't him"
