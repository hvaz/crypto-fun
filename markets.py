intervals = ['1m', '3m', '5m', '15m', '30m', \
             '1h', '2h', '4h', '6h', '8h', '12h', \
             '1d', '3d', \
             '1w',
             '1M']

class Market(object):

    def __init__(self, name, percentage_fee):

        self.name = name
        self.fee = percentage_fee
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
            close = float(candle_list[i]['close'])
            if (short_ema_list[i] > (long_ema_list[i]*(1+treshold)) and side == 'c1'):
                total_c2 = (1-fee)*total_c1*close
                total_c1 = 0
                side = 'c2'

            if (short_ema_list[i] < (long_ema_list[i]*(1-treshold)) and side == 'c2'):
                total_c1 = (1 - fee) * total_c2 / close
                total_c2 = 0
                side = 'c1'

        if side == 'c2':
            total_c1 = (1 - fee) * total_c2 / close
            total_c2 = 0

        profits = total_c1 - 1.0
        return profits
