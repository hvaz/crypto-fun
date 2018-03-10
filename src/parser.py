import argparse
from infos import info_exchanges, strategies


def set_parser():
    parser = argparse.ArgumentParser(description="Executing trading strategies for different crypto exchanges")

    parser.add_argument("--exchanges", metavar="EXCHANGES", type=str, nargs="+", \
            help="List of exchanges to be used. Default value is list of all exchanges")

    parser.add_argument("--markets", metavar="MARKETS", type=str, nargs="+", \
            help="List of market's symbols in which to test model. Default covers all defined markets for each exchange")

    parser.add_argument("--candles_m_size", metavar="CANDLES_M_SIZE", type=int, nargs=1, default=3, \
            help="Candles m parameter's size used to determine their chronological extension. Check infos.py file for options. Default value is 3")

    parser.add_argument("--candles_m_unit", metavar="CANDLES_M_UNIT", type=str, nargs=1, default="minute", \
            help="Candles m parameter's unit used to determine their chronological extension: Check infos.py file for options. Default value is minute")

    parser.add_argument("--strategy", metavar="STRATEGY", type=str, nargs=1, choices=strategies, \
            help="Strategy to be tested")

    parser.add_argument("--start", metavar="START", type=int, nargs=1, default=10, \
            help="Index of candle from which to start executing strategy. Default value is 10")

    parser.add_argument("--end", metavar="END", type=int, nargs=1, default=950, \
            help="Index of candle in which to stop executing strategy. Default value is 950")

    parser.add_argument("--calib_proportion", metavar="CALIB_PROPORTION", type=float, nargs=1, default=0.2, \
            help="Calibration rate to be passed to test_stat and test_hold")

    parser.add_argument("--updating_stat", metavar="UPDATING_STAT", type=bool, nargs=1, default=True, \
            help="Parameter to indicate whether stat strategy should update parameters often or not. Default value is TRUE")

    parser.add_argument("--ema_short", metavar="EMA_SHORT_FACTOR", type=float, nargs=1, \
            help="Parameter indicating short_factor parameter to be passed to test_ema")

    parser.add_argument("--ema_long", metavar="EMA_LONG_FACTOR", type=float, nargs=1, \
            help="Parameter indicating long_factor parameter to be passed to test_ema")

    parser.add_argument("--ema_threshold", metavar="EMA_THREASHOLD", type=float, nargs=1, \
            help="Parameter indicating threashold parameter to be passed to test_ema")

    parser.add_argument("--stat_buy_th", metavar="STAT_BUY_TH", type=float, nargs=1, default=-2.0, \
            help="Parameter indicating buy_th parameter to be passed to test_stat (negative number!)")

    parser.add_argument("--stat_sell_th", metavar="STAT_SELL_TH", type=float, nargs=1, default=2.0, \
            help="Parameter indicating sell_th parameter to be passed to test_stat (positive number!)")

    return parser


def format_args(args):
    for a in args:
        if a == "exchanges":
            args[a] = info_exchanges.keys() if args["exchanges"] == None \
                      else [x.lower() for x in args["exchanges"]]
                              
        elif a != "markets":
                val = args[a]
                if type(val) == list and len(val) == 1:
                    args[a] = val[0]

    if args["strategy"] == "ema":
        args["calib_proportion"] = 0.0

    ## format markets argument
    mkts_list = None if args["markets"] == None else [m.upper() for m in args["markets"]]
    args["markets"] = {x: mkts_list if mkts_list != None else info_exchanges[x]["symbols"] \
                       for x in args["exchanges"]}

def check_args(args):
    for e in ["exchanges", "markets"]:
        assert(e in args.keys()), "Invalid set of arguments. It does not the contain element '{}'".format(e)

    for x in args["exchanges"]:
        exchange = info_exchanges[x]
        for m in args["markets"][x]:
            assert(m in exchange["symbols"]), "'{}' market not yet supported by exchange '{}' in our system. Please try again.".format(m, x)


def handle_args(args):
    format_args(args)
    check_args(args)
