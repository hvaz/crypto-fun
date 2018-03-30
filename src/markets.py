import random
import ccxt
from collections import defaultdict
from ccxt_exchanges import ccxtExchange
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
        
        #start = 0 if start == None else start
        #end = len(self.candles[interval].candle_list) if end == None else end

        return self.candles[interval]
    #.candle_list[start:end]
