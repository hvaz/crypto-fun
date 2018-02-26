intervals = ['1m', '3m', '5m', '15m', '30m', \
             '1h', '2h', '4h', '6h', '8h', '12h', \
             '1d', '3d', \
             '1w',
             '1M']

class Market(object):

    def __init__(self, name, percentage_fee):

        self.name = name
        self.fee = percentage_fee
        self.candles = {i:None for i in intervals}

