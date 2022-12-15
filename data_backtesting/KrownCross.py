import backtesting
import pandas_ta as ta
from backtesting import Strategy, Backtest
import numpy as np
import pandas as pd
import datetime
import matplotlib
import numpy as np



import os
import time
from os.path import exists

import backtesting
import pandas
import pandas_ta as ta
from backtesting import Strategy, Backtest
import numpy as np
import pandas as pd
import datetime
import matplotlib
# import yfinance as yf


import multiprocessing as mp

mp.set_start_method('fork')
backtesting.set_bokeh_output(notebook=False)


def EMA(df, window):
    ema_series = ta.ema(df['Close'], length=window)
    return ema_series


def RSI(df, window):
    rsi_series = ta.rsi(df['Close'], window=window)
    return rsi_series

def BBWP(df, window):
    STD = 2.0
    LOOKBACK = 252
    bbands_series = ta.bbands(df['Close'], std=STD, mamode='sma', length=13, window=window)
    # bbwp_series = pd.DataFrame(index=bbands_series.index,columns=np.array(bbands_series['BBB_14_2']))
    BBW = bbands_series['BBB_13_2.0']
    bbwp_series = np.array([])
    bbwp = [0]*LOOKBACK

    #make sure the series is at least as long as 252
    if len(BBW) > LOOKBACK:
        for current_bbw in range (LOOKBACK, len(BBW)):
            count = 0
            for bbw in range(current_bbw-LOOKBACK, current_bbw):
                if BBW[bbw] < BBW[current_bbw]:
                    count+=1
            bbwp.append((count/LOOKBACK)*100)
        bbwp_series = np.array(bbwp)
    bbwp_series = pd.DataFrame(index=bbands_series.index, data=bbwp_series, columns=['BBWP'])

    #replace the bbwp_series value with the new calculated value

    # for value in bbwp_series:
    return bbwp_series



def build_data_file_path(symbol):
    file_name = f"{symbol}.txt"
    file_path = os.path.join(symbol, file_name)
    return file_path


# def reformat_time(x):
#     time_str = str(x)
#     time_str = time_str.zfill(4)
#     hour = time_str[0:2]
#     minute = time_str[2:4]
#     return f" {hour}:{minute}"


def load_data_file(path):
    file_path = path
    if not exists(file_path):
        print(f"Error loading file {file_path}")
        return None
    #  Load data file
    df1 = pd.read_csv(file_path)
    if df1 is None or len(df1) == 0:
        print(f"Empty file: {file_path}")
        return None
    df1 = df1.rename(columns={"open": "Open", "close": "Close", "low": "Low", "high": "High", "volume": "Volume"})
    df1['timestamp'] = pd.to_datetime(df1['Date'])
    df1 = df1.set_index('Date')

    return df1


class KrownCross(Strategy):
    data_df_5_min = None
    ema_period_1 = 9
    ema_period_2 = 21
    ema_period_3 = 55
    rsi_period = 14
    rsi_low = 30
    rsi_high = 70
    take_profit_percent = 3
    stop_loss_percent = 1
    last_purchase_price = 0
    long_hold = 0
    i = 0

    def init(self):
        super().init()
        # Add indicators
        """
            The krown cross method consists of the following indicators:
            EMA 9: Exponential Moving average 9 - short term trend
            EMA 21: Exponential Moving average 21 - mid term trend
            EMA 55: Exponential Moving average 55 - long term trend
            RSI:Relative Strength Index - measuring the strength of a move
            BBWP: Bollinger Band Width Percentage - Measures volatility
            BMSB: Boolean which says weather or not data exists under or below Bitcoins 20week MA
        """
        self.ema_1 = self.I(EMA, self.data.df, self.ema_period_1)
        self.ema_2 = self.I(EMA, self.data.df, self.ema_period_2)
        self.ema_3 = self.I(EMA, self.data.df, self.ema_period_3)
        self.rsi = self.I(RSI, self.data.df, self.rsi_period)
        self.bbwp = self.I(BBWP, self.data.df, 0)


    def next(self):
        super().init()
        long_entry_signals = 0
        #  EMA checks
        if self.ema_1[-1] > self.ema_2[-1] and self.ema_1[-2] <= self.ema_2[-2]:
            long_entry_signals += 1
        #  RSI checks
        rsi_lb = self.rsi[-10:]
        for i in range(1, len(rsi_lb)):
            if rsi_lb[i] > self.rsi_low and rsi_lb[i - 1] <= self.rsi_low:
                long_entry_signals += 1
                break
        #  Take profit
        price = self.data.df.Close[-1]
        is_take_profit = self.long_hold == 1 and price > self.last_purchase_price * (
                    1 + (self.take_profit_percent / 100))
        #  Stop Loss
        is_stop_loss = self.long_hold == 1 and price < self.last_purchase_price * (1 - (self.stop_loss_percent / 100))
        #  Long entry
        if self.long_hold == 0 and long_entry_signals >= 2:
            #  Buy
            self.buy()
            self.last_purchase_price = price
            self.long_hold = 1
        # Long exit - stop loss or take profit
        elif self.long_hold == 1 and (is_take_profit or is_stop_loss):
            # Close any existing long trades, and sell the asset
            self.position.close()
            self.long_hold = 0
            self.last_purchase_price = 0




