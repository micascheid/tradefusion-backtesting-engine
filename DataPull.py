"""
DataPull Class takes the following: market, time_frame, start, end
"""
import nomics

import NomicsAPI
import json
from datetime import datetime, timedelta
from IntervalLimits import IntervalLimits, interval_limit_dict, TimeFrames

KEY = NomicsAPI.API_KEY
U = "__"
MINUTELY = "m"
HOURLY = "h"
DAILY = "d"
JSON_RAW_DIR = "./data/json_raw/"


class DataPull:
    def __init__(self, quote, base, time_frame_unit, time_frame_quantity, start, end):
        self.quote = quote
        self.base = base
        self.time_frame_unit = time_frame_unit
        self.time_frame_quantity = time_frame_quantity
        self.time_frame = time_frame_quantity + time_frame_unit
        self.start = start
        self.end = end
        self.deltas = self.configure_time_delta()
        self.nomics = NomicsAPI.API

    def api_call(self, start, end) -> list:
        return self.nomics.Candles.get_candles(quote=self.quote, base=self.base, interval=self.time_frame,
                                               start=start.isoformat()+"Z", end=end.isoformat()+"Z")

    def data_conglomeration(self) -> list:
        start = self.start
        end = self.end
        main_list = []
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
        if last_candles != 0:
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
            total_candles = (time_diff.total_seconds()/86400)/float(self.time_frame_quantity)

        if total_candles > interval_limit_dict[self.time_frame].value:
            conglomerate = True

        return conglomerate, total_candles


    def file_name_creator(self) -> str:
        # EX "/data/json_raw/in_sample/btcusd__1h__2012-01-01:00:00:00__2022-0101:00:00:00"
        file_name = ""
        file_name = file_name + self.base + "-" + self.quote
        file_name = file_name + U + self.time_frame
        file_name = file_name + U + datetime.strftime(self.start, "%Y-%m-%dT%H:%M:%S")
        file_name = file_name + U + datetime.strftime(self.end, "%Y-%m-%dT%H:%M:%S")
        return file_name

    def configure_time_delta(self) -> (timedelta, timedelta):
        if self.time_frame_unit == MINUTELY:
            return (timedelta(minutes=(interval_limit_dict[self.time_frame].value * int(self.time_frame_quantity)) - 1),
                    timedelta(minutes=int(self.time_frame_quantity)))
        if self.time_frame_unit == HOURLY:
            return (timedelta(hours=(interval_limit_dict[self.time_frame].value * int(self.time_frame_quantity)) - 1),
                    timedelta(hours=int(self.time_frame_quantity)))
        if self.time_frame_unit == DAILY:
            if self.time_frame_unit == HOURLY:
                return (timedelta(hours=interval_limit_dict[self.time_frame].value - 1),
                        timedelta(hours=int(self.time_frame_quantity)))

    def pull_and_export(self):
        file_export = self.file_name_creator()
        raw_data = self.data_conglomeration()
        print(raw_data)
        list_for_export = json.dumps(raw_data)
        file = open(JSON_RAW_DIR+file_export, 'w')
        file.write(list_for_export)
        file.close()




