import datetime  # For datetime objects
import itertools
import os.path  # To manage paths
import sys  # To find out the script name (in argv[0])

# Import the backtrader platform
import backtrader as bt
import backtrader.feeds as btfeed
import pandas as pd
from backtrader import date2num

class BinanceCSVData(btfeed.GenericCSVData):
    # Open time	Open	High	Low	Close	Volume	Close time	Quote asset volume	Number of trades	Taker buy base asset volume	Taker buy quote asset volume	Ignore
    params = (
        ('fromdate', datetime.datetime(2017, 12, 1)),
        ('todate', datetime.datetime(2017, 12, 31)),
        ('nullvalue', 0.0),
        ('dtformat', 1),
        # ('tmformat', ('%H.%M.%S')),
        # ('format', ('%Y-%m-%d %H:%M:%S.%f')),
        ('timeframe', bt.TimeFrame.Minutes),
        ('date_parser', lambda x: datetime.utcfromtimestamp(int(x) / 1000)),

        ('datetime', 0),
        ('open', 1),
        ('high', 2),
        ('low', 3),
        ('close', 4),
        ('volume', 5),
        ('ctime', 6),
        ('qv', 7),
        ('count', 8),
        ('tbv', 9),
        ('tqv', 10),
        ('ig', 11),
        ('openinterest', -1)
    )

