from traders import ExchangeTrader
import time

class MoneyMaker(ExchangeTrader):

    def __init__(self, exchange_name, mkt_symbol, interval):
        try:
            super(MoneyMaker, self).__init__(exchange_name)
            self.mkt_symbol = mkt_symbol
            self.interval = interval
        except:
            raise


    def stat_trade(self, quantity):

        buy_th = -1.0
        sell_th = 1.0
        start = 200

        avg_interval = 60

        sleep_interval = 3 * 60
        time_to_reset = 10 * sleep_interval

        side = 'c1'

        # on each cycle of this loop an order is made on one of the sides
        # when the order is filled or canceled, it continues to the next cycle
        while True:

            candles_obj = self.markets[self.mkt_symbol].get_candles()
            num_of_candles = len(candles_obj.candle_list)
            avg = candles_obj.get_avg(num_of_candles - avg_interval, num_of_candles)
            stdev = candles_obj.get_std(num_of_candles - avg_interval, num_of_candles)

            if side == 'c1':

                buy_price = avg + stdev * buy_th

                current_order = self.buy(self.mkt_symbol, quantity, buy_price)

                # some error handling should go here (insufficient funds, etc)

                elapsed_time = 0

                time.sleep(sleep_interval)
                elapsed_time += sleep_interval
                
                while not current_order.is_filled():

                    if elapsed_time > time_to_reset:
                        # there should be some error handling here since ordery may be partially filled
                        current_order.cancel()
                        continue

                    time.sleep(sleep_interval)
                    elapsed_time += sleep_interval
                    
                side = 'c2'
                continue

            if side == 'c2':
                
                sell_price = avg + stdev * sell_th

                current_order = self.sell(self.mkt_symbol, quantity, sell_price)

                # some error handling should go here

                elapsed_time = 0

                time.sleep(sleep_interval)
                elapsed_time += sleep_interval

                while not current_order.is_filled():

                    if elapsed_time> time_to_reset:
                        # there should be some error handling here since ordery may be partially filled      
                        current_order.cancel()
                        continue

                    time.sleep(sleep_interval)
                    elapsed_time += sleep_interval

                side = 'c1'
                continue


