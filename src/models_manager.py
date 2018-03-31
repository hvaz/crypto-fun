import random
from ccxt_exchanges import ccxtExchange
from printing import print_comparing_hold
from infos import valid_strategies

class TestManager(ccxtExchange):

    def __init__(self, exchange_name, portfolio, candles_magnitude, strategy):
        try:
            super(TestManager, self).__init__(exchange_name)
        except:
            raise

        else:
            ## List of market objects in this portfolio, all in the same exchange
            self.portfolio = portfolio
            ## Strategy to be followed by manager
            self.strategy = strategy
            ## Magnitute of candles (1 minute, 3 minutes, 1 day, etc)
            self.candles_magnitude = candles_magnitude
    

    def apply_model_to_portfolio(self, params): 
        profits = {}
        for mkt_obj in self.portfolio:
            profit = self.apply_model_once(mkt_obj, params)
            profits[mkt_obj] = profit

        return profits


    def apply_model_once(self, mkt_obj, params):
        
        try:
            start, end = params["start"], params["end"]
        except:
            start, end = None, None

        if self.strategy == "ema":
            short_factor, long_factor = params["short_factor"], params["long_factor"]
            threshold = params["threshold"]
            return self.test_ema_model(mkt_obj, start, end, short_factor, long_factor, threshold)

        elif self.strategy == "stat":
            buy_th, sell_th = params["stat_buy_th"], params["stat_sell_th"]
            calib_proportion = params["calib_proportion"]
            updating = params["updating_stat"]
            return self.test_stat_model(mkt_obj, start, end, buy_th, sell_th, calib_proportion, updating)

        elif self.strategy == "hold":
            calib_proportion = params["calib_proportion"]
            return self.test_hold_model(mkt_obj, start, end, calib_proportion)

        elif self.strategy == "study_stats":
            calib_proportion = params["calib_proportion"]
            updating = params["updating_stat"]
            return self.study_stats(mkt_obj, start, end, calib_proportion, updating)

        else:
            raise ValueError("{}: Invalid strategy in models_manager.py".format(self.strategy))


    def test_ema_model(self, mkt_obj, start, end, short_factor, long_factor, threshold):
        fee = mkt_obj.taker_fee
        c_list = mkt_obj.get_candles(self.candles_magnitude, start, end)
        short_ema_list = mkt_obj.candles[self.candles_magnitude].get_ema_list(short_factor, start, end)
        long_ema_list = mkt_obj.candles[self.candles_magnitude].get_ema_list(long_factor, start, end)

        # the market is c2/c1                                                                    
        total_c1 = 1.0
        total_c2 = 0.0
        side = 'c1'

        for c, short_ema, long_ema in zip(c_list, short_ema_list, long_ema_list):
            close = float(c['close_price'])

            if (short_ema > (long_ema * (1 + threshold)) and side == 'c1'):
                total_c2 = (1 - fee) * total_c1 / close
                total_c1 = 0
                side = 'c2'

            if (short_ema < (long_ema * (1 - threshold)) and side == 'c2'):
                total_c1 = (1 - fee) * total_c2 * close
                total_c2 = 0
                side = 'c1'

        if side == 'c2':
            total_c1 = (1 - fee) * total_c2 * close
            total_c2 = 0

        profits = total_c1 - 1.0
        return profits


    def test_vidya_model(self, mkt_obj, start, end, short_factor, long_factor, threshold):
        fee = mkt_obj.taker_fee
        c_list = mkt_obj.get_candles(self.candles_magnitude, start, end)
        short_ema_list = mkt_obj.candles[self.candles_magnitude].get_ema_list(short_factor, start, end)
        long_ema_list = mkt_obj.candles[self.candles_magnitude].get_ema_list(long_factor, start, end)

        # the market is c2/c1 
        total_c1 = 1.0
        total_c2 = 0.0
        side = 'c1'

        for c, short_ema, long_ema in zip(c_list, short_ema_list, long_ema_list):
            close = float(c['close_price'])

            if (short_ema > (long_ema * (1 + threshold)) and side == 'c1'):
                total_c2 = (1 - fee) * total_c1 / close
                total_c1 = 0
                side = 'c2'

            if (short_ema < (long_ema * (1 - threshold)) and side == 'c2'):
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
    def test_stat_model(self, mkt_obj, start, end, buy_th, sell_th, calib_proportion, updating=True):
        fee = mkt_obj.maker_fee
        end_calib = int(start + (end - start) * calib_proportion)
        c_list = mkt_obj.get_candles(self.candles_magnitude, start, end_calib)
        
        if end-start < 8:
            return 0

        if end_calib - start < 4:
            end_calib = min(end, start+4)

        tot = 0
        n = 0
        for c in c_list:
            close = float(c['close_price'])
            tot += close
            n += 1

        avg = tot / n
        tot = 0
        for c in c_list:
            close = float(c['close_price'])
            tot += (close - avg)**2

        stdev = (tot / (n - 1))**0.5

        # the market is c1/c2
        total_c1 = 1.0
        total_c2 = 0
        side = 'c1'
        buy_count = 0
        sell_count = 0

        c_list_after_end_calib = mkt_obj.get_candles(self.candles_magnitude, start=end_calib)
        for c in c_list_after_end_calib:
            close = float(c['close_price'])

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


    def test_hold_model(self, mkt_obj, start, end, calib_proportion):
        fee = mkt_obj.taker_fee
        c_list = mkt_obj.get_candles(self.candles_magnitude, start, end)
        total_c1 = 1.0
        total_c2 = 0.0
        end_calib = int(start + calib_proportion * (end - start))
        
        close_price = float(mkt_obj.candles[self.candles_magnitude].get_candle(end_calib)['close_price'])
        total_c2 = (1 - fee) * total_c1 / close_price
        total_c1 = 0

        close_price = float(mkt_obj.candles[self.candles_magnitude].get_candle(end)['close_price'])
        total_c1 = (1 - fee) * total_c2 * close_price
        total_c2 = 0

        profits = total_c1 - 1.0
        return profits


    def study_stats(self, mkt_obj, start, end, calib_proportion, updating=True): 
        lim = 1000
        mmax = -2
        candle_obj = mkt_obj.candles[self.candles_magnitude]
        hold_profit = self.test_hold_model(mkt_obj, start, end, calib_proportion)
        
        print "\n" + "." * 100 + "\n"
        print "Exchange: {}".format(self.ccxt_obj.id)
        print "Market: {}\n".format(mkt_obj.symbol)

        info_hold_profit = "Hold profit: {}".format(hold_profit)
        print_comparing_hold(info_hold_profit, hold_profit, hold_profit)

        print "Avg = {} ....... Std = {}\n".format(candle_obj.get_avg(start, end), \
                                                   candle_obj.get_std(start, end))
        
        for i in range(lim):
            buy_th = -6 * random.random()
            sell_th = 6 * random.random()
            profit, buy_count, sell_count = \
                self.test_stat_model(mkt_obj, start, end, buy_th, sell_th, calib_proportion, updating)
            if profit > mmax:
                bestbuy = buy_th
                bestsell = sell_th
                mmax = profit
                results = {"(buy_th, sell_th)": (buy_th, sell_th), \
                        "(buy_count, sell_count - 1)": (buy_count, sell_count), "profit": profit}
                
                print_comparing_hold(str(results), results["profit"], hold_profit)


    def weighted_stats(self, mkt_obj, start, end, buy_th, sell_th, calib_proportion, updating):
        fee = mkt_obj.maker_fee
        end_calib = int(start + (end - start) * calib_proportion)
        candle_obj = mkt_obj.candles[self.candles_magnitude]
        test_size = end_calib - start
        c_list = candle_obj.candle_list

        if end-start < 8:
            return 0

        if end_calib - start < 4:
            end_calib = min(end, start+4)

        n = test_size
        hh = candle_obj.weighted_avg_and_stdev(n - test_size, n)
        avg = hh[0]
        stdev = hh[1]

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
                hh = candle_object.weighted_avg_and_stdev(n - test_size, n)
                avg = hh[0]
                stdev = hh[1]
                n += 1

        if side == 'c2':
            total_c1 = (1 - fee) * total_c2 * close
            total_c2 = 0

        profits = total_c1 - 1.0
        return profits
