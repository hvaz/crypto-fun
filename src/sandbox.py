import random
from models_manager import TestManager

class SandboxManager(TestManager):

    def __init__(self, exchange_name, portfolio, candles_magnitude):
        super(SandboxManager, self).__init__(exchange_name, portfolio, candles_magnitude, "sandbox")


    def apply_model_once(self, mkt_obj, params):
        return self.test_sandbox_model(mkt_obj, params)


    def test_sandbox_model(self, mkt_obj, params):
        start, end = int(params["start"]), int(params["end"])
        return self.optimize_then_stat(mkt_obj, start, end)[0]


    def optimize_stats(self, mkt_obj, start, end):
        lim = 1000
        mmax = -2

        calib_proportion = 0.1
        updating = True

        for i in range(lim):
            buy_th = -6 * random.random()
            sell_th = 6 * random.random()
            profit, buy_count, sell_count = \
                self.test_stat_model(mkt_obj, start, end, buy_th, sell_th, calib_proportion, updating)
            
            if profit > mmax:
                bestbuy = buy_th
                bestsell = sell_th
                mmax = profit

        return (bestbuy, bestsell)


    def optimize_then_stat(self, mkt_obj, start, end):
        half = int( (start + end) / 2 )
        optimized = self.optimize_stats(mkt_obj, start, half)

        return self.test_stat_model(mkt_obj, half, end, optimized[0], optimized[1], 0.1, True)
