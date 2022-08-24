import os
import pandas as pd
import backtrader as bt


class LoadBinanceDataService:

    def __init__(self, path, pair, begin, end=None):
        self.path = path
        self.pair = pair
        self.begin = begin
        self.end = end

    def load(self):
        allCsvList = os.listdir(self.path)
        allData = None
        for singleCsv in allCsvList:
            path = os.path.join(self.path, singleCsv)
            dtStr = singleCsv[len(self.pair) + 4:-4]
            if dtStr < self.begin:
                continue
            if self.end is not None and dtStr > self.end:
                continue
            print("loading:", singleCsv)
            singleData = pd.read_csv(path,
                                     names=["datetime", "open", "high", "low", "close", "volume", "ctime", "qv", "num",
                                            "tbv",
                                            "tqv",
                                            "ig"],
                                     header=None)
            if allData is None:
                allData = singleData
            else:
                allData = pd.concat([allData, singleData])
        allData["datetime"] = pd.to_datetime(allData['datetime'], unit='ms')
        # btc['datetime'] = btc['datetime'].map(lambda x: x.strftime('%Y-%m-%d %H:%M:%S'))
        data = bt.feeds.PandasData(
            dataname=allData,
            datetime=0,
            openinterest=-1,
            # format='%Y-%m-%d %H:%M:%S.%f'
        )
        return data


if __name__ == '__main__':
    service = LoadBinanceDataService("./data", "BTCUSDT", "2021-01")
    data = service.load()
    print(data)
