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




    def test_ema_model(candles_object, start, end, short_factor, long_factor, threshold):

        fee = self.fee
        candle_list = candles_object.data
        short_ema_list = candles_object.get_ema_list(short_factor)
        long_ema_list = candles_object.get_ema_list(long_factor)

        # the market is c2/c1                                                                    
        total_c1 = 1.0
        total_c2 = 0.0
        side = 'c1'

        for i in range(start, end):

            if (short_emma_list[i] > long_emma_list[i] + threshold) and side == 'c1':
                total_c1 = 0
                total_c2 = (1-fee)*total_c1*candle_list[i]['close']
                side = 'c2'

            if (short_emma_list[i] < long_emma_list[i] - threshold) and side == 'c2'):
                total_c1 = (1 - fee) * total_c2 / candle_list[i]['close']
                total_c2 = 0
                side = 'c1'

        if side == 'c2':
            total_c1 = (1 - fee) * total_c2 / candle_list[end - 1]['close']
            total_c2 = 0

        profits = total_c1 - 1.0
        return profits
