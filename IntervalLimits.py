"""
Name: IntervalLimits
Description: To serve as a set of constants relating to the intervals and limits defined by the Nomics API
interval	limit
1d	        no limit
4h	        120 days
1h	        30 days
30m	        14 days
5m	        3 days
1m	        1 day

The value set for the interval is the amount of candles that can be request for a given limit period
    EX| Interval: 5min, limit:3 days. They're 12 5min candles in an hour at 72 hours(3 days). Hence 12*24 = 864
"""

from enum import Enum


class IntervalLimits(Enum):
    ONE_MINUTE = 1440
    FIVE_MINUTE = 864
    THIRTY_MINUTE = 672
    ONE_HOUR = 720
    FOUR_HOUR = 720
    ONE_DAY = None



