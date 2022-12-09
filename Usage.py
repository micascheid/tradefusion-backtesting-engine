import json
from datetime import datetime
import NomicsAPI
import urllib.request


class Usage:
    def __init__(self, API_KEY):
        self.API_KEY = API_KEY

    def get_total_usage(self):
        month = datetime.now().month
        month_name = datetime.strftime(datetime.strptime(str(month), "%m"),"%B")
        year = datetime.now().year
        print("Grabbing usage starting from the first of the month for {}...".format(month_name))

        start = datetime(year=year, month=month, day=1).isoformat()+"Z"
        print(self.API_KEY)
        url = "https://api.nomics.com/v1/meta/usage?key="+self.API_KEY+"&start="+start
        usage = urllib.request.urlopen(url).read()
        json_list = json.loads(usage)
        total = sum([request['requests'] for request in json_list])
        print("Total request starting from:", start, "is", total)


if __name__ == '__main__':
    Usage(NomicsAPI.API.key).get_total_usage()
