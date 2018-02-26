import requests
import json

import markets
import info_exchanges

LIMIT = 1000

class exchange(object):

    def __init__(self, info):

        self.name = info['name']
        self.api = info['api_endpoint']
        self.symbols = info['symbols']
        self.candles_endpoint = info['candles_endpoint']
        self.candles_intervals = info['candles_intervals']
        self.data_ascending = info['data_ascending']

        if (symbol != None):
            for s_name in symbols:
                new_symbol = symbol(s_name)
                self._symbols.append(new_symbol)

    def get_candles(self, symbol_name, interval):

        if (symbol_name not in self.symbols or 
            interval not in self.candles_intervals):

            raise "Invalid parameters for get_candles"
            return

        mkt = market(symbol_name)
        return mkt.get_candles(interval)

        

binance = exchange(info_binance)


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
