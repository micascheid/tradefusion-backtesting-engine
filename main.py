import glob
from os.path import exists
import json
import nomics
from data_pulling import NomicsAPI
from data_pulling.DataPull import DataPull
from data_backtesting import KrownCrossLong
from datetime import datetime, timedelta
from data_pulling.DataPull import DataPull, export_df
from backtesting.backtesting import Backtest
import os
import pandas as pd
from data_backtesting.KrownCrossLong import KrownCrossLong
from data_backtesting.KrownCrossShort import KrownCrossShort
from data_backtesting.KrownCrossBoth import KrownCrossBoth
from data_backtesting.ColoradoSnowPack import ColoradoSnowPack
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
    print(stats)
    # print('\n\n')
    bt.plot()
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
        # bt.plot(plot_volume=True, plot_pl=True, filename='./data/backtest_graphics/test.html', open_browser=True)
        # heatmap.plot()
    return stats

def get_missing_data_set_times(json_data_list):
    results = json_data_list
    HOUR_ADD = timedelta(minutes=5)
    time_compare = results[0]['timestamp']
    missing_times = []
    for x in range(len(results)):
        while not time_compare == results[x]['timestamp']:
            missing_times.append(time_compare)
            time_next = datetime.strptime(time_compare.strip('Z'), "%Y-%m-%dT%H:%M:%S")
            time_compare = (time_next + HOUR_ADD).isoformat() + "Z"
        if time_compare == results[x]['timestamp']:
            time_next = datetime.strptime(time_compare.strip('Z'), "%Y-%m-%dT%H:%M:%S")
            time_compare = (time_next + HOUR_ADD).isoformat() + "Z"
    return missing_times

if __name__ == "__main__":
    # The below is for data pulling stuff
    start = datetime(year=2017, month=12, day=17, hour=0, minute=0, second=0)
    end = datetime(year=2021, month=11, day=8, hour=23, minute=55, second=0)
    # dp1 = DataPull(exchange="gdax", market="BTC", time_frame_unit="m", time_frame_quantity="5", start=start, end=end)
    dp1 = DataPull(exchange="gdax", market="BTC-USD", time_frame_unit="m", time_frame_quantity="5", start=start,
                   end=end)
    # f = open('data/json_raw/BTC-USD__5m__2011-11-18T00:00:00__2018-12-15T00:00:00')
    # print(get_missing_data_set_times(json.load(f)))
    dp1.pull_and_export()

    # f = open('data/df_raw/BTC-USD__5m__2020-01-01T00:00:00__2022-12-01T00:00:00.csv', 'r')
    # json_obj = pd.json_normalize(json.loads(f.read()))
    # df = pd.DataFrame.from_records(json_obj)
    # if df.isna().any().any():
    #     print(True)

    # export_df('BTC-USD__5m__2022-01-01T00:00:00__2022-12-01T00:00:00.csv', json_obj)

    # print("-------------1 HOUR-------------")

    file_path = 'data/df_raw/gdax-BTC-USD__5m__2022-01-15T00:00:00__2022-01-25T00:00:00.csv'
    # file_path_2 = 'data/df_raw/btc_bull/4h/BTC-USD__4h__2021-09-06T00:00:00__2021-12-05T23:00:00.csv'
    # file_path_3 = 'data/df_raw/btc_bear/4h/BTC-USD__4h__2022-04-11T00:00:00__2022-10-30T23:00:00.csv'
    t = time()
    # run_backtest(file_path, ColoradoSnowPack, ColoradoSnowPack.OPTIMIZE_VALUES, 100000, False)
    print(time()-t)

    # for each_file in glob.glob('data/df_raw/btc_bull/4h/*.csv'):
    #     filepath = 'data/df_raw/btc_bull/4h/' + os.path.basename(each_file)
    #     stats = run_backtest(filepath, ColoradoSnowPack, ColoradoSnowPack.OPTIMIZE_VALUES, 100000, True)
    #     print(stats['Return [%]'])
