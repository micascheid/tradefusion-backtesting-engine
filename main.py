import NomicsAPI
from datetime import datetime
from DataPull import DataPull
from IntervalLimits import IntervalLimits, interval_limit_dict
import pandas as pd
"""
Plan for Dec7th
Work part 1 of my backtesting engine requirments list: This revolves around data pulling from nomics

Create a Data_pull class with the following parameters: Pair, timeframe,
"""

if __name__ == "__main__":

    start = datetime(year=2022, month=6, day=1, hour=0, minute=0, second=0)
    end = datetime(year=2022, month=12, day=7, hour=1, minute=0, second=0)
    dp1 = DataPull(quote="USD", base="BTC", time_frame_unit="h", time_frame_quantity="4", start=start, end=end)
    dp1.pull_and_export()
