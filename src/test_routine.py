import argparse
from exchanges import Exchange, NUM_CANDLES
from infos import info_exchanges, strategies

parser = argparse.ArgumentParser(description="Executing trading strategies for different crypto exchanges")

parser.add_argument("--exchanges", metavar="EXCHANGES", type=str, nargs="+", help="List of exchanges to be used. Default value is list of all exchanges")

parser.add_argument("--markets", metavar="MARKETS", type=str, nargs="+", help="List of market's symbols in which to test model. Default covers all defined markets for each exchange")

parser.add_argument("--candles_m_size", metavar="CANDLES_M_SIZE", type=int, nargs=1, default=3, help="Candles m parameter's size used to determine their chronological extension. Check infos.py file for options. Default value is 3")

parser.add_argument("--candles_m_unit", metavar="CANDLES_M_UNIT", type=str, nargs=1, default="minute", help="Candles m parameter's unit used to determine their chronological extension: Check infos.py file for options. Default value is minute")

parser.add_argument("--strategy", metavar="STRATEGY", type=str, nargs=1, required=True, help="Strategy to be tested. Options: {}".format(strategies))

parser.add_argument("--start", metavar="START", type=int, nargs=1, default=10, help="Index of candle from which to start executing strategy. Default value is 10")

parser.add_argument("--end", metavar="END", type=int, nargs=1, default=950, help="Index of candle in which to stop executing strategy. Default value is 950")

parser.add_argument("--calib_proportion", metavar="CALIB_PROPORTION", required=True, type=float, nargs=1, help="Calibration rate to be passed to test_stat and test_hold")

parser.add_argument("--updating_stat", metavar="UPDATING_STAT", type=bool, nargs=1, default=True, help="Parameter to indicate whether stat strategy should update parameters often or not. Default value is TRUE")

parser.add_argument("--ema_short", metavar="EMA_SHORT_FACTOR", type=float, nargs=1, help="Parameter indicating short_factor parameter to be passed to test_ema")

parser.add_argument("--ema_long", metavar="EMA_LONG_FACTOR", type=float, nargs=1, help="Parameter indicating long_factor parameter to be passed to test_ema")

parser.add_argument("--ema_threshold", metavar="EMA_THREASHOLD", type=float, nargs=1, help="Parameter indicating threashold parameter to be passed to test_ema")

parser.add_argument("--stat_buy_th", metavar="STAT_BUY_TH", type=float, nargs=1, help="Parameter indicating buy_th parameter to be passed to test_stat (negative number!)")

parser.add_argument("--stat_sell_th", metavar="STAT_SELL_TH", type=float, nargs=1, help="Parameter indicating sell_th parameter to be passed to test_stat (positive number!)")

args = parser.parse_args()

exchange_list = info_exchanges.keys() if args.exchanges == None else [x.lower() for x in args.exchanges]
markets_list = None if args.markets == None else [m.upper() for m in args.markets]
m_size = args.candles_m_size[0] if type(args.candles_m_unit) == list else args.candles_m_size
m_unit = args.candles_m_unit[0] if type(args.candles_m_unit) == list  else args.candles_m_unit
strategy = args.strategy[0]
start = args.start[0] if type(args.start) == list else args.start
end = args.end[0] if type(args.end) == list else args.end
calib_proportion = args.calib_proportion[0]
updating_stat = args.updating_stat[0] if type(args.updating_stat) == list else args.updating_stat
ema_short = args.ema_short[0] if type(args.ema_short) == list else args.ema_short
ema_long = args.ema_long[0] if type(args.ema_long) == list else args.ema_long
ema_threshold = args.ema_threshold[0] if type(args.ema_threshold) == list else args.ema_threshold
stat_buy_th = args.stat_buy_th[0] if type(args.stat_buy_th) == list else args.stat_buy_th
stat_sell_th = args.stat_sell_th[0] if type(args.stat_sell_th) == list else args.stat_sell_th

test_mkts = {x: markets_list if markets_list != None else info_exchanges[x]["symbols"] \
            for x in exchange_list}

## check if arguments make sense
if args.strategy[0] not in strategies:
    raise Exception("There is no implemented strategy named {}".format(strategy))

for x in exchange_list:
    if x not in info_exchanges.keys():
        raise Exception("{} exchange not yet supported in our system. Please try again".format(x))

    exchange = info_exchanges[x]
    for m in test_mkts[x]:
        if m not in exchange["symbols"]:
            raise Exception("{} market not yet supported by exchange {} in our system. Please try again.".format(m, x))



## instantiate exchanges, update candles, and run strategy
profits = {}
exchange_objs = []
for x in exchange_list:
    exchange_info = info_exchanges[x]
    new_exchange = Exchange(exchange_info)
    exchange_objs.append(new_exchange)
    profits[x] = {}
    exchange_profits = profits[x]

    for m in test_mkts[x]:
        new_exchange.update_candles(m, m_size, m_unit)
        interval = new_exchange.format_interval(m_size, m_unit)
        mkt = new_exchange.markets[m]
        
        mkt_strategy_profit = 0
        cur_candles = mkt.candles[interval]
        if (strategy == "ema"):
            mkt_strategy_profit = mkt.test_ema_model(cur_candles, start, end, ema_short, ema_long, ema_threshold)

        elif (strategy == "stat"):
            mkt_strategy_profit = mkt.test_stat_model(cur_candles, start, end, stat_buy_th, stat_sell_th, calib_proportion, updating=updating_stat)
        
        exchange_profits[m] = {}
        mkt_profits = exchange_profits[m]
        mkt_profits[strategy] = mkt_strategy_profit
        
        ## run benckmark strategy (holding)
        hold_profit = mkt.test_hold_model(cur_candles, start, end, calib_proportion)
        mkt_profits["hold"] = hold_profit

	mkt.study_stats(cur_candles, start, end, calib_proportion, updating=updating_stat)

print "\n\n*** Sample size: {} candles ***\n\n".format(NUM_CANDLES)

## print results
for x, mkts_profits in profits.items():
    print "---> Exchange: {}\n".format(x)

    for mkt, strat_profits in mkts_profits.items():
        for strat_name, profit in strat_profits.items():

            if (strat_name == "stat"):

                if (updating_stat):
                    print "---------> Market: {} ........... Strategy: stat updating=True ............ Profit: {}".format(mkt, profit)

                else:
                    print "---------> Market: {} ........... Strategy: stat updating=False ............ Profit: {}".format(mkt, profit)


            else:
                print "---------> Market: {} ........... Strategy: {} ............ Profit: {}".format(mkt, strat_name, profit)


        print "\n"

    print "\n\n\n"
