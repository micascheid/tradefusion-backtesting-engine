"""
DataPull Class takes the following: market, time_frame, start, end
"""


from data_pulling import NomicsAPI
import json
from datetime import datetime, timedelta
from data_pulling.IntervalLimits import IntervalLimits, interval_limit_dict, interval_limit_max_time_call, TimeFrames
import pandas as pd


KEY = NomicsAPI.API_KEY
U = "__"
MINUTELY = "m"
HOURLY = "h"
DAILY = "d"
JSON_RAW_DIR = "./data/json_raw/"
JSON_RAW_TO_DF = "./data/df_raw/"


def get_missing_data_set_times(json_data_list):
    results = json_data_list
    HOUR_ADD = timedelta(hours=1)
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


def export_json(file_name, raw_json):
    list_for_export = json.dumps(raw_json)
    file = open(JSON_RAW_DIR + file_name, 'w')
    file.write(list_for_export)
    file.close()


def export_df(file_name, raw_json):
    # json_obj = pd.json_normalize(raw_json)
    df = pd.DataFrame.from_records(raw_json)
    df = df.set_index('timestamp')
    df.to_csv(JSON_RAW_TO_DF + file_name + ".csv")


class DataPull:
    def __init__(self, time_frame_unit, time_frame_quantity, start, end, quote=None, base=None, market=None,
                 exchange=None):
        self.quote = quote
        self.base = base
        self.time_frame_unit = time_frame_unit
        self.time_frame_quantity = time_frame_quantity
        self.time_frame = time_frame_quantity + time_frame_unit
        self.start = start
        self.end = end
        self.deltas = self.configure_time_delta()
        self.nomics = NomicsAPI.API
        self.market = market
        self.exchange = exchange

    def api_call(self, start, end) -> list:
        if self.exchange is None:
            return self.nomics.Candles.get_candles(quote=self.quote, base=self.base, interval=self.time_frame,
                                               start=start.isoformat()+"Z", end=end.isoformat()+"Z")
        else:
            return self.nomics.Candles.get_candles(market=self.market, exchange=self.exchange,
                                                   interval=self.time_frame, start=start.isoformat()+"Z",
                                                   end=end.isoformat()+"Z")

    def data_conglomeration(self) -> list:
        start = self.start
        end = self.end
        main_list = []
        if self.time_frame_unit == "d":
            json_obj = self.api_call(start=start, end=self.end)
            [main_list.append(candle) for candle in json_obj]
        else:
            DELTA = self.deltas[0]
            DELTA_NEXT = self.deltas[1]
            time_diff = end - start
            conglomerate_tuple = self.to_conglomerate_or_not()
            conglomerate = conglomerate_tuple[0]
            total_candles = conglomerate_tuple[1]
            iteration = int(total_candles // interval_limit_dict[self.time_frame].value)
            last_candles = total_candles % interval_limit_dict[self.time_frame].value
            start_new = start
            if conglomerate:
                for i in range(iteration):
                    time_1 = start_new
                    time_2 = time_1 + DELTA
                    json_obj = self.api_call(start=time_1, end=time_2)
                    [main_list.append(candle) for candle in json_obj]
                    print(i, "|", time_1, time_2)
                    start_new = time_2 + DELTA_NEXT
            if last_candles != 0 or not conglomerate:
                print("last call", "|", start_new, self.end)
                json_obj = self.api_call(start=start_new, end=self.end)
                [main_list.append(candle) for candle in json_obj]
        return main_list

    def to_conglomerate_or_not(self) -> (bool, int):
        conglomerate = False
        time_diff = self.end - self.start
        total_candles = 0
        if self.time_frame_unit == "m":
            total_candles = (time_diff.total_seconds()/60)/float(self.time_frame_quantity)
        elif self.time_frame_unit == "h":
            total_candles = (time_diff.total_seconds()/3600)/float(self.time_frame_quantity)
        elif self.time_frame_unit == "d":
            return False

        if total_candles > interval_limit_dict[self.time_frame].value:
            conglomerate = True

        return conglomerate, total_candles


    def file_name_creator(self) -> str:
        # EX "/data/json_raw/in_sample/btcusd__1h__2012-01-01:00:00:00__2022-0101:00:00:00"
        if self.exchange is None:
            file_name = ""
            file_name = file_name + self.base + "-" + self.quote
            file_name = file_name + U + self.time_frame
            file_name = file_name + U + datetime.strftime(self.start, "%Y-%m-%dT%H:%M:%S")
            file_name = file_name + U + datetime.strftime(self.end, "%Y-%m-%dT%H:%M:%S")
            return file_name
        else:
            file_name = ""
            file_name = file_name + self.exchange + "-" + self.market
            file_name = file_name + U + self.time_frame
            file_name = file_name + U + datetime.strftime(self.start, "%Y-%m-%dT%H:%M:%S")
            file_name = file_name + U + datetime.strftime(self.end, "%Y-%m-%dT%H:%M:%S")
            return file_name

    def configure_time_delta(self) -> (timedelta, timedelta):
        max_time_call = interval_limit_max_time_call[self.time_frame]
        candle_session_size = int(self.time_frame_quantity)
        DELTA = max_time_call-candle_session_size

        if self.time_frame_unit == MINUTELY:
            return timedelta(minutes=DELTA), timedelta(minutes=candle_session_size)
        if self.time_frame_unit == HOURLY:
            return timedelta(hours=DELTA), timedelta(hours=candle_session_size)
        else:
            return timedelta(days=9999), timedelta(days=1)

    def pull_and_export(self):
        file_export = self.file_name_creator()
        raw_json = self.data_conglomeration()
        export_json(file_export, raw_json)
        export_df(file_export, raw_json)




