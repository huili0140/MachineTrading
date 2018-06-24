
import datetime as dt
import pandas as pd
import util as ut
import random
import indicators as ind
from util import get_data, plot_data
import numpy as np
import QLearner as ql

class StrategyLearner(object):

    # constructor
    def __init__(self, verbose = True, impact=0.0):
        self.verbose = verbose
        self.impact = impact
        ##print "StrategyLearner Condition: ", verbose, " and ", impact
        ## initialize the qlearner
        self.learner = ql.QLearner(num_states=10000000, \
                              num_actions=3, \
                              alpha=0.2, \
                              gamma=0.9, \
                              rar=0.98, \
                              radr=0.999, \
                              dyna=0, \
                              verbose=self.verbose)

    # this method should create a QLearner, and train it for trading
    def addEvidence(self, symbol = "IBM", \
        sd=dt.datetime(2008,1,1), \
        ed=dt.datetime(2009,1,1), \
        sv = 10000):

        # add your code to do learning here

        # compute the technical indicators
        sym = [symbol]
        momentum3, sma_ratio3, bbp3 = ind.indicators(sd, ed, sym, 70, False)
        momentum14, sma_ratio14, bbp14 = ind.indicators(sd, ed, sym, 14, False)

        # create feature array and discretize the values of the features
        row = momentum3.values[:, 0].size - 70
        features = np.zeros((row, 7))
        features[:, 0] = momentum3.ix[70:, symbol].values
        features[:, 1] = sma_ratio3.ix[70:, symbol].values
        features[:, 2] = bbp3.ix[70:, symbol].values
        features[:, 3] = momentum14.ix[70:, symbol].values
        features[:, 4] = sma_ratio14.ix[70:, symbol].values
        features[:, 5] = bbp14.ix[70:, symbol].values

        fmin = features.min(axis=0)
        fmax = features.max(axis=0)
        for i in range(6):
            bins = np.linspace(fmin[i], fmax[i], 9)
            features[:, i] = np.digitize(features[:, i], bins)
        # print features[0:30, ]

        for i in range(row):
            features[i, 6] = int(str(int(features[i, 0])) + str(int(features[i, 1])) + str(int(features[i, 2])) +
                                 str(int(features[i, 3])) + str(int(features[i, 4])) + str(int(features[i, 5])))
        # print features[0:30, ]

        # Read in the SPY & symbol data (adj_close) using util.py
        dates = pd.date_range(sd, ed)
        prices_all = get_data(sym, dates)  # automatically adds SPY
        price = prices_all / prices_all.ix[0, :]
        price = price.ix[70:, symbol].values
        # print(price[0:9])

        ## initiate the qlearner
        pre_action = 0 ## track the previous action
        cur_action = self.learner.querysetstate(int(features[0, 6]))
        ##print("state: ", features[0, 6], "action", cur_action)

        ## update the qlearner until converge
        i = 1
        total_reward = 0
        last_reward = 0
        while i < row:
            cur_state = int(str(int(features[i, 6])) + str(int(pre_action)))

            ##print("days of ", i, "state: ", cur_state, "action: ", cur_action)

            if cur_action == 1:  ## buy and long 1000
                if pre_action == 0:
                    cur_reward = (price[i] - price[i - 1])*1000 - price[i-1]*1000*self.impact
                elif pre_action == 1:
                    cur_reward = (price[i] - price[i - 1])*1000
                elif pre_action == 2:
                    cur_reward = (price[i] - price[i - 1])*1000 - price[i-1]*2000*self.impact
            elif cur_action == 2:  ## sell and short 1000
                if pre_action == 0:
                    cur_reward = (price[i-1] - price[i])*1000 - price[i-1]*1000*self.impact
                elif pre_action == 1:
                    cur_reward = (price[i-1] - price[i])*1000 - price[i-1]*2000*self.impact
                elif pre_action == 2:
                    cur_reward = (price[i-1] - price[i])*1000
            else:  ## no holding
                if pre_action == 0:
                    cur_reward = 0
                elif pre_action == 1:
                    cur_reward = - price[i-1]*1000*self.impact
                elif pre_action == 2:
                    cur_reward = - price[i-1]*1000*self.impact

            total_reward = total_reward + cur_reward
            action = self.learner.query(cur_state, cur_reward)

            ##print("current reward: ", cur_reward, "next_action: ", action)
            pre_action = cur_action
            cur_action = action
            i = i + 1

        j = 0
        while total_reward != last_reward:
            ## initiate the qlearner
            pre_action = 0  ## track the previous action
            cur_action = self.learner.querysetstate(int(str(int(features[0, 6])) + str(int(pre_action))))

            ##print "total reward is ", total_reward, " last_reward is ", last_reward
            i = 1
            last_reward = total_reward
            total_reward = 0
            while i < row:
                cur_state = int(str(int(features[i, 6])) + str(int(pre_action)))

                if cur_action == 1:  ## buy and long 1000
                    if pre_action == 0:
                        cur_reward = (price[i] - price[i - 1]) * 1000 - price[i - 1] * 1000 * self.impact
                    elif pre_action == 1:
                        cur_reward = (price[i] - price[i - 1]) * 1000
                    elif pre_action == 2:
                        cur_reward = (price[i] - price[i - 1]) * 1000 - price[i - 1] * 2000 * self.impact
                elif cur_action == 2:  ## sell and short 1000
                    if pre_action == 0:
                        cur_reward = (price[i - 1] - price[i]) * 1000 - price[i - 1] * 1000 * self.impact
                    elif pre_action == 1:
                        cur_reward = (price[i - 1] - price[i]) * 1000 - price[i - 1] * 2000 * self.impact
                    elif pre_action == 2:
                        cur_reward = (price[i - 1] - price[i]) * 1000
                else:  ## no holding
                    if pre_action == 0:
                        cur_reward = 0
                    elif pre_action == 1:
                        cur_reward = - price[i - 1] * 1000 * self.impact
                    elif pre_action == 2:
                        cur_reward = - price[i - 1] * 1000 * self.impact

                total_reward = total_reward + cur_reward
                action = self.learner.query(cur_state, cur_reward)
                '''
                if (cur_reward != 0):
                    print "\ndays of ", i, "state: ", cur_state, "action: ", cur_action, "pre-action: ", pre_action
                    print "price[i] ", price[i], "  price[i-1] ", price[i - 1], "  impact ", self.impact
                    print "current reward: ", cur_reward, "next_action: ", action
                '''
                pre_action = cur_action
                cur_action = action
                i = i + 1

            j = j + 1
            ##print "j is ", j, "total reward is ", total_reward, " last_reward is ", last_reward

    # this method should use the existing policy and test it against new data
    def testPolicy(self, symbol = "IBM", \
        sd=dt.datetime(2009,1,1), \
        ed=dt.datetime(2010,1,1), \
        sv = 10000):

        # compute the technical indicators
        sym = [symbol]
        momentum3, sma_ratio3, bbp3 = ind.indicators(sd, ed, sym, 70, False)
        momentum14, sma_ratio14, bbp14 = ind.indicators(sd, ed, sym, 14, False)

        # create feature array and discretize the values of the features
        row = momentum3.values[:, 0].size - 70
        features = np.zeros((row, 7))
        features[:, 0] = momentum3.ix[70:, symbol].values
        features[:, 1] = sma_ratio3.ix[70:, symbol].values
        features[:, 2] = bbp3.ix[70:, symbol].values
        features[:, 3] = momentum14.ix[70:, symbol].values
        features[:, 4] = sma_ratio14.ix[70:, symbol].values
        features[:, 5] = bbp14.ix[70:, symbol].values

        fmin = features.min(axis=0)
        fmax = features.max(axis=0)
        for i in range(6):
            bins = np.linspace(fmin[i], fmax[i], 9)
            features[:, i] = np.digitize(features[:, i], bins)
        # print features[0:30, ]

        for i in range(row):
            features[i, 6] = int(str(int(features[i, 0])) + str(int(features[i, 1])) + str(int(features[i, 2])) +
                                 str(int(features[i, 3])) + str(int(features[i, 4])) + str(int(features[i, 5])))
        # print features[0:30, ]

        # build a set of trades
        dates = pd.date_range(sd, ed)
        prices_all = ut.get_data([symbol], dates)  # automatically adds SPY
        holdings = prices_all[[symbol, ]]  # only portfolio symbols
        holdings.values[:, :] = 0  # set them all to nothing

        pre_action = 0
        for i in (range(row)):
            cur_action = self.learner.querysetstate(int(str(int(features[i, 6])) + str(int(pre_action))))
            ##print "row is ", i, " cur_action is ", cur_action
            if cur_action == 1:  ## buy and long 1000
                holdings.values[70 + i, :] = 1000
            elif cur_action == 2:  ## sell and short 1000
                holdings.values[70 + i, :] = -1000
            else:  ## no holding
                holdings.values[70 + i, :] = 0
            pre_action = cur_action


        trades = holdings.copy()
        trades[1:] = trades.diff()
        if self.verbose: print type(trades) # it better be a DataFrame!
        if self.verbose: print trades
        if self.verbose: print prices_all
        return trades

    def author(self):
        return 'hli651'  # replace tb34 with your Georgia Tech username


if __name__=="__main__":

    print "One does not simply think up a strategy"
