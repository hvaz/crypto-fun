import ccxt
from keys import keys
from exchanges import Exchange
from orders import Order

class ExchangeTrader(ccxtExchange):

    def __init__(self):
        try:
            exchange_id = self.ccxt_exchange.id
            self.ccxt_exchange.apiKey = keys[exchange_id]['apiKey'],
            self.ccxt_exchange.secret = keys[exchange_id]['secret']
        except Exception as e:
            raise e
        else:
            self.orders = []


    def _make_order(self, mkt_symbol, quantity, price=None, side='buy', order_type='limit'):
        if side not in ['buy', 'sell']:
            raise ValueError("make order: -side- parameter must be either 'buy' or 'sell'")
        if order_type not in ['limit', 'market']:
            raise ValueError("make order: -order_type- parameter must be either 'limit' or 'market'")
        
        try:
            if order_type == 'limit':
                if side == 'buy':
                    response = self.ccxt_exchange.create_limit_buy_order(mkt_symbol, quantity, price)
                else:
                    response = self.ccxt_exchange.create_limit_sell_order(mkt_symbol, quantity, price)

            else:
                if side == 'buy':
                    response = self.ccxt_exchange.create_market_buy_order(mkt_symbol, quantity)
                else:
                    response = self.ccxt_exchange.create_market_sell_order(mkt_symbol, quantity)
            
            order = Order(self, response['id'])
            self.orders.append(order)
        except Exception as e:
            raise e
        else:
            return order.id


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


    def remove_order(self, order_id):
        try:
            self.orders.remove(order_id)
        except Exception as e:
            raise e
