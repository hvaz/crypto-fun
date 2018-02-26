"""
Candles consist of a list of candles obeying to the following format:

[
  {
    "open_tstamp": int,
    "close_tstamp": int,
    "open_price": float,
    "close_price": float,
    "min_price": float,
    "max_price": float,
    "volume": float,
    "volumeQuote": float
  },
  {
    "open_tstamp": int,
    "close_tstamp": int,
    "open_price": float,
    "close_price": float,
    "min_price": float,
    "max_price": float,
    "volume": float,
    "volumeQuote": float
  }, 
  ...
]

OBS: Data is returned in ascending order. Oldest first, newest last.
"""

class Candles(object):

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
