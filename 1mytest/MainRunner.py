import time
from pprint import pprint

import backtrader as bt
import pandas as pd
import LoadData
import MacdStrategy
import matplotlib.pyplot as plt

if __name__ == "__main__":
    cerebro = bt.Cerebro()
    cerebro.broker.set_cash(10000)
    cerebro.broker.setcommission(0.001)
    # 添加数据
    loadDataService = LoadData.LoadBinanceDataService("./data", "BTCUSDT", "2022-05")
    data = loadDataService.load()
    cerebro.adddata(data)
    cerebro.addstrategy(MacdStrategy.MacdStrategy)
    # 分析
    cerebro.addanalyzer(bt.analyzers.SharpeRatio, _name='SharpeRatio')
    cerebro.addanalyzer(bt.analyzers.DrawDown, _name='DW')
    cerebro.addanalyzer(bt.analyzers.TradeAnalyzer, _name='Ta')
    cerebro.addanalyzer(bt.analyzers.Transactions, _name='transaction')
    beginSec = time.time()
    res = cerebro.run(runonce=False)
    stat = res[0]
    endSec = time.time()
    print('组合期末资金: %.2f' % cerebro.broker.getvalue())
    print('耗时:', endSec - beginSec)
    pprint('SR:', stat.analyzers.SharpeRatio.get_analysis())
    pprint('DW:', stat.analyzers.DW.get_analysis())
    pprint('ta:', stat.analyzers.Ta.get_analysis())
    pprint('transaction:', stat.analyzers.transaction.get_analysis())
    # cerebro.plot(style='candle')
    # plt.show()
