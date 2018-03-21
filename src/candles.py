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

NUM_CANDLES = 1000

class Candles(object):
    def __init__(self, interval, data):
        self.interval = interval
        self.candle_list = data


    def get_avg(self, start=-1, end=-1):
        start = 0 if start == -1 else start
        end = len(self.candle_list) if end == -1 else end
        
        n = 0
        tot = 0.0

        for i in range(start, end):
            close_price = self.candle_list[i]['close_price']
            tot += close_price
            n += 1
            
        return (tot / n)


    def get_std(self, start=-1, end=-1):
        start = 0 if start == -1 else start
        end = len(self.candle_list) if end == -1 else end
        
        n = 0
        tot = 0.0
        avg = self.get_avg(start, end)

        for i in range(start, end):
            close_price = self.candle_list[i]['close_price']
            tot += (close_price - avg)**2
            n += 1

        return (tot / n)**0.5


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
            close_price = float(candle['close_price'])
            open_price = float(candle['open_price'])
            cmo = (open_price - close_price) / (open_price + close_price)
            current_factor = abs(cmo) * factor

            if current_vidya == -1:
                current_vidya = close_price
            else:
                current_vidya = close_price * current_factor \
                                + current_vidya * (1 - current_factor)

            vidya_list.append(current_vidya)
        
        return vidya_list
