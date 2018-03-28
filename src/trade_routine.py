import time
from traders import ExchangeTrader

def test_trader_pipeline():

    hitbtc2 = ExchangeTrader("hitbtc2")

    try:
        hitbtc2.buy("ETH/BTC", 0.001, 0.00059498)
        hitbtc2.sell("ETH/BTC", 0.001, 0.1)
    except Exception as e:
        raise e

    time.sleep(5)
    
    for order in hitbtc2.orders:
        assert(order.status() == 'open')

    time.sleep(5)

    num_orders = len(hitbtc2.orders)
    for order in hitbtc2.orders:
        order.cancel()
        num_orders -= 1
        assert(len(hitbtc2.orders) == num_orders)

    time.sleep(5)

    for order in hitbtc2.orders:
        assert(order.status() == 'canceled')


test_trader_pipeline()
