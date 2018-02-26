"""
Candles consist of a list of candles obeying to the following format:

[
  {
    "timestamp": "2017-10-20T20:00:00.000Z",
    "open": "0.050459",
    "close": "0.050087",
    "min": "0.050000",
    "max": "0.050511",
    "volume": "1326.628",
    "volumeQuote": "66.555987736"
  },
  {
    "timestamp": "2017-10-20T20:30:00.000Z",
    "open": "0.050108",
    "close": "0.050139",
    "min": "0.050068",
    "max": "0.050223",
    "volume": "87.515",
    "volumeQuote": "4.386062831"
  }
]

OBS: Data is returned in ascending order. Oldest first, newest last.
"""

class candles(object):

    def __init__(self, factor, unit):

        self.factor = factor
        self.unit = unit


    def get_ema(factor, unit, at):
        """
        factor: size of EMA, positive integer
        unit: s, m, h, d (seconds, minutes, hours, days)
        at: timestamp indicating which EMA to calculate

        return value: ?
        """

        pass
