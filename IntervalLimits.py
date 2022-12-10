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

interval_limit_max_time_call = {
    "1m": IntervalLimits.ONE_MINUTE.value * 60,
    "5m": IntervalLimits.FIVE_MINUTE.value * 5,
    "30m": IntervalLimits.THIRTY_MINUTE.value * 30,
    "1h": IntervalLimits.ONE_HOUR.value * 1,
    "4h": IntervalLimits.FOUR_HOUR.value * 4,
    "1d": IntervalLimits.ONE_DAY.value
}
interval_limit_dict = {
    "1m": IntervalLimits.ONE_MINUTE,
    "5m": IntervalLimits.FIVE_MINUTE,
    "30m": IntervalLimits.THIRTY_MINUTE,
    "1h": IntervalLimits.ONE_HOUR,
    "4h": IntervalLimits.FOUR_HOUR,
    "1d": IntervalLimits.ONE_DAY,
}


class TimeFrames(Enum):
    ONE_MINUTE = "1m"
    FIVE_MINUTE = "5m"
    THIRTY_MINUTE = "30m"
    ONE_HOUR = "1h"
    FOUR_HOUR = "4h"
    SIX_HOUR = "6h"
    TWELVE_HOUR = "12h"
    ONE_DAY = "1d"





