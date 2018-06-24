
import pandas as pd
import numpy as np
import datetime as dt
import os
from util import get_data, plot_data


def compute_portvals(orders, start_date, end_date, start_val=100000, commission=9.95, impact=0.005):
    # this is the function the autograder will call to test your code
    # NOTE: orders_file may be a string, or it may be a file object. Your
    # code should work correctly with either input

    # if there is no order at all
    if orders.empty:
        dates = pd.date_range(start_date, end_date)
        prices_all = get_data(['SPY'], dates)  # automatically adds SPY
        result = pd.DataFrame(index=prices_all.index,
                              data=start_val, columns=["Value"])
        return result


    # if there are orders
    # Read in adjusted closing prices for given symbols, date range
    syms = list(set(orders['Symbol'].tolist()))
    dates = pd.date_range(start_date, end_date)
    prices_all = get_data(syms, dates)  # automatically adds SPY
    prices = prices_all[syms]  # only portfolio symbols
    prices.fillna(method='ffill', inplace=True)
    prices.fillna(method='bfill', inplace=True)

    rv = pd.DataFrame(index=prices.index, columns=syms)
    rv['Count'] = 0
    rv = rv.fillna(0)  ## with 0s rather than NaNs
    rvAbs = rv.copy()  ## save the absolute trading volumn

    for i in range(orders.shape[0]):
        if (orders.iloc[i, 2] == "BUY"):
            rv.ix[orders.iloc[i, 0], orders.iloc[i, 1]] = rv.ix[orders.iloc[i, 0], orders.iloc[i, 1]] + orders.iloc[
                i, 3]
        else:
            rv.ix[orders.iloc[i, 0], orders.iloc[i, 1]] = rv.ix[orders.iloc[i, 0], orders.iloc[i, 1]] + -orders.iloc[
                i, 3]

        rv.ix[orders.iloc[i, 0], 'Count'] = rv.ix[orders.iloc[i, 0], 'Count'] + 1
        rvAbs.ix[orders.iloc[i, 0], orders.iloc[i, 1]] = rvAbs.ix[orders.iloc[i, 0], orders.iloc[i, 1]] + orders.iloc[
            i, 3]

    ## print rv.to_string()
    priceChange = rv.ix[:, syms] * prices
    priceChangeAbs = rvAbs.ix[:, syms] * prices

    ## Cash fluctuation
    priceChange['Cash'] = - priceChange.sum(axis=1) - commission * rv['Count'] - impact * priceChangeAbs.sum(axis=1)
    priceChangeCum = priceChange.cumsum()

    ## stock values
    priceSum = rv.ix[:, syms].cumsum() * prices
    priceSum['Cash'] = start_val + priceChangeCum['Cash']
    ## print priceSum.to_string()

    result = pd.DataFrame(index=rv.index, data=priceSum.sum(axis=1), columns = ["Value"])

    return result


def author():
    return 'hli651'  # replace tb34 with your Georgia Tech username


def test_code():
    # this is a helper function you can use to test your code
    # note that during autograding his function will not be called.
    # Define input parameters

    ##of = "./orders/orders-short.csv"
    of = "./orders/orders-01.csv"
    sv = 1000000

    # Process orders
    portvals = compute_portvals(orders_file=of, start_val=sv)
    if isinstance(portvals, pd.DataFrame):
        portvals = portvals[portvals.columns[0]]  # just get the first column
    else:
        "warning, code did not return a DataFrame"

    # Get portfolio stats
    # Here we just fake the data. you should use your code from previous assignments.
    start_date = dt.datetime(2008, 1, 1)
    end_date = dt.datetime(2008, 6, 1)
    cum_ret, avg_daily_ret, std_daily_ret, sharpe_ratio = [0.2, 0.01, 0.02, 1.5]
    cum_ret_SPY, avg_daily_ret_SPY, std_daily_ret_SPY, sharpe_ratio_SPY = [0.2, 0.01, 0.02, 1.5]

    # Compare portfolio against $SPX
    ##print "Date Range: {} to {}".format(start_date, end_date)
    ##print
    ##print "Sharpe Ratio of Fund: {}".format(sharpe_ratio)
    ##print "Sharpe Ratio of SPY : {}".format(sharpe_ratio_SPY)
    ##print
    ##print "Cumulative Return of Fund: {}".format(cum_ret)
    ##print "Cumulative Return of SPY : {}".format(cum_ret_SPY)
    ##print
    ##print "Standard Deviation of Fund: {}".format(std_daily_ret)
    ##print "Standard Deviation of SPY : {}".format(std_daily_ret_SPY)
    ##print
    ##print "Average Daily Return of Fund: {}".format(avg_daily_ret)
    ##print "Average Daily Return of SPY : {}".format(avg_daily_ret_SPY)
    ##print
    ##print "Final Portfolio Value: {}".format(portvals[-1])


if __name__ == "__main__":
    test_code()
