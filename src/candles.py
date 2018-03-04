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
        self.candle_list = data


    # assumes data is in ascending time
    def get_ema_list(self, factor):
        ema_list = []
        current_ema = 0

        for candle in self.candle_list:
            close = float(candle['close_price'])
            current_ema = close * factor + current_ema * (1 - factor)
            ema_list.append(current_ema)

        return ema_list
