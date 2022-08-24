import datetime  # For datetime objects
import itertools
import os.path  # To manage paths
import sys  # To find out the script name (in argv[0])

# Import the backtrader platform
import time

import backtrader as bt
import backtrader.feeds as btfeed
import pandas as pd
from backtrader import date2num
import LoadData


# 自定义信号指标
class MySignal(bt.Indicator):
    lines = ('signal',)  # 声明 signal 线，交易信号放在 signal line 上
    params = dict(
        short_period=5,
        long_period=20)

    def __init__(self):
        self.s_ma = bt.ind.SMA(period=self.p.short_period)
        self.l_ma = bt.ind.SMA(period=self.p.long_period)
        # 短期均线上穿长期均线，取值为1；反之，短期均线下穿长期均线，取值为-1
        self.lines.signal = bt.ind.CrossOver(self.s_ma, self.l_ma)


if __name__ == '__main__':
    # 1. 准备数据
    loadDataService = LoadData.LoadBinanceDataService("./data", "BTCUSDT", "2022-05")
    data = loadDataService.load()
    # 2. 准备回测引擎
    # Create a cerebro entity
    cerebro = bt.Cerebro()
    # Add a strategy
    # cerebro.addstrategy(TestStrategy)
    cerebro.broker.setcommission(commission=0.001)
    cerebro.adddata(data)
    cerebro.addsizer(bt.sizers.FixedSize, stake=10)
    # Set our desired cash start
    cerebro.broker.setcash(100000.0)

    # 添加交易信号
    cerebro.add_signal(bt.SIGNAL_LONG, MySignal)
    # 回测时需要添加 PyFolio 分析
    cerebro.addanalyzer(bt.analyzers.PyFolio, _name='pyfolio')
    # Run over everything
    beginSec = time.time()
    # 3.  运行策略引擎
    cerebro.run()
    cerebro.plot()
    endSec = time.time()
    # 引擎运行后打期末资金
    print('组合期末资金: %.2f' % cerebro.broker.getvalue())
    print('耗时:', endSec - beginSec)
