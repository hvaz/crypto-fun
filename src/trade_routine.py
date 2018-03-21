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
        order_status = hitbtc2.order_status(order['id'])
        assert(order_status == 'open')

    time.sleep(5)

    for order in hitbtc2.orders:
        hitbtc2.cancel_order(order['id'])

    time.sleep(5)

    for order in hitbtc2.orders:
        order_status = hitbtc2.order_status(order['id'])
        assert(order_status == 'canceled')


test_trader_pipeline()
