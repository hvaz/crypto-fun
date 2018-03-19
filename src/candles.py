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
        current_ema = - 1

        for candle in self.candle_list:
            close = float(candle['close_price'])
            
            if current_ema == -1:
                current_ema = close
            else:
                current_ema = close * factor + current_ema * (1 - factor)
           
            ema_list.append(current_ema)

        return ema_list


    def get_vidya_list(self, factor):
        vidya_list = []
        current_vidya = -1

        for candle in self.candle_list:
            close = float(candle['close_price'])
            open = float(candle['open_price'])
            cmo = (open - close) / (open + close)
            current_factor = abs(cmo)*factor

            if current_vidya == -1:
                current_vidya = close
            else:
                current_vidya = close * current_factor + current_vidya * (1-current_factor)

            vidya_list.append(current_vidya)
        
        return vidya_list
