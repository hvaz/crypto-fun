class Market(object):

    def __init__(self, name, percentage_fee, intervals):
        
        self.name = name
        self.fee = percentage_fee
        self.candles = {}
        
        for _, unit_dict in intervals.iteritems():
            for size in unit_dict:
                self.candles[unit_dict[size]] = None


    def test_ema_model(self, candle_object, start, end, short_factor, long_factor, threshold):
        
        ## adjust fee to be between 0 and 1 since it is given as percentage
        fee = self.fee / 100
        c_list = candle_object.candle_list
        short_ema_list = candle_object.get_ema_list(short_factor)
        long_ema_list = candle_object.get_ema_list(long_factor)

        # the market is c2/c1                                                                    
        total_c1 = 1.0
        total_c2 = 0.0
        side = 'c1'

        for i in range(start, end):
            close = float(c_list[i]['close_price'])

            if (short_ema_list[i] > (long_ema_list[i] * (1 + threshold)) and side == 'c1'):
                total_c2 = (1 - fee) * total_c1 / close
                total_c1 = 0
                side = 'c2'

            if (short_ema_list[i] < (long_ema_list[i] * (1 - threshold)) and side == 'c2'):
                total_c1 = (1 - fee) * total_c2 * close
                total_c2 = 0
                side = 'c1'

        if side == 'c2':
            total_c1 = (1 - fee) * total_c2 * close
            total_c2 = 0

        profits = total_c1 - 1.0
        return profits

    # buy_th and sell_th are thresholds given in number of stdev
    # in general buy_th is negative and sell_th is positive
    def test_stat_model(self, candle_object, start, end, buy_th, sell_th, calib_proportion, updating=False):
        
        fee = self.fee / 100
        end_calib = int(start + (end - start) * calib_proportion)
        c_list = candle_object.candle_list
        
        tot = 0
        n = 0
        for i in range(start, end_calib):
            close = float(c_list[i]['close_price'])
            tot += close
            n += 1
       
        avg = tot / n
        tot = 0
        for i in range(start, end_calib):
            close = float(c_list[i]['close_price'])
            tot += (close - avg)**2

        stdev = (tot / (n - 1))**0.5

        # the market is c1/c2
        total_c1 = 1.0
        total_c2 = 0
        side = 'c1'

        for i in range(end_calib, end-1):
            close = float(c_list[i+1]['close_price'])
            if (close < (avg + stdev * buy_th) and side == 'c1'):
                total_c2 = (1 - fee) * total_c1 / close
                total_c1 = 0
                side = 'c2'

            if (close > (avg + stdev * sell_th) and side == 'c2'):
                total_c1 = (1 - fee) * total_c2 * close
                total_c2 = 0
                side = 'c1'

            if (updating):
                avg = (avg * n + close) / (n + 1)
                stdev = (((stdev**2) * (n - 1) + (close - avg)**2) / n)**0.5
                n += 1

        if side == 'c2':
            total_c1 = (1 - fee) * total_c2 * close
            total_c2 = 0

        profits = total_c1 - 1.0
        return profits


    def test_hold_model(self, candle_object, start, end, calib_proportion):
        
        candle_list = candle_object.candle_list
        fee = self.fee / 100
        total_c1 = 1.0
        total_c2 = 0.0

        end_calib = int(start + calib_proportion * (end-start))
        
        close = float(candle_list[end_calib]['close_price'])
        total_c2 = (1 - fee) * total_c1 / close
        total_c1 = 0

        close = float(candle_list[end]['close_price'])
        total_c1 = (1 - fee) * total_c2 * close
        total_c2 = 0

        profits = total_c1 - 1.0
        return profits
