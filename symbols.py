class symbol(object):

    def __init__(self, name):

        self.name = name

    def get_candles(self, factor, unit):

        if (unit not in ['s', 'm', 'h', 'd']):

            raise "Invalid unit for candles!"
            return

        :
