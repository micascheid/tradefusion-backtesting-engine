from datetime import datetime
from data_pulling.DataPull import DataPull
if __name__=='__main__':

    #Bull pulls
    # start = datetime(year=2012, month=2, day=20, hour=0, minute=0, second=0)
    # end = datetime(year=2012, month=3, day=25, hour=23, minute=0, second=0)
    #
    # start1 = datetime(year=2012, month=6, day=11, hour=0, minute=0, second=0)
    # end1 = datetime(year=2013, month=6, day=30, hour=23, minute=0, second=0)
    #
    # start2 = datetime(year=2013, month=6, day=10, hour=0, minute=0, second=0)
    # end2 = datetime(year=2014, month=2, day=23, hour=23, minute=0, second=0)
    #
    # start3 = datetime(year=2014, month=6, day=23, hour=0, minute=0, second=0)
    # end3 = datetime(year=2014, month=8, day=17, hour=23, minute=0, second=0)
    #
    # start4 = datetime(year=2016, month=1, day=18, hour=0, minute=0, second=0)
    # end4 = datetime(year=2018, month=2, day=4, hour=23, minute=0, second=0)
    #
    # start5 = datetime(year=2019, month=3, day=18, hour=0, minute=0, second=0)
    # end5 = datetime(year=2019, month=9, day=1, hour=23, minute=0, second=0)
    #
    # start6 = datetime(year=2020, month=1, day=27, hour=0, minute=0, second=0)
    # end6 = datetime(year=2020, month=3, day=8, hour=23, minute=0, second=0)
    #
    # start7 = datetime(year=2020, month=6, day=1, hour=0, minute=0, second=0)
    # end7 = datetime(year=2021, month=5, day=2, hour=23, minute=0, second=0)
    #
    # start8 = datetime(year=2021, month=9, day=6, hour=0, minute=0, second=0)
    # end8 = datetime(year=2021, month=12, day=5, hour=23, minute=0, second=0)
    #
    # start9 = datetime(year=2020, month=6, day=1, hour=0, minute=0, second=0)
    # end9 = datetime(year=2021, month=5, day=2, hour=23, minute=0, second=0)
    #
    # bull_pulls_start = [start, start1, start2, start3, start4, start5, start6, start7, start8, start9]
    # bull_pulls_end = [end, end1, end2, end3, end4, end5, end6, end7, end8, end9]
    #
    # for i in range(len(bull_pulls_start)):
    #     dp = DataPull(quote="USD", base="BTC", time_frame_unit="h", time_frame_quantity="1", start=bull_pulls_start[i],
    #                   end=bull_pulls_end[i])
    #     dp.pull_and_export()


    #Bear Pulls
    start = datetime(year=2011, month=9, day=29, hour=0, minute=0, second=0)
    end = datetime(year=2011, month=12, day=25, hour=23, minute=0, second=0)

    # start1 = datetime(year=2014, month=9, day=15, hour=0, minute=0, second=0)
    # end1 = datetime(year=2015, month=6, day=21, hour=23, minute=0, second=0)
    #
    # start2 = datetime(year=2018, month=3, day=12, hour=0, minute=0, second=0)
    # end2 = datetime(year=2018, month=7, day=29, hour=23, minute=0, second=0)
    #
    # start3 = datetime(year=2018, month=9, day=10, hour=0, minute=0, second=0)
    # end3 = datetime(year=2019, month=3, day=17, hour=23, minute=0, second=0)
    #
    # start4 = datetime(year=2019, month=11, day=18, hour=0, minute=0, second=0)
    # end4 = datetime(year=2020, month=1, day=12, hour=23, minute=0, second=0)
    #
    # start5 = datetime(year=2022, month=1, day=3, hour=0, minute=0, second=0)
    # end5 = datetime(year=2022, month=3, day=27, hour=23, minute=0, second=0)
    #
    # start6 = datetime(year=2022, month=4, day=11, hour=0, minute=0, second=0)
    # end6 = datetime(year=2022, month=10, day=30, hour=23, minute=0, second=0)

    bull_pulls_start = [start]
    bull_pulls_end = [end]
    for i in range(len(bull_pulls_start)):
        dp = DataPull(quote="USD", base="BTC", time_frame_unit="h", time_frame_quantity="1", start=bull_pulls_start[i],
                      end=bull_pulls_end[i])
        dp.pull_and_export()

    # Limbo
    start = datetime(year=2011, month=12, day=26, hour=0, minute=0, second=0)
    end = datetime(year=2012, month=2, day=19, hour=23, minute=0, second=0)

    # start1 = datetime(year=2012, month=3, day=26, hour=0, minute=0, second=0)
    # end1 = datetime(year=2012, month=6, day=10, hour=23, minute=0, second=0)
    #
    # start2 = datetime(year=2013, month=7, day=1, hour=0, minute=0, second=0)
    # end2 = datetime(year=2013, month=10, day=6, hour=23, minute=0, second=0)
    #
    # start3 = datetime(year=2014, month=2, day=24, hour=0, minute=0, second=0)
    # end3 = datetime(year=2014, month=6, day=22, hour=23, minute=0, second=0)
    #
    # start4 = datetime(year=2014, month=8, day=18, hour=0, minute=0, second=0)
    # end4 = datetime(year=2014, month=9, day=14, hour=23, minute=0, second=0)
    #
    # start5 = datetime(year=2015, month=6, day=22, hour=0, minute=0, second=0)
    # end5 = datetime(year=2016, month=1, day=17, hour=23, minute=0, second=0)
    #
    # start6 = datetime(year=2018, month=2, day=5, hour=0, minute=0, second=0)
    # end6 = datetime(year=2018, month=3, day=18, hour=23, minute=0, second=0)
    #
    # start7 = datetime(year=2018, month=7, day=30, hour=0, minute=0, second=0)
    # end7 = datetime(year=2018, month=9, day=9, hour=23, minute=0, second=0)
    #
    # start8 = datetime(year=2019, month=9, day=2, hour=0, minute=0, second=0)
    # end8 = datetime(year=2019, month=11, day=17, hour=23, minute=0, second=0)
    #
    # start9 = datetime(year=2020, month=1, day=13, hour=0, minute=0, second=0)
    # end9 = datetime(year=2020, month=1, day=26, hour=23, minute=0, second=0)
    #
    # start10 = datetime(year=2020, month=3, day=9, hour=0, minute=0, second=0)
    # end10 = datetime(year=2020, month=5, day=31, hour=23, minute=0, second=0)
    #
    # start11 = datetime(year=2021, month=5, day=3, hour=0, minute=0, second=0)
    # end11 = datetime(year=2021, month=9, day=5, hour=23, minute=0, second=0)
    #
    # start12 = datetime(year=2021, month=12, day=6, hour=0, minute=0, second=0)
    # end12 = datetime(year=2022, month=1, day=2, hour=23, minute=0, second=0)
    #
    # start13 = datetime(year=2022, month=3, day=28, hour=0, minute=0, second=0)
    # end13 = datetime(year=2022, month=5, day=10, hour=23, minute=0, second=0)
    #
    # start14 = datetime(year=2022, month=10, day=31, hour=0, minute=0, second=0)
    # end14 = datetime(year=2022, month=11, day=13, hour=23, minute=0, second=0)

    bull_pulls_start = [start]
    bull_pulls_end = [end]
    for i in range(len(bull_pulls_start)):
        dp = DataPull(quote="USD", base="BTC", time_frame_unit="h", time_frame_quantity="1", start=bull_pulls_start[i],
                      end=bull_pulls_end[i])
        dp.pull_and_export()