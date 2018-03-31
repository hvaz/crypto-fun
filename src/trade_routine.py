import time
from traders import ExchangeTrader
from markets import Market

def test_trader_pipeline():

    hitbtc2 = ExchangeTrader("hitbtc2")
    eth_btc_market = Market("ETH/BTC", hitbtc2)

    try:
        hitbtc2.buy(eth_btc_market, 0.001, 0.00059498)
        time.sleep(0.1)
        hitbtc2.sell(eth_btc_market, 0.001, 0.1)
        time.sleep(0.1)
    except:
        raise

    time.sleep(1)
    
    for order in hitbtc2.orders_alive:
        print(order.status())
        time.sleep(0.1)
        print(order.status())
        time.sleep(0.1)
        print(order.status())
        time.sleep(0.1)
        assert(order.status() == 'open')


    time.sleep(1)

    num_orders = len(hitbtc2.orders_alive)
    print hitbtc2.orders_history
    for order in hitbtc2.orders_history:
        order.cancel()
        time.sleep(0.1)
        num_orders -= 1
        print hitbtc2.orders_alive
        assert(len(hitbtc2.orders_alive) == num_orders)

    time.sleep(1)

    for order in hitbtc2.orders_history:
        assert(order.status() == 'canceled')


test_trader_pipeline()
