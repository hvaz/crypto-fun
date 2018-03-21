import time

# if the market is c2/c1, quantity is the quantity of c2 that will be bought on each trade

def stat_trade(exchange, market, quantity):

    buy_th = -1.0
    sell_th = 1.0
    past_interval = 200
    candle_size = 1
    candle_unit = "minute"

    sleep_interval = 3*60
    time_to_reset = 10 * sleep_interval

    side = 'c1'

    # on each cycle of this loop an order is made on one of the sides
    # when the order is filled or canceled, it continues to the next cycle
    while True:

        candle_list = get_candles(market, candle_size, candle_unit, past_interval)
        
        avg = get_average(candle_list)
        stdev = get_stdev(candle_list)

        if side == 'c1':

            buy_price = avg + stdev * buy_th

            current_order = make_order(exchange, market, 'buy', quantity, buy_price)

            # some error handling should go here (insufficient funds, etc)

            elapsed_time = 0

            time.sleep(sleep_interval)
            elapsed_time += sleep_interval
            
            while get_order_status(current_order) != 'filled':

                if elapsed_time > time_to_reset:
                    # there should be some error handling here since ordery may be partially filled
                    cancel_order(order)
                    continue

                time.sleep(sleep_interval)
                elapsed_time += sleep_interval
                
            side = 'c2'
            continue

        if side == 'c2':
            
            sell_price = avg + stdev * sell_th

            current_order = make_order(exchange, market, 'sell', quantity, sell_price)

            # some error handling should go here

            elapsed_time = 0

            time.sleep(sleep_interval)
            elapsed_time += sleep_interval

            while get_order_status(current_order) != 'filled':

                if elapsed_time> time_to_reset:
                    # there should be some error handling here since ordery may be partially filled      
                    cancel_order(order)
                    continue

                time.sleep(sleep_interval)
                elapsed_time += sleep_interval

            side = 'c1'
            continue
