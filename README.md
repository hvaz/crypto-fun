# crypto-fun

## Dependencies

```
pip install requests
```

## Running

```
python test_routine.py -h

➜  src git:(master) python test_routine.py -h
usage: test_routine.py [-h] [--exchanges EXCHANGES [EXCHANGES ...]]
                       [--markets MARKETS [MARKETS ...]]
                       [--candles_m_size CANDLES_M_SIZE]
                       [--candles_m_unit CANDLES_M_UNIT] --strategy STRATEGY
                       [--start START] [--end END] --calib_proportion
                       CALIB_PROPORTION [--updating_stat UPDATING_STAT]
                       [--ema_short EMA_SHORT_FACTOR]
                       [--ema_long EMA_LONG_FACTOR]
                       [--ema_threshold EMA_THREASHOLD]
                       [--stat_buy_th STAT_BUY_TH]
                       [--stat_sell_th STAT_SELL_TH]

Executing trading strategies for different crypto exchanges

optional arguments:
  -h, --help            show this help message and exit
  --exchanges EXCHANGES [EXCHANGES ...]
                        List of exchanges to be used. Default value is list of
                        all exchanges
  --markets MARKETS [MARKETS ...]
                        List of market's symbols in which to test model.
                        Default covers all defined markets for each exchange
  --candles_m_size CANDLES_M_SIZE
                        Candles m parameter's size used to determine their
                        chronological extension. Check infos.py file for
                        options. Default value is 3
  --candles_m_unit CANDLES_M_UNIT
                        Candles m parameter's unit used to determine their
                        chronological extension: Check infos.py file for
                        options. Default value is minute
  --strategy STRATEGY   Strategy to be tested. Options: ['ema', 'stat']
  --start START         Index of candle from which to start executing
                        strategy. Default value is 10
  --end END             Index of candle in which to stop executing strategy.
                        Default value is 950
  --calib_proportion CALIB_PROPORTION
                        Calibration rate to be passed to test_stat and
                        test_hold
  --updating_stat UPDATING_STAT
                        Parameter to indicate whether stat strategy should
                        update parameters often or not. Default value is TRUE
  --ema_short EMA_SHORT_FACTOR
                        Parameter indicating short_factor parameter to be
                        passed to test_ema
  --ema_long EMA_LONG_FACTOR
                        Parameter indicating long_factor parameter to be
                        passed to test_ema
  --ema_threshold EMA_THREASHOLD
                        Parameter indicating threashold parameter to be passed
                        to test_ema
  --stat_buy_th STAT_BUY_TH
                        Parameter indicating buy_th parameter to be passed to
                        test_stat (negative number!)
  --stat_sell_th STAT_SELL_TH
                        Parameter indicating sell_th parameter to be passed to
                        test_stat (positive number!)
```
