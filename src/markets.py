class Market(object):
    def __init__(self, name, percentage_fee, intervals):
        self.name = name
        self.fee = percentage_fee
        self.candles = {}
        
        for _, unit_dict in intervals.iteritems():
            for size in unit_dict:
                self.candles[unit_dict[size]] = None

    
    def test_ema_model(self, candles_object, start, end, short_factor, long_factor, threshold):
        
        ## adjust fee to be between 0 and 1 since it is given as percentage
        fee = self.fee / 100
        candle_list = candles_object.data
        short_ema_list = candles_object.get_ema_list(short_factor)
        long_ema_list = candles_object.get_ema_list(long_factor)

        # the market is c2/c1                                                                    
        total_c1 = 1.0
        total_c2 = 0.0
        side = 'c1'

        for i in range(start, end):
            close = float(candle_list[i]['close_price'])
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
    def test_stat_model(self, candles_object, start, end, buy_th, sell_th):
        
        candles_list = candles_object.data
        fee = self.fee / 100
        calib_proportion = 0.2
        end_calib = int(start+(end-start) * calib_proportion)
        
        tot = 0
        n = 0
        for i in range(start, end_calib):
            close = float(candle_list[i]['closing_price'])
            tot += close
            n += 1
        
        tot = 0
        for i in range(start, end_calib):
            close = float(candle_list[i]['closing_price'])
            tot += (close - avg)**2

        stdev = (tot / (n-1))**0.5

        # the market is c1/c2
        total_c1 = 1.0
        total_c2 = 0

        for i in range(start, end):
            close = float(candle_list[i]['close_price'])
            if (close > (avg + stdev * buy_th) and side == 'c1'):
                total_c2 = (1 - fee) * total_c1 / close
                total_c1 = 0
                side = 'c2'

            if (close > (avg + stdev * sell_th) and side == 'c2'):
                total_c1 = (1 - fee) * total_c2 * close
                total_c2 = 0
                side = 'c1'

        if side == 'c2':
            total_c1 = (1 - fee) * total_c2 * close
            total_c2 = 0

        profits = total_c1 - 1.0
        return profits                         
                        
                         
                     
