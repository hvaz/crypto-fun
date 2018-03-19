import ccxt
import json
from keys import keys

class ExchangeTrader():

    def __init__(self, exchange_name):
        self.exchange = getattr(ccxt, exchange_name)({
            'apiKey': keys['exchange_name']['public'],
            'secret': keys['exchange_name']['private']
        })

        self.orders = []


    def _make_order(self, mkt_symbol, side='buy', amount, price=None, order_type='limit'):
        if side not in ['buy', 'sell']:
            raise ValueError("make order: -side- parameter must be either 'buy' or 'sell'")
        if order_type not in ['limit', 'market']:
            raise ValueError("make order: -order_type- parameter must be either 'limit' or 'market'")
        
        try:
            if order_type == 'limit':
                if side == 'buy':
                    response = self.exchange.create_limit_buy_order(mkt_symbol, amount, price)
                else:
                    response = self.exchange.create_limit_sell_order(mkt_symbol, amount, price)

            else:
                if side == 'buy':
                    response = self.exchange.create_market_buy_order(mkt_symbol, amount)
                else:
                    response = self.exchange.create_market_sell_order(mkt_symbol, amount)
        except:
            print e
        else:
            order_id = str_to_dict(response)['id']
            order_info = {'order_id': order_id, 'mkt_symbol': mkt_symbol, \
                    'side': side, 'amount': amount, 'price': price, 'order_type': order_type}
            self.orders.append(order_info)
            return order_id


    def buy(self, mkt_symbol, amount, price=None, limit=True):
        if limit:
            self._make_order(side='buy', amount, price, order_type='limit')
        else:
            self._make_order(side='buy', amount, price, order_type='market')


    def sell(self, amount, price, limit=True):
        if limit:
            self._make_order(mkt_symbol, side='sell', amount, price, order_type='limit')
        else:
            self._make_order(mkt_symbol, side='sell', amount, price, order_type='market')

            
    def cancel_order(self, order_id):
        '''
            Cancel order identified by order_id

            order_id (str): id of order being canceled

            Return Value: https://github.com/ccxt/ccxt/wiki/Manual#exceptions-on-order-canceling
        '''
        try:
            self.exchange.cancel_order(order_id)
        except Exception as e:
            print e


    def full_order_info(self, order_id):
        '''
            Fetches complete information of an order. Synchronous.
            Not all exchanges support this method. Async option can be implemented

            order_id (str): id of order whose information is being fetched

            Return Value: dictionary as specified in https://github.com/ccxt/ccxt/wiki/Manual#order-structure
        '''
        if self.exchange.has['fetchOrder']:
            order = self.exchange.fetch_order[order_id]
            return order
        else:
            return None


    def order_status(self, order_id):
        '''
            Determines order's status using full_order_info method
            
            order_id (str): id of order whose status is being checked

            Return Value: None, 'open', 'closed', or 'canceled'    
        '''
        status = None
        try:
            status = self.full_order_info['status']
        except Exception as e:
            print e
        finally:
            return status
