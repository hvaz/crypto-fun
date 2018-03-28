import time
from traders import ExchangeTrader

def test_trader_pipeline():

    hitbtc2 = ExchangeTrader("hitbtc2")

    try:
        hitbtc2.buy("ETH/BTC", 0.001, 0.00059498)
        hitbtc2.sell("ETH/BTC", 0.001, 0.1)
    except:
        raise

    time.sleep(5)
    
    for order in hitbtc2.orders_alive:
        assert(order.status() == 'open')

    time.sleep(5)

    num_orders = len(hitbtc2.orders_alive)
    for order in hitbtc2.orders_history:
        order.cancel()
        num_orders -= 1
        assert(len(hitbtc2.orders_alive) == num_orders)

    time.sleep(5)

    for order in hitbtc2.orders_history:
        assert(order.status() == 'canceled')


test_trader_pipeline()
