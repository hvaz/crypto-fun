import argparse
from exchanges import Exchange
from infos import info_exchanges, strategies

parser = argparse.ArgumentParser(description="Executing trading strategies for different crypto exchanges")

parser.add_argument("--exchanges", metavar="EXCHANGES", type=str, nargs="+", help="List of exchanges to be used")

parser.add_argument("--markets", metavar="MARKETS", type=str, nargs="+", help="List of market's symbols in which to test model")

parser.add_argument("--strategy", metavar="STRATEGY", type=str, nargs=1, help="Strategy to be tested. Options: [ema]")

args = parser.parse_args()

exchange_list = [x.lower() for x in args.exchanges]
markets_list = [m.upper() for m in args.markets]

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


## instantiate exchanges and update candles
exchange_objs = []
for x in exchange_list:
    exchange_info = info_exchanges[x]
    new_exchange = Exchange(exchange_info)
    exchange_objs.append(new_exchange)

    for m in markets_list:
        new_exchange.update_candles(m, 1, 'minute')
