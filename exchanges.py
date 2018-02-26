import requests
import json

from markets import Market
from candles import Candles
import info_exchanges


class Exchange(object):

    def __init__(self, info):

        self.name = info['name']
        self.api_endpoint = info['api_endpoint']
        self.percentage_fee = info['percentage_fee']
        self.every_transaction_fee = info['every_transaction_fee']
        self.markets = {}
        self.candles_endpoint = info['candles_endpoint']
        self.candles_intervals = info['candles_intervals']
        self.data_ascending = info['data_ascending']

        if (len(info['symbols']) > 0):
            for s_name in info['symbols']:
                self.markets[s_name] = Market(s_name, self.percentage_fee)


    def __format_candles_binance(self, candles):

        new_candles = []
        for c in candles:
            
            c_new = {}
            c_new['open_tstamp'] = int(c[0])
            c_new['close_tstamp'] = int(c[6])
            c_new['open_price'] = float(c[1])
            c_new['close_price'] = float(c[4])
            c_new['min_price'] = float(c[3])
            c_new['max_price'] = float(c[2])
            c_new['volume'] = float(c[5])
            c_new['volume_quote'] = float(c[7])
            new_candles.append(c_new)

        return new_candles


    def __format_candles(self, candles):

        if (self.name == 'binance'):
            return self.__format_candles_binance(candles)
        else:
            return None

    
    def __get_candles_data(self, mkt_name, interval):

        filename = 'exchange=' + self.name + '_mkt=' + mkt_name + '_data=candles_interval=' + interval + '.txt'
        with open(filename, 'a') as f:
            
            with requests.Session() as session:
                
                payload = {'symbol': mkt_name, 'interval': interval}
                url = self.api_endpoint + self.candles_endpoint
                r = session.get(url, params=payload)
                
                json_content = json.loads(r.content)
                formatted_candles = self.__format_candles(json_content)
                if (formatted_candles == None):
                    raise 'Cannot format candles for this exchange yet. Please implement method'
                    return

                print "Number of candles: {}".format(len(formatted_candles))

                if (r.status_code != 200):
                    raise r.raise_for_status()

                f.write(str(formatted_candles))


    def update_candles(self, mkt_name, interval):

        if (mkt_name not in self.markets.keys() or 
            interval not in self.candles_intervals):

            raise "Invalid parameters for get_candles"
            return
        
        mkt = self.markets[mkt_name]
        candles_data = self.__get_candles_data(mkt_name, interval)
        mkt.candles[interval] = Candles(interval, candles_data)

        
info_binance = info_exchanges.get_info_binance()
binance = Exchange(info_binance)
binance.update_candles('ETHBTC', '1m')


"""
    def _most_recent_trade_id(self, symbol):

        url = self._trades_url
        payload = {'limit': 1}
        r = requests.get(url.format(symbol), params=payload)
        if (r.status_code != 200):
            raise r.raise_for_status()
            return

        trades_list = json.loads(r.content)
        return trades_list[0]['id']

    def get_trades(self, symbol):

        stop = 208000000
        #first_from = 208100511
        most_recent = self._most_recent_trade_id(symbol)
        first_from = most_recent
        first_till = first_from - LIMIT
        limit = LIMIT
        by = 'id'

        payload = {'by': by, 'limit': limit, 'till': first_from, 'from': first_till}
        
        filename = symbol + '_trades.txt'
        with open(filename, 'a') as f:
            
            with requests.Session() as session:
                
                if (stop == None):
                    print 'try again...'

                while payload['from'] >= stop:
                    
                    print '[{}, {}], stop = {}'.format(payload['from'], payload['till'], stop)
                    
                    url = self._trades_url
                    r = session.get(url.format(symbol), params=payload)
                    print r.content
                    if (r.status_code != 200):
                        raise r.raise_for_status()

                    trades_list = json.loads(r.content)
                    if (len(trades_list) == 0):

                        payload['till'] -= LIMIT
                        payload['from'] -= LIMIT
                        
                    else:
                        
                        f.write(r.content)
                        payload['till'] = trades_list[0]['id'] - LIMIT
                        payload['from'] = payload['from'] - LIMIT



hitbtc = exchange('hitbtc', "https://api.hitbtc.com/api/2/public/trades/{}")
hitbtc.get_trades('SKINBTC')
"""
