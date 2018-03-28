import ccxt
from collections import defaultdict
from infos import candle_units
from candles import MarketCandles


class ccxtExchange(object):
    def __init__(self, exchange_name):
        try:
            self.ccxt_obj = getattr(ccxt, exchange_name) ()
            self.ccxt_obj.load_markets()
        except Exception as e:
            raise e
        else:
            self.markets = defaultdict()
    
    
    def get_ccxt_candles_interval_format(self, size, unit):
        key = str(size) + candle_units[unit]
        return key
        #return self.ccxt_obj.timeframes[key]


    def get_market_candles(self, mkt_symbol, interval, start=None, end=None):

        ## IF PROGRAM IS RUNNING FOREVER, THE LIST OF MARKET CANDLES DOES NOT UPDATE
        ## AS TIME GOES BY

        try:
            return self.markets[mkt_symbol].get_candles(interval, start, end)
        except:
            raise
