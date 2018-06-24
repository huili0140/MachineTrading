
import pandas as pd
import numpy as np
import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import os
from util import get_data, plot_data


def indicators(start_date, end_date, symbol, lookback = 14, plot = False):

    # Read in the SPY & symbol data (adj_close) using util.py
    dates = pd.date_range(start_date, end_date)
    prices_all = get_data(symbol, dates)  # automatically adds SPY
    price = prices_all/prices_all.ix[1, :]

    symbols = symbol

    ## Indicator 1: price/SMA
    sma = price.cumsum()
    sma.values[lookback:, :] = (sma.values[lookback:, :] - sma.values[:-lookback, :]) / lookback
    sma.ix[:lookback, :] = np.nan
    sma_ratio = price / sma
    ##print sma_ratio.head()

    if plot == True:
        for sym in symbols:

            df_sym = price[[sym]]
            df_sym = df_sym.rename(columns={sym:'Price'})
            df_sym['SMA'] = sma[sym]
            df_sym['Price/SMA'] = sma_ratio[sym]

            plt.figure(figsize=(6, 4))
            plt.plot(df_sym)
            plt.legend(df_sym.columns.values, loc=4, prop={'size': 9})
            plt.title("Indicator: Price/SMA of " + sym)
            plt.ylabel('Normalized Value')
            plt.grid(False)
            plt.setp(plt.gca().get_xticklabels(), rotation=30)
            plt.show()

    ## Indicator 2: Bollinger Bands
    rolling_std = price.rolling(window = lookback, min_periods=lookback).std()
    top_band = sma + 2*rolling_std
    bottom_band = sma - 2*rolling_std
    bbp = (price - bottom_band) / (top_band - bottom_band)

    if plot == True:
        for sym in symbols:

            df_sym = price[[sym]]
            df_sym = df_sym.rename(columns={sym:'Price'})
            df_sym['Top_Bollinger_Band'] = top_band[sym]
            df_sym['Bottom_Bollinger_Band'] = bottom_band[sym]

            fig = plt.figure(figsize = (6, 6))
            G = gridspec.GridSpec(4, 1)
            top_panel = fig.add_subplot(G[0:3, :])
            top_panel.set_xticklabels([])
            plt.plot(df_sym)
            plt.legend(df_sym.columns.values, loc=4, prop={'size': 9})
            plt.title("Indicator: Bollinger Band Percentage of " + sym)
            plt.ylabel('Normalized Value')
            plt.grid(False)
            bottom_panel = fig.add_subplot(G[3, :])
            plt.plot(bbp[sym], 'k', label = 'Bollinger Band Percentage')
            plt.legend(loc=4, prop={'size': 9})
            plt.ylabel('Percentage')
            plt.grid(False)
            plt.setp(plt.gca().get_xticklabels(), rotation=30)
            plt.show()

    ## Indicator 3: Momentum
    momentum = price.copy()
    momentum.values[lookback:, :] = momentum.values[lookback:, :] / momentum.values[:-lookback, :] - 1
    momentum.ix[:lookback, :] = np.nan

    if plot == True:
        for sym in symbols:
            df_sym = price[[sym]]
            df_sym = df_sym.rename(columns={sym: 'Price'})
            df_sym['Top_Bollinger_Band'] = top_band[sym]
            df_sym['Bottom_Bollinger_Band'] = bottom_band[sym]

            fig = plt.figure(figsize=(6, 6))
            G = gridspec.GridSpec(4, 1)
            top_panel = fig.add_subplot(G[0:3, :])
            top_panel.set_xticklabels([])
            plt.plot(df_sym)
            plt.legend(df_sym.columns.values, loc=4, prop={'size': 9})
            plt.title("Indicator: Momentum of " + sym)
            plt.ylabel('Normalized Value')
            plt.grid(False)
            bottom_panel = fig.add_subplot(G[3, :])
            plt.plot(momentum[sym], 'k', label='Momentum')
            plt.legend(loc=4, prop={'size': 9})
            plt.ylabel('Momentum')
            plt.grid(False)
            plt.setp(plt.gca().get_xticklabels(), rotation=30)
            plt.show()

    return momentum, sma_ratio, bbp



def author():
    return 'hli651'  # replace tb34 with your Georgia Tech username


def test_code():

    start_date = dt.datetime(2008, 1, 1)
    end_date = dt.datetime(2011, 12, 31)
    ##end_date = dt.datetime(2008, 6, 30)
    symbol = ["JPM"]
    momentum, sma_ratio, bbp = indicators(start_date, end_date, symbol, 14, True)

if __name__ == "__main__":
    test_code()

