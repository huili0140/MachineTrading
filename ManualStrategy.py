
import pandas as pd
import numpy as np
import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import os
from util import get_data, plot_data
import marketsimcode as ms
import indicators as ind

def testPolicy(symbol, sd, ed, sv):

    # Read in the SPY & symbol data (adj_close) using util.py
    momentum3, sma_ratio3, bbp3 = ind.indicators(sd, ed, symbol, 70, False)
    momentum14, sma_ratio14, bbp14 = ind.indicators(sd, ed, symbol, 14, False)
    start = momentum3.index[0].date()

    holdings = momentum3.copy()
    holdings.ix[:, ] = np.nan

    holdings[((momentum3 > 0) & (sma_ratio3 < 0.95)) | (bbp3 < 0)] = 1000
    holdings[((momentum3 < 0) & (sma_ratio3 > 1.05)) | (bbp3 > 1)] = -1000
    holdings[((momentum14 > 0) & (sma_ratio14 < 0.95)) | (bbp14 < 0)] = 1000
    holdings[((momentum14 < 0) & (sma_ratio14 > 1.05)) | (bbp14 > 1)] = -1000
    #print holdings.head(50)

    orders = holdings.copy()
    orders.ffill(inplace=True)
    orders.fillna(0, inplace=True)
    orders[1:] = orders.diff()
    #print orders.head(50)

    orders = orders.loc[(orders != 0).any(axis=1)]
    orders_list = []
    for day in orders.index:
        for sym in symbol:
            if (sym != 'SPY') & (orders.ix[day, sym] > 0):
                orders_list.append([day.date(), sym, 'BUY', orders.ix[day, sym]])
            elif (sym != 'SPY') & (orders.ix[day, sym] < 0):
                orders_list.append([day.date(), sym, 'SELL', -orders.ix[day, sym]])

    df_trades = pd.DataFrame(np.array(orders_list), columns=['Date', 'Symbol', 'Order', 'Shares'])
    ##print df_trades.to_string()
    return df_trades, start

def author():
    return 'hli651'  # replace tb34 with your Georgia Tech username


def test_code():

    start_date = dt.datetime(2008, 1, 1)
    end_date = dt.datetime(2009, 12, 31)
    start_value = 100000
    symbol = ["JPM"]
    commission = 9.95
    impact = 0.005

    ## Manual strategy
    df_trades, start = testPolicy(symbol, start_date, end_date, start_value)
    manual_port_val = ms.compute_portvals(df_trades, start_date, end_date, start_value, commission, impact)
    print "Rule Based Portfolio"
    port_status(manual_port_val)

    ## Benchmark portfolio
    benchmark = []
    benchmark.append([start, symbol[0], 'BUY', 1000])
    benchmark_trades = pd.DataFrame(np.array(benchmark), columns=['Date', 'Symbol', 'Order', 'Shares'])
    ##print benchmark_trades
    benchmark_port_val = ms.compute_portvals(benchmark_trades, start_date, end_date, start_value, commission, impact)
    print "\nBenchmark Portfolio"
    port_status(benchmark_port_val)

    ## Plot the chart of Benchmark and Best Portfolio
    value = manual_port_val.copy()
    value = value.rename(columns={'Value':'Rule Based Portfolio'})
    value['Benchmark Portfolio'] = benchmark_port_val['Value']
    value = value / value.ix[0, :]

    plt.figure(figsize=(6, 4))
    plt.plot(value)
    plt.gca().get_lines()[0].set_color("black")
    plt.gca().get_lines()[1].set_color("blue")
    plt.legend(value.columns.values, loc=0, prop={'size': 9})
    plt.title("Rule Based Strategy vs. Benchmark")
    plt.ylabel('Normalized Value')
    plt.grid(False)
    plt.setp(plt.gca().get_xticklabels(), rotation=30)

    xcoords = df_trades.loc[df_trades['Order'] == 'SELL']['Date']
    for xc in xcoords:
        plt.axvline(x=xc, color = 'red',linestyle = 'dashed', linewidth = 1)

    xcoords = df_trades.loc[df_trades['Order'] == 'BUY']['Date']
    for xc in xcoords:
        plt.axvline(x=xc, color='green', linestyle='dashed', linewidth=1)
    plt.show()

def port_status(port_val):
    cr = port_val.ix[-1] / port_val.ix[0] - 1
    daily_returns = (port_val.ix[1:] / port_val.ix[:-1].values) - 1
    adr = daily_returns.mean()
    sddr = daily_returns.std()
    print "Cumulative Return: {}".format(cr['Value'])
    print "Mean of Daily Return: {}".format(adr['Value'])
    print "Standard Deviation of Daily Return: {}".format(sddr['Value'])

if __name__ == "__main__":
    test_code()


## olt.axvline(std, color = 'r', linestyle = 'dashed', linewidth = 1)