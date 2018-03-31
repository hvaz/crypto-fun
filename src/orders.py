import ccxt

class Order(object):

    def __init__(self, exchange_trader, order_id):
        self.owner = exchange_trader
        self.id = order_id


    def cancel(self):
        '''
            Cancel order identified by order_id

            order_id (str): id of order being canceled

            Return Value: https://github.com/ccxt/ccxt/wiki/Manual#exceptions-on-order-canceling
        '''

        canceled = False
        
        while not canceled:
            try:
                canceled = (self.status() == 'canceled')
                print self.status()
                self.owner.ccxt_obj.cancel_order(self.id)
            except Exception as e:
                print e
            

        try:
            self.owner.kill_order(self)
        except Exception as e:
            print e


    def full_info(self):
        '''
            Fetches complete information of an order. Synchronous.
            Not all exchanges support this method. Async option can be implemented

            order_id (str): id of order whose information is being fetched

            Return Value: dictionary as specified in https://github.com/ccxt/ccxt/wiki/Manual#order-structure
        '''
        
        order = None

        if self.owner.ccxt_obj.has['fetchOrder']:
            while order == None:
                try:
                    order = self.owner.ccxt_obj.fetch_order(self.id)
                except Exception as e:
                    print e
  
        return order


    def status(self):
        '''
            Determines order's status using full_order_info method
            
            order_id (str): id of order whose status is being checked

            Return Value: None, 'open', 'closed', or 'canceled'    
        '''
        status = None
        
        try:
            status = self.full_info()['status']
        except Exception as e:
            print e

        return status


    def is_filled(self):

        if self.status() == 'closed':
            return True
        else:
            return False
