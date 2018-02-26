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

class Candles(object):

    def __init__(self, interval, data):

        self.interval = interval
        self.data = data


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


    def get_ema_list(self, factor):

        candlelist = self.data
        ema_list = []
        current_ema = 0

        for candle in candlelist:

            close = float(candlelist['close'])
            current_ema = close * factor + current_ema * (1 - factor)
            ema_list.append(current_ema)

        return ema_list


    def test_ema_model(self, start, end, short_factor, long_factor, fee, threshold):

        candle_list = self.data
        short_ema_list = self.get_ema_list(short_factor)
        long_ema_list = self.get_ema_list(long_factor)

        # the market is c2/c1
        total_c1 = 1.0
        total_c2 = 0.0
        side = 'c1'
        
        for i in range(start, end):

            if (short_emma_list[i] > long_emma_list[i] + threshold) and side == 'c1':
                total_c1 = 0
                total_c2 = (1-fee)*total_c1*candle_list[i]['close']
                side = 'c2'

            if (short_emma_list[i] < (long_emma_list[i] - threshold) and side == 'c2'):
                total_c1 = (1 - fee) * total_c2 / candle_list[i]['close']
                total_c2 = 0
                side = 'c1'
        
        if side == 'c2':
            total_c1 = (1 - fee) * total_c2 / candle_list[end - 1]['close']
            total_c2 = 0

        profits = total_c1 - 1.0
        return profits
            



