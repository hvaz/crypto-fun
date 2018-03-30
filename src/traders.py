import ccxt
from keys import keys
from ccxt_exchanges import ccxtExchange
from orders import Order

class ExchangeTrader(ccxtExchange):

    def __init__(self, exchange_name):
        try:
            super(ExchangeTrader, self).__init__(exchange_name)
            exchange_id = self.ccxt_obj.id
            self.ccxt_obj.apiKey = keys[exchange_id]['apiKey']
            self.ccxt_obj.secret = keys[exchange_id]['secret']
        except:
            raise
        else:
            self.orders_alive = []
            self.orders_history = []


    def _make_order(self, mkt_symbol, quantity, price=None, side='buy', order_type='limit'):
        if side not in ['buy', 'sell']:
            raise ValueError("make order: -side- parameter must be either 'buy' or 'sell'")
        if order_type not in ['limit', 'market']:
            raise ValueError("make order: -order_type- parameter must be either 'limit' or 'market'")
        
        try:
            if order_type == 'limit':
                if side == 'buy':
                    response = self.ccxt_obj.create_limit_buy_order(mkt_symbol, quantity, price)
                else:
                    response = self.ccxt_obj.create_limit_sell_order(mkt_symbol, quantity, price)

            else:
                if side == 'buy':
                    response = self.ccxt_obj.create_market_buy_order(mkt_symbol, quantity)
                else:
                    response = self.ccxt_obj.create_market_sell_order(mkt_symbol, quantity)
            
            order = Order(self, response['id'])
            self.orders_alive.append(order)
            self.orders_history.append(order)
        except:
            raise
        else:
            return order


    def buy(self, mkt_symbol, quantity, price=None, limit=True):
        if limit:
            self._make_order(mkt_symbol, quantity, price, side='buy', order_type='limit')
        else:
            self._make_order(mkt_symbol, quantity, price, side='buy', order_type='market')


    def sell(self, mkt_symbol, quantity, price, limit=True):
        if limit:
            self._make_order(mkt_symbol, quantity, price, side='sell', order_type='limit')
        else:
            self._make_order(mkt_symbol, quantity, price, side='sell', order_type='market')


    def kill_order(self, order):
        try:
            self.orders_alive.remove(order)
        except:
            raise
