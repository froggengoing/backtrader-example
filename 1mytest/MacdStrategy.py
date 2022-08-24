# MACD交易策略，光头光脚阳线，光头光脚阴线交易策略
# 测试资金100万，交易费用0.003
import pandas as pd
import matplotlib.pyplot as plt
import backtrader as bt
import datetime
import logging


logging.basicConfig(filename="trade.log", filemode='a',level=logging.INFO)

# 写策略
class MacdStrategy(bt.Strategy):
    # 记录函数
    def log(self, txt, dt=None):
        dt = dt or self.datas[0].datetime.date(0)
        logging.info('%s, %s' % (dt.isoformat(), txt))

    # 初始化数据,私有类
    def __init__(self):
        self.dataclose = self.datas[0].close
        self.dataopen = self.datas[0].open
        self.datalow = self.datas[0].low
        self.datahigh = self.datas[0].high
        self.ma5 = bt.indicators.MovingAverageSimple(self.dataclose, period=5)
        self.ma10 = bt.indicators.MovingAverageSimple(self.dataclose, period=10)
        self.ma20 = bt.indicators.MovingAverageSimple(self.dataclose, period=20)
        self.MACD = bt.indicators.MACD(self.datas[0])
        self.macd = self.MACD.macd
        self.signal = self.MACD.signal
        self.rsi = bt.indicators.RSI(self.datas[0])
        self.boll = bt.indicators.BollingerBands(self.datas[0])
        self.atr = bt.indicators.ATR(self.datas[0])
        self.order = None
        self.buyprice = None
        self.comm = None

    # 交易状态检测
    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            return
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log('买进的价格 %.2f,账户值；%.2f,交易费用：%.2f' % (
                order.executed.price, order.executed.value, order.executed.comm))
                self.buyprice = order.executed.price
                self.buycomm = order.executed.comm
            if order.issell():
                self.log('卖出的价格 %.2f,账户值；%.2f,交易费用：%.2f' % (
                order.executed.price, order.executed.value, order.executed.comm))
        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('交易取消,资金不足，交易拒接')

    # 交易完统计
    def notify_trade(self, trade):
        if not trade.isclosed:
            return
        self.log('利润：%.2f,总利润: %.2f' % (trade.pnl, trade.pnlcomm))

    # 交易函数
    def next(self):
        # 低位金叉买入
        if not self.position:
            if self.macd[-1] < self.signal[-1]:
                if self.macd[0] > self.signal[0]:
                    if self.macd[0] < 0:
                        self.buy(size=0.001)
                        self.log('MACD低位金叉买入价格:%.2f' % self.dataclose[0])
        # # 正常金叉买价
        # if self.macd[-1] < self.signal[-1]:
        #     if self.macd[0] > self.signal[0]:
        #         if self.macd[0] == 0:
        #             self.buy(size=500)
        #             self.log('MACD正常金叉买入价格:%.2f' % self.dataclose[0])
        # # 高位金叉买价，高位金叉有加速上升的作用
        # if self.macd[-1] < self.signal[-1]:
        #     if self.macd[0] > self.signal[0]:
        #         if self.macd[0] > 0:
        #             self.buy(size=500)
        #             self.log('MACD高位金叉买入价格:%.2f' % self.dataclose[0])
        # 高位死叉卖出

        if  self.position:
            if self.macd[-1] > self.signal[-1]:
                if self.macd[0] < self.signal[-1]:
                    if self.macd[0] >= 0:
                        self.sell(size=0.001)
                        self.log('MACD高位死叉卖出价格:%.2f' % self.dataclose[0])
        # # 低位死叉卖出，和死叉减创
        # if self.macd[-1] < self.signal[-1]:
        #     if self.macd[0] > self.signal[0]:
        #         if self.macd[0] < 0:
        #             self.buy(size=500)
        #             self.log('MACD低位金叉卖出价格:%.2f' % self.dataclose[0])
        # # 低位死叉，加速下降卖出
        # if self.macd[-1] > self.signal[-1]:
        #     if self.macd[0] < self.signal[-1]:
        #         if self.macd[0] < 0:
        #             self.sell(size=200)
        #             self.log('MACD低位死叉卖出价格:%.2f' % self.dataclose[0])
        # # macd下降趋势卖出
        # if (self.macd[-1] - self.signal[-1]) > (self.macd[0] - self.signal[0]):
        #     if self.signal[0] > self.macd[0]:
        #         self.buy(size=100)
        #         self.log('MACD下降趋势卖出价格:%.2f' % self.dataclose[0])
        # # macd上涨趋势买入
        # if (self.macd[-1] - self.signal[-1]) < (self.macd[0] - self.signal[0]):
        #     if self.signal[0] < self.macd[0]:
        #         self.buy(size=100)
        #         self.log('MACD上升趋势买入价格:%.2f' % self.dataclose[0])
        # # 光头光脚大阳线买入
        # if self.dataopen[0] == self.datalow[0] and self.dataclose[0] == self.datahigh[0] and self.dataclose[0] > \
        #         self.dataopen[0]:
        #     self.buy(size=500)
        #     self.log('光头光脚阳线买入，价格 %.2f' % self.dataclose[0])
        # # 光头光脚大阴线卖出
        # if self.dataopen[0] == self.datahigh[0] and self.dataclose[0] == self.datalow[0] and self.dataopen[0] > \
        #         self.dataclose[0]:
        #     self.sell(size=100)
        #     self.log('光头光脚大阴线卖出，价格 %.2f' % self.dataclose[0])
        # 底背离
        # 顶背离有空写
