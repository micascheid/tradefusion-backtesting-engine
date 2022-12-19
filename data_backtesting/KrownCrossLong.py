"""
    - Static functions involve indicators unique to the strategy
    - init is where to add indicators for the strategy you want to implement
    - next function is the buy/sell logic for the strategy
"""
from os.path import exists
import backtesting
import pandas
import pandas_ta as ta
from backtesting import Strategy
import numpy as np
import pandas as pd
from talib import BBANDS


import multiprocessing as mp

mp.set_start_method('fork')
backtesting.set_bokeh_output(notebook=False)

def EMA(df, window):
    ema_series = ta.ema(df['Close'], length=window)
    return ema_series


def RSI(df, window):
    rsi_series = ta.rsi(df['Close'], window=window)
    return rsi_series


def BBWP(df):
    STD = 2.0
    LOOKBACK = 252
    bbands_series = ta.bbands(df['Close'], std=STD, mamode='sma', length=13)
    # bbwp_series = pd.DataFrame(index=bbands_series.index,columns=np.array(bbands_series['BBB_14_2']))
    BBW = bbands_series['BBB_13_2.0']
    bbwp_series = np.array([])
    bbwp = [0.0]*LOOKBACK

    #make sure the series is at least as long as 252
    if len(BBW) > LOOKBACK:
        for current_bbw in range (LOOKBACK, len(BBW)):
            count = 0
            for bbw in range(current_bbw-LOOKBACK, current_bbw):
                if BBW[bbw] < BBW[current_bbw]:
                    count += 1
            bbwp.append((count/LOOKBACK)*100)
        bbwp_series = np.array(bbwp)
    bbwp_series = pd.DataFrame(index=bbands_series.index, data=bbwp_series, columns=['BBWP'])

    #replace the bbwp_series value with the new calculated value

    # for value in bbwp_series:
    return bbwp_series


class KrownCross(Strategy):
    data_df_5_min = None
    ema_period_1 = 9
    ema_period_2 = 21
    ema_period_3 = 55
    separation = 1
    bbwp_entry = 40
    bbwp_exit = 90
    # rsi_period = 14
    # rsi_low = 30
    # rsi_high = 70
    take_profit_percent = 3
    stop_loss_percent = 1
    last_purchase_price = 0
    long_hold = 0
    i = 0
    bbwp_hit_exit = 0
    OPTIMIZE_VALUES = {'ema_period_1': range(5, 13, 1),
                       'ema_period_2': range(12, 30, 1),
                       'ema_period_3': range(45, 65, 2),
                       'bbwp_entry': range(0, 70, 10),
                       'bbwp_exit': range(70, 100, 5),
                       'separation': range(0, 4, 1)}

    def init(self):
        super().init()
        # Add indicators
        '''
            The krown cross method consists of the following indicators:
            EMA 9: Exponential Moving average 9 - short term trend ✔
            EMA 21: Exponential Moving average 21 - mid term trend ✔
            EMA 55: Exponential Moving average 55 - long term trend ✔
            RSI: Relative Strength Index - measuring the strength of a move ✔
            BBWP: Bollinger Band Width Percentage - Measures volatility ✔
        '''

        self.ema_1 = self.I(EMA, self.data.df, self.ema_period_1)
        self.ema_2 = self.I(EMA, self.data.df, self.ema_period_2)
        self.ema_3 = self.I(EMA, self.data.df, self.ema_period_3)
        # self.rsi = self.I(RSI, self.data.df, self.rsi_period)
        self.bbwp = self.I(BBWP, self.data.df)

    def next(self):
        super().init()
        '''
        Krown Cross Going Long Bias:
            Entry:
                - 9>21>55 emas
                - bbwp is positive sloping and < 50 (Optimize)
                - trading within 1% of 21 (Optimize)
            Stop Loss:
                - Close below 55
                - low < mid
            Exit:
                - BBWP > 90
                - low < mid
        '''

        prev_close = self.data.df.Close[-1]
        long_entry_signals = 0
        seperation_calc = abs((prev_close-self.ema_2[-1])/self.ema_2[-1])*100
        bbwp_slope = True if self.bbwp[0]/self.bbwp[-1] > 0 else False

        # Check 1: EMA Checks of 9>21>55
        if self.ema_1[-1] > self.ema_2[-1] > self.ema_3[-1]:
            long_entry_signals += 1

        # Check 2: Degree of separation check
        if seperation_calc <= self.separation:
            long_entry_signals += 1

        # Check 3: bbwp checks
        if self.bbwp[-1] < self.bbwp_entry:
            long_entry_signals += 1

        #Take profit
        if self.bbwp[-1] >= self.bbwp_exit:
            self.bbwp_hit_exit += 1
        price = self.data.df.Close[-1]
        is_take_profit = self.long_hold == 1 and self.bbwp_hit_exit == 2

        # Stop loss
        is_stop_loss = self.long_hold == 1 and self.ema_1[-1] < self.ema_2[-1] or prev_close <= self.ema_3[-1]

        # Long entry
        if self.long_hold == 0 and long_entry_signals == 3:
            self.buy()
            self.last_purchase_price = price
            self.long_hold = 1

        # Long exit
        elif self.long_hold == 1 and (is_take_profit or is_stop_loss):
            self.position.close()
            self.long_hold = 0
            self.last_purchase_price = 0
            self.bbwp_hit_exit = 0
