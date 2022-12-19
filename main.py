import glob
from os.path import exists
from data_pulling.DataPull import DataPull
from data_backtesting import KrownCrossLong
from datetime import datetime
from data_pulling.DataPull import DataPull
from backtesting.backtesting import Backtest
import os
import pandas as pd
from data_backtesting.KrownCrossLong import KrownCrossLong
from data_backtesting.KrownCrossShort import KrownCrossShort
from data_backtesting.KrownCrossBoth import KrownCrossBoth
from time import time
"""
Plan for Dec7th
Work part 1 of my backtesting engine requirments list: This revolves around data pulling from nomics

Create a Data_pull class with the following parameters: Pair, timeframe,
"""


def load_data_file(path):
    if not exists(path):
        print(f"Error loading file {path}")
        return None
    #  Load data file
    df1 = pd.read_csv(path)
    if df1 is None or len(df1) == 0:
        print(f"Empty file: {path}")
        return None

    # Name columns per documentation of Backtest.py from backtesting package
    df1 = df1.set_index('timestamp')
    df1 = df1.rename(columns={'timestamp': 'Date', "open": "Open", "close": "Close", "low": "Low", "high": "High",
                              "volume": "Volume"})
    df1.index = pd.to_datetime(df1.index)

    return df1


def run_backtest(path, strategy, optimize_dict, cash, optimize) -> dict:
    # If exclusive orders (each new order auto-closes previous orders/position),
    # cancel all non-contingent orders and close all open trades beforehand
    df = load_data_file(path)
    bt = Backtest(df, strategy, cash=cash, commission=.00075, trade_on_close=True,
                  exclusive_orders=True, hedging=False)
    stats = bt.run()
    # print(stats)
    # print('\n\n')
    # bt.plot()
    if optimize:
        stats, heatmap = bt.optimize(**optimize_dict,
                                     maximize='Equity Final [$]',
                                     max_tries=200,
                                     random_state=0,
                                     return_heatmap=True)
        print(stats)
        print(stats.tail())
        print(stats._strategy)
        print(heatmap)
        bt.plot(plot_volume=True, plot_pl=True, filename='./data/backtest_graphics/test.html', open_browser=False)
        heatmap.plot()
    return stats

if __name__ == "__main__":
    # The below is for data pulling stuff
    # start = datetime(year=2011, month=8, day=1, hour=0, minute=0, second=0)
    # end = datetime(year=2022, month=12, day=16, hour=23, minute=0, second=0)
    # dp1 = DataPull(quote="USD", base="BTC", time_frame_unit="h", time_frame_quantity="1", start=start, end=end)
    # f = open("data/json_raw/BTC-USD__1h__2022-01-01T00:00:00__2022-12-01T00:00:00")
    # print(get_missing_data_set_times(json.load(f)))
    # dp1.pull_and_export()
    # print("-------------1 HOUR-------------")

    file_path = 'data/df_raw/btc_bull/4h/BTC-USD__1h__2019-03-18T00:00:00__2019-09-01T23:00:00.csv'
    t = time()
    run_backtest(file_path, KrownCrossBoth, KrownCrossBoth.OPTIMIZE_VALUES, 100000, False)
    print(time()-t)


