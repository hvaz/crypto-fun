import ccxt
from utils import active_internet

NUM_CANDLES = 1000

class MarketCandles(object):
    def __init__(self, ccxt_exchange, mkt_symbol, interval):
        if mkt_symbol not in ccxt_exchange.markets:
            print ccxt_exchange.markets
            raise Exception("invalid market symbol")
        self.ccxt_exchange = ccxt_exchange
        self.mkt_symbol = mkt_symbol
        self.interval = interval
        self.candle_list = []
        self.update_candles()

    def update_candles(self):
        ## should start appending later on
        if not self.ccxt_exchange.ccxt_obj.has['fetchOHLCV']:
            raise Exception("{} Error: impossible to fetch candles for this exchange".format(self.exchange.name))

        def get_offline_candles(filename):
            try:
                with open(filename, 'r') as f:
                    candles = f.read()[1:-2].split("}, ")
                    candle_data = [str_to_dict(c + "}") for c in candles]
            except:
                raise
            else: 
                return candle_data

        def store_candles_offline(filename):
            with open(filename, 'w') as f:
                f.write(str(self.candle_list))

        def format_candle_list(candle_list):
            new_list = []
            for c in candle_list:
                candle_dict = {
                    'tstamp': c[0],
                    'open_price': c[1],
                    'max_price': c[2],
                    'min_price': c[3],
                    'close_price': c[4],
                    'volume': c[5]
                }
                new_list.append(candle_dict)
            return new_list

        filename = './candles_txt_data/' + 'exchange=' + self.ccxt_exchange.ccxt_obj.id + '_mkt=' \
                   + self.mkt_symbol.replace("/", "-") + '_data=candles_interval=' + self.interval + '.txt'
        if not active_internet():
            self.candle_list = get_offline_candles(filename)
        else:
            try:
                self.candle_list = format_candle_list(
                                        self.ccxt_exchange.ccxt_obj.fetch_ohlcv(self.mkt_symbol, self.interval, limit=1000)
                                    )
                store_candles_offline(filename)
            except:
                raise


    def get_avg(self, start=None, end=None):
        start = 0 if start == None else start
        end = len(self.candle_list) if end == None else end
        
        n = 0
        tot = 0.0

        for i in range(start, end):
            close_price = self.candle_list[i]['close_price']
            tot += close_price
            n += 1
            
        return (tot / n)


    def get_std(self, start=None, end=None):
        start = 0 if start == None else start
        end = len(self.candle_list) if end == None else end
        
        n = 0
        tot = 0.0
        avg = self.get_avg(start, end)

        for i in range(start, end):
            close_price = self.candle_list[i]['close_price']
            tot += (close_price - avg)**2
            n += 1

        return (tot / n)**0.5


    def avg_and_stdev(self, start, end):

        avg = self.get_avg(start, end)
        stdev = self.get_stdv(start, end)
        return (avg, stdev)


    def weighted_avg_and_stdev(self, start, end):

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



    # assumes data is in ascending time
    def get_ema_list(self, factor):
        ema_list = []
        current_ema = - 1

        for candle in self.candle_list:
            close = float(candle['close_price'])
            
            if current_ema == -1:
                current_ema = close
            else:
                current_ema = close * factor + current_ema * (1 - factor)
           
            ema_list.append(current_ema)

        return ema_list


    def get_vidya_list(self, factor):
        vidya_list = []
        current_vidya = -1

        for candle in self.candle_list:
            close_price = float(candle['close_price'])
            open_price = float(candle['open_price'])
            cmo = (open_price - close_price) / (open_price + close_price)
            current_factor = abs(cmo) * factor

            if current_vidya == -1:
                current_vidya = close_price
            else:
                current_vidya = close_price * current_factor+ current_vidya * (1 - current_factor)

            vidya_list.append(current_vidya)
        
        return vidya_list
