class candles(object):

    def __init__(self, factor, unit):

        self.factor = factor
        self.unit = unit


    def get_ema(self, factor, at):
        candlelist = self.data
        if at >= len(candlelist) or at < 0:
            return -1
        period = 1.0/factor
        start = int(at - period)
        current_ema = 0
        for i in range(max(start,0), at+1):
            close = candlelist[i]['close']
            current_ema = close*factor+current_ema*(1-factor)
        return current_ema

    def get_ema_list(self, factor):
        candlelist = self.data
        ema_list = []
        current_ema = 0
        for candle in candlelist:
            close = float(candlelist['close'])
            current_ema = close*factor + current_ema*(1-factor)
            ema_list.append(current_ema)
        return ema_list
