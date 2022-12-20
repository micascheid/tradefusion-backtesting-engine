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

# mp.set_start_method('fork')
backtesting.set_bokeh_output(notebook=False)


def EMA(df, window):
    ema_series = ta.ema(df['Close'], length=window)
    return ema_series


def RSI(df, window):
    rsi_series = ta.rsi(df['Close'], window=window)
    return rsi_series


def PPVI_BAND(df, period, high_low,) -> pd.DataFrame:
    PERIOD = period
    price_series = df[high_low]
    rolling_price_sma = ta.sma(df['Close'], length=PERIOD)

    #calculate rolling 3 period std off the highs
    rolling_std = df[high_low].rolling(PERIOD).std()
    #calculate rolling sma 3 off std highs series
    rolling_ppvi_vol = ta.sma(rolling_std, length=PERIOD) * 2
    #calculate bands
    if high_low == 'High':
        band = rolling_price_sma + rolling_ppvi_vol
    else:
        band = rolling_price_sma - rolling_ppvi_vol
    column_name = 'SMA_'+str(PERIOD)
    final =pd.DataFrame(index=df.index, data=band, columns=[column_name])
    return final


class ColoradoSnowPack(Strategy):
    ppvi_period = 3
    stop_loss_percent = 1
    take_profit_percent = 3
    last_purchase_price = 0
    long_hold = 0
    short_hold = 0
    i = 0
    OPTIMIZE_VALUES = {'ppvi_period': range(3, 10, 1),
                       'stop_loss_percent': range(1, 5, 1),
                       'take_profit_percent': range(1, 10, 1)}
    def init(self):
        super().init()
        self.ppvi_high_band = self.I(PPVI_BAND, self.data.df, self.ppvi_period, 'High')
        self.ppvi_low_band = self.I(PPVI_BAND, self.data.df, self.ppvi_period, 'Low')

    def next(self):
        super().init()
        '''
            Long Entry: When price closes below lower band you go long
            Short Entry: When price closes above upper band you go short
            
            Long Exit: When price closes above upper band or hit exit profit
            Short Exit: When price closes below lower band or hit exit profit
        '''
        price = self.data.df.Close[-1]
        long_entry_signals = 0
        short_entry_signals = 0
        #Long Checks
        if price < self.ppvi_low_band[-1]:
            long_entry_signals += 1

        #Short Checks
        if price > self.ppvi_high_band[-1]:
            short_entry_signals += 1

        #Take Profit
        is_take_profit = False
        if self.long_hold == 1:
            is_take_profit = price > self.ppvi_high_band[-1] or price > self.last_purchase_price * (
                    1 + (self.take_profit_percent / 100))
        if self.short_hold == 1:
            is_take_profit = price < self.ppvi_low_band[-1] or price < self.last_purchase_price * (1 - (
                    self.take_profit_percent/100))

        #Stop Loss
        is_stop_loss = False
        if self.long_hold == 1:
            is_stop_loss = price < self.last_purchase_price * (1-(self.stop_loss_percent / 100))

        if self.short_hold == 1:
            is_stop_loss = price > self.last_purchase_price * (1 + (self.stop_loss_percent/100))


        #Long Entry and Short Check Exit
        if self.long_hold == 0 and long_entry_signals >= 1:
            if self.short_hold == 1:
                self.position.close()
                self.short_hold = 0
            self.buy()
            self.last_purchase_price = price
            self.long_hold = 1
        # Long Exit as stop loss or take profit
        elif self.long_hold == 1 and (is_take_profit or is_stop_loss):
            self.position.close()
            self.long_hold = 0
            self.last_purchase_price = 0

        # Short Entry and Long Exit Check
        if self.short_hold == 0 and short_entry_signals >= 1:
            if self.long_hold == 1:
                self.position.close()
                self.long_hold = 0
            self.sell()
            self.last_purchase_price = price
            self.short_hold = 1
        # Short Exit as stop loss or take profit
        elif self.short_hold == 1 and (is_take_profit or is_stop_loss):
            self.position.close()
            self.short_hold = 0
            self.last_purchase_price = 0

