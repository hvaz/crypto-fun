import random
import ccxt
from collections import defaultdict
from exchanges import ccxtExchange
from candles import MarketCandles
from printing import print_comparing_hold

class Market(object):

    def __init__(self, symbol, ccxt_exchange):
        
        self.symbol = symbol
        self.ccxt_exchange = ccxt_exchange
        self.taker_fee = ccxt_exchange.ccxt_obj.market(symbol)['taker']
        self.maker_fee = ccxt_exchange.ccxt_obj.market(symbol)['maker']
        self.candles = defaultdict(lambda: None)
        

    def get_candles(self, interval, start=None, end=None):
        
        ## IF PROGRAM IS RUNNING FOREVER, THE LIST OF MARKET CANDLES DOES NOT UPDATE
        ## AS TIME GOES BY

        if self.candles[interval] == None:
            self.candles[interval] = MarketCandles(self.ccxt_exchange, self.symbol, interval)
        
        start = 0 if start == None else start
        end = len(self.candles[interval].candle_list) if end == None else end

        return self.candles[interval].candle_list[start:end]


    def test_ema_model(self, candle_object, start, end, short_factor, long_factor, threshold):
        
        fee = self.taker_fee
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


    def test_vidya_model(self, candle_object, start, end, short_factor, long_factor, threshold):

        fee = self.taker_fee
        c_list = candle_object.candle_list
        short_ema_list = candle_object.get_vidya_list(short_factor)
        long_ema_list = candle_object.get_vidya_list(long_factor)

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
    def test_stat_model(self, candle_object, start, end, buy_th, sell_th, calib_proportion, updating=True):
        
        fee = self.maker_fee
        end_calib = int(start + (end - start) * calib_proportion)
        c_list = candle_object.candle_list
        
        if end-start < 8:
            return 0

        if end_calib - start < 4:
            end_calib = min(end, start+4)

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
        buy_count = 0
        sell_count = 0

        for i in range(end_calib, end - 1):
            close = float(c_list[i + 1]['close_price'])

            if (close < (avg + stdev * buy_th) and side == 'c1'):
                total_c2 = (1 - fee) * total_c1 / close
                total_c1 = 0
                buy_count += 1
                side = 'c2'

            if (close > (avg + stdev * sell_th) and side == 'c2'):
                total_c1 = (1 - fee) * total_c2 * close
                total_c2 = 0
                sell_count += 1
                side = 'c1'

            if (updating):
                avg = (avg * n + close) / (n + 1)
                stdev = (((stdev**2) * (n - 1) + (close - avg)**2) / n)**0.5
                n += 1

        if side == 'c2':
            total_c1 = (1 - fee) * total_c2 * close
            total_c2 = 0

        profits = total_c1 - 1.0
        return (profits, buy_count, sell_count)


    def test_hold_model(self, candle_object, start, end, calib_proportion):
        
        candle_list = candle_object.candle_list
        fee = self.taker_fee
        total_c1 = 1.0
        total_c2 = 0.0

        end_calib = int(start + calib_proportion * (end - start))
        
        close_price = float(candle_list[end_calib]['close_price'])
        total_c2 = (1 - fee) * total_c1 / close_price
        total_c1 = 0

        close_price = float(candle_list[end]['close_price'])
        total_c1 = (1 - fee) * total_c2 * close_price
        total_c2 = 0

        profits = total_c1 - 1.0
        return profits


    def study_stats(self, candle_object, start, end, calib_proportion, updating=True):
        
        lim = 1000
        mmax = -2
        hold_profit = self.test_hold_model(candle_object, start, end, calib_proportion)
        
        print "\n" + "." * 100 + "\n"
        print "Exchange: {}".format(self.ccxt_exchange.ccxt_obj.id)
        print "Market: {}\n".format(self.symbol)
        print "Hold profit:", hold_profit
        print "Avg = {} ....... Std = {}\n".format(candle_object.get_avg(start, end), \
                                                 candle_object.get_std(start, end))
        
        for i in range(lim):
            buy_th = -6*random.random()
            sell_th = 6*random.random()
            profit, buy_count, sell_count = \
                self.test_stat_model(candle_object, start, end, buy_th, sell_th, calib_proportion, updating)
            if profit > mmax:
                bestbuy = buy_th
                bestsell = sell_th
                mmax = profit
                results = {"(buy_th, sell_th)": (buy_th, sell_th), \
                        "(buy_count, sell_count - 1)": (buy_count, sell_count), "profit": profit}
                
                print_comparing_hold(str(results), results["profit"], hold_profit)


    def test_sandbox_model(self, candle_object, params):
        
        start, end = int(params[0]), int(params[1])

        short_factor, long_factor, threshold = float(params[2]), float(params[3]), float(params[4])

        return self.test_vidya_model(candle_object, start, end, short_factor, long_factor, threshold)



    def avg_and_stdev(self, candle_object, start, end):

        c_list = candle_object.candle_list

        tot = 0
        n = 0
        for i in range(start, end):
            close = float(c_list[i]['close_price'])
            tot += close
            n += 1

        avg = tot / n
        tot = 0
        for i in range(start, end):
            close = float(c_list[i]['close_price'])
            tot += (close - avg)**2

        stdev = (tot / (n - 1))**0.5

        return (avg, stdev)


    def weighted_avg_and_stdev(self, candle_object, start, end):

        c_list = candle_object.candle_list

        tot = 0
        tot_volume = 0
        n = 0
        for i in range(start, end):
            close = float(c_list[i]['close_price'])
            vol = float(c_list[i]['volume'])
            tot += close * vol
            tot_volume += vol
            n += 1

        avg = tot / tot_volume

        tot = 0

        for i in range(start, end):
            close = float(c_list[i]['close_price'])
            vol = float(c_list[i]['volume'])
            tot += vol * (close - avg)**2

        stdev = (tot / tot_volume)**0.5

        return (avg, stdev)


    def optimize_stats(self, candle_object, start, end):


        lim = 1000
        mmax = -2

        calib_proportion = 0.1
        updating = True

        for i in range(lim):
            buy_th = -6*random.random()
            sell_th = 6*random.random()
            profit, buy_count, sell_count = \
                self.test_stat_model(candle_object, start, end, buy_th, sell_th, calib_proportion, updating)
            if profit > mmax:
                bestbuy = buy_th
                bestsell = sell_th
                mmax = profit

        return (bestbuy, bestsell)


    def optimize_then_stat(self, candle_object, start, end):

        half = int( (start + end)/2 )

        optimized = self.optimize_stats(candle_object, start, half)

        return self.test_stat_model(candle_object, half, end, optimized[0], optimized[1], 0.1, True)
