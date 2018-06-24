# Machine Trading 

The Machine Trading strategies are based on Q-Learning with the technical indicators of the stock market: Price/Simple Moving Average, Bollinger Bands Percentage, and Momentum. The three indicators are calculated at short term with a lookback period of 14 days and long term with a lookback period of 70 days. 

The result of Strategy Learner Portfolio varies a little bit every time with in sample data since randomness is involved in the training process of Q-Leaner. The Q-Learner randomly explores all possible actions during training with the parameters of random action rate (rar) and random action decay rate (radr).


