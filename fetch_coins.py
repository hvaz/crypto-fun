import requests
import json
import time

LIMIT = 1000

class exchanges(object):

    def __init__(self, name, trades_url):

        self._name = name
        self._trades_url = trades_url

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

        first_from = 208000000
        #first_from = 208100511
        first_till = first_from + 1000
        limit = LIMIT
        by = 'id'

        payload = {'by': by, 'limit': limit, 'from': first_from, 'till': first_till}
        
        filename = symbol + '_trades.txt'
        with open(filename, 'a') as f:
            
            with requests.Session() as session:
                
                stop = self._most_recent_trade_id(symbol)
                if (stop == None):
                    print 'try again...'

                while payload['from'] <= stop:
                    
                    print '[{}, {}], stop = {}'.format(payload['from'], payload['till'], stop)
                    
                    url = self._trades_url
                    r = session.get(url.format(symbol), params=payload)
                    #print r.content
                    if (r.status_code != 200):
                        raise r.raise_for_status()

                    trades_list = json.loads(r.content)
                    if (len(trades_list) == 0):

                        payload['from'] += LIMIT
                        payload['till'] += LIMIT
                        
                    else:
                        
                        f.write(r.content)
                        payload['from'] = trades_list[0]['id'] + 1000
                        payload['till'] = payload['from'] + LIMIT



hitbtc = exchanges('hitbtc', "https://api.hitbtc.com/api/2/public/trades/{}")
hitbtc.get_trades('SKINBTC')
