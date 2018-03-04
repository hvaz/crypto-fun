import argparse
from exchanges import Exchange
from infos import info_exchanges, strategies

parser = argparse.ArgumentParser(description="Executing trading strategies for different crypto exchanges")

parser.add_argument("--exchanges", metavar="EXCHANGES", type=str, nargs="+", help="List of exchanges to be used")

parser.add_argument("--markets", metavar="MARKETS", type=str, nargs="+", help="List of market's symbols in which to test model")

parser.add_argument("--candles_m_size", metavar="CANDLES_M_SIZE", type=int, nargs=1, help="Candles m parameter's size used to determine their chronological extension. Check infos.py file for options")

parser.add_argument("--candles_m_unit", metavar="CANDLES_M_UNIT", type=str, nargs=1, help="Candles m parameter's unit used to determine their chronological extension: Check infos.py file for options")

parser.add_argument("--strategy", metavar="STRATEGY", type=str, nargs=1, help="Strategy to be tested. Options: {}".format(strategies))

args = parser.parse_args()

exchange_list = [x.lower() for x in args.exchanges]
markets_list = [m.upper() for m in args.markets]
m_size = args.candles_m_size[0]
m_unit = args.candles_m_unit[0]
strategy = args.strategy[0]

## check if arguments make sense
if args.strategy[0] not in strategies:
    raise Exception("There is no implemented strategy named {}".format(args.strategy[0]))

for x in exchange_list:
    if x not in info_exchanges.keys():
        raise Exception("{} exchange not yet supported in our system. Please try again".format(x))

    exchange = info_exchanges[x]
    for m in markets_list:
        if m not in exchange["symbols"]:
            raise Exception("{} market not yet supported by exchange {} in our system. Please try again.".format(x, m))


profits = {}
## instantiate exchanges and update candles
exchange_objs = []
for x in exchange_list:
    exchange_info = info_exchanges[x]
    new_exchange = Exchange(exchange_info)
    exchange_objs.append(new_exchange)
    profits[x] = {}
    exchange_profits = profits[x]

    for m in markets_list:
        new_exchange.update_candles(m, m_size, m_unit)
        interval = new_exchange.format_interval(m_size, m_unit)
        mkt = new_exchange.markets[m]
        
        mkt_profit = 0
        cur_candles = mkt.candles[interval]
        if (strategy == "ema"):
            mkt_profit = mkt.test_ema_model(cur_candles, 10, 400, 0.1, 0.7, 0.0001)

        elif (strategy == "stat"):
            mkt_profit = mkt.test_stat_model(cur_candles, 10, 400, -2, 1)
    
        exchange_profits[m] = mkt_profit

## print results
print "Results for strategy {}\n\n".format(strategy)

for x, mkts in profits.items():
    print "---> Exchange: {}\n".format(x)

    for mkt, profit in mkts.items():
        print "---------> Market: {} ........... Profit: {}".format(mkt, profit)

    print "\n\n\n"
