"""
Candles consist of a list of candles obeying to the following format:

[
  {
    "timestamp": "2017-10-20T20:00:00.000Z",
    "open": "0.050459",
    "close": "0.050087",
    "min": "0.050000",
    "max": "0.050511",
    "volume": "1326.628",
    "volumeQuote": "66.555987736"
  },
  {
    "timestamp": "2017-10-20T20:30:00.000Z",
    "open": "0.050108",
    "close": "0.050139",
    "min": "0.050068",
    "max": "0.050223",
    "volume": "87.515",
    "volumeQuote": "4.386062831"
  }
]

OBS: Data is returned in ascending order. Oldest first, newest last.
"""

class candles(object):

    def __init__(self, interval, data):

        self.interval = interval
        self.data = data

    # assumes data is in ascending time
    def get_ema(self, factor, at):

        candlelist = self.data
        if at >= len(candlelist) or at < 0:
            return -1

        period = 1.0 / factor
        start = int(at - period)
        current_ema = 0

        for i in range(max(start, 0), at + 1):

            close = candlelist[i]['close']
            current_ema = close * factor + current_ema * (1 - factor)

        return current_ema

    # assumes data is in ascending time
    def get_ema_list(self, factor):

        candlelist = self.data
        ema_list = []
        current_ema = 0

        for candle in candlelist:

            close = float(candlelist['close'])
            current_ema = close * factor + current_ema * (1 - factor)
            ema_list.append(current_ema)

        return ema_list


            



