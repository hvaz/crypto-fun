import time
from traders import ExchangeTrader

hitbtc2 = ExchangeTrader("hitbtc2")

print "Making orders..."
hitbtc2.buy("ETH/BTC", 0.001, 0.00059498)
hitbtc2.sell("ETH/BTC", 0.001, 0.1)

time.sleep(5)

print "\nRetrieving orders' status..."
for order in hitbtc2.orders:
    print order
    print 'order status = {}'.format(hitbtc2.order_status(order['id']))

time.sleep(5)

print "\nCanceling orders..."
for order in hitbtc2.orders:
    print order
    hitbtc2.cancel_order(order['id'])

time.sleep(5)

print "\nRetrieving orders' status again..."
for order in hitbtc2.orders:
    print order
    print 'order status = {}'.format(hitbtc2.order_status(order['id']))
