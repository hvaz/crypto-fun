import requests
import json

LIMIT = 1000

class exchange(object):

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
