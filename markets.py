intervals = ['1m', '3m', '5m', '15m', '30m', \
             '1h', '2h', '4h', '6h', '8h', '12h', \
             '1d', '3d', \
             '1w',
             '1M']

class market(object):

    def __init__(self, name):

        self.name = name
        self.candles = {i:None for i in intervals}

    def get_candles(self, interval):

        if (interval not in intervals):

            raise "Invalid unit for candles!"
            return

        self.candles[interval] = candles(interval)

