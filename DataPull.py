"""
DataPull Class takes the following: market, time_frame, start, end
"""
import NomicsAPI

KEY = NomicsAPI.API_KEY


class DataPull:
    def __init__(self, market, time_frame, start, end, sample_type):
        self.market = market
        self.time_frame = time_frame
        self.start = start
        self.end = end

    def file_name_creator(self) -> str:


        return self.market
