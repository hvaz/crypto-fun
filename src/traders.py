import ccxt
from keys import keys
from exchanges import Exchange
from orders import Order

class ExchangeTrader(Exchange):

    def __init__(self, exchange_name):
        try:
            self.exchange = getattr(ccxt, exchange_name)({
                'apiKey': keys[exchange_name]['apiKey'],
                'secret': keys[exchange_name]['secret']
            })
        except Exception as e:
            raise e
        else:
            self.orders = []


    def _make_order(self, mkt_symbol, amount, price=None, side='buy', order_type='limit'):
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
            
            order = Order(self.exchange, response['id'])
            self.orders.append(order)
        except Exception as e:
            raise e
        else:
            return order.id


    def buy(self, mkt_symbol, amount, price=None, limit=True):
        if limit:
            self._make_order(mkt_symbol, amount, price, side='buy', order_type='limit')
        else:
            self._make_order(mkt_symbol, amount, price, side='buy', order_type='market')


    def sell(self, mkt_symbol, amount, price, limit=True):
        if limit:
            self._make_order(mkt_symbol, amount, price, side='sell', order_type='limit')
        else:
            self._make_order(mkt_symbol, amount, price, side='sell', order_type='market')
