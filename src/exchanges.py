import requests
import json
from datetime import datetime

from markets import Market
from candles import Candles
from utils import active_internet, str_to_dict

NUM_CANDLES = 1000

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

        for s_name in info['symbols']:
            self.markets[s_name] = Market(s_name, self.name, self.percentage_fee, self.candles_intervals)


    def _format_candles(self, candles):
        equivalence = {}
        if (self.name == 'binance'):
            equivalence = {'open_tstamp': 0, 'close_tstamp': 6, 'open_price': 1, 'close_price': 4, \
                           'min_price': 3, 'max_price': 2, 'volume': 5, 'volume_quote': 7}

        elif (self.name == 'hitbtc'):
            equivalence = {'open_tstamp': None, 'close_tstamp': 'timestamp', 'open_price': 'open', \
                           'close_price': 'close', 'min_price': 'min', 'max_price': 'max', \
                           'volume': 'volume', 'volume_quote': 'volumeQuote'}

        else:
            raise 'Cannot format candles for this exchange yet. Please update code.'
   
        formatted_candles = []
        for c in candles:
            new_candle = {}
            
            for param, index in equivalence.items():

                if (index == None):
                    new_candle[param] = None
                else:
                    if (param in ['open_tstamp', 'close_tstamp']):
                        tstamp = c[index]
                        if (self.name == 'hitbtc'):
                            utc_dt = datetime.strptime(tstamp, '%Y-%m-%dT%H:%M:%S.%fZ')
                            tstamp = (utc_dt - datetime(1970, 1, 1)).total_seconds() * 1000 - 1

                        new_candle[param] = int(tstamp)
                    else:
                        new_candle[param] = float(c[index])

            formatted_candles.append(new_candle)

        return formatted_candles


    def _get_candles_url_and_payload(self, mkt_name, interval, limit=1000):
        if (self.name == 'binance'):
            url = self.api_endpoint + self.candles_endpoint
            payload = {'symbol': mkt_name, 'interval': interval, 'limit': limit}

        elif (self.name == 'hitbtc'):
            url = (self.api_endpoint + self.candles_endpoint).format(mkt_name)
            payload = {'period': interval, 'limit': limit}

        else:
            raise 'Cannot get candles for this exchange yet. Please update code'

        return {'url': url, 'payload': payload}

    def _get_offline_candles(self, filename):
        try:
            with open(filename, 'r') as f:
                candles = f.read()[1:-2].split("}, ")
                candle_data = [str_to_dict(c + "}") for c in candles]

        except Exception as e:
            print e
        else: 
            return candle_data 


    def _get_candles_data(self, mkt_name, interval, target):
        filename = './candles_txt_data/' + 'exchange=' + self.name + '_mkt=' + mkt_name \
                   + '_data=candles_interval=' + interval + '.txt'

        if (not active_internet()):
            return self._get_offline_candles(filename)
        
        with open(filename, 'w') as f:
            with requests.Session() as session:
                candles_count = 0
                while (candles_count < target):
                    request_info = self._get_candles_url_and_payload(mkt_name, interval)
                    url, payload = request_info['url'], request_info['payload']

                    r = session.get(url, params=payload)
                    if (r.status_code != 200):
                        raise Exception(r.content)
                    
                    json_content = json.loads(r.content)
                    formatted_candles = self._format_candles(json_content)
                    if (formatted_candles == None):
                        return
                    
                    candles_count += len(formatted_candles)

                    if (r.status_code != 200):
                        raise r.raise_for_status()

                    f.write(str(formatted_candles))
                
        return formatted_candles


    def format_interval(self, size, unit):
        if (unit not in self.candles_intervals.keys()):
            raise Exception('Invalid unit used for candles in this exchange')
        
        possible_intervals = self.candles_intervals[unit]
        possible_sizes = possible_intervals.keys()
        if (size not in possible_sizes):
            raise Exception('Invalid size/unit used for candles in this exchange')

        return possible_intervals[size]


    def update_candles(self, mkt_name, size, unit):
        
        interval = self.format_interval(size, unit)

        if (mkt_name not in self.markets.keys()):
            raise "Invalid mkt_name parameter for get_candles"
        
        mkt = self.markets[mkt_name]
        candles_data = self._get_candles_data(mkt_name, interval, NUM_CANDLES)
        mkt.candles[interval] = Candles(interval, candles_data)
