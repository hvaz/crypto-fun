import ccxt
import argparse
from infos import strategies, candle_units


def set_parser():
    parser = argparse.ArgumentParser(description="Executing trading strategies for different crypto exchanges")

    parser.add_argument("--exchanges", metavar="EXCHANGES", type=str, nargs="+", default=['hitbtc2', 'binance'], \
            help="List of exchanges to be used. Default value is list of all exchanges")

    parser.add_argument("--markets", metavar="MARKETS", type=str, nargs="+", default=['ETH/BTC', 'TRX/BTC'], \
            help="List of market's symbols in which to test model. Default covers all defined markets for each exchange")

    parser.add_argument("--candles_m_size", metavar="CANDLES_M_SIZE", type=int, nargs=1, default=3, \
            help="Candles m parameter's size used to determine their chronological extension. Check infos.py file for options. Default value is 3")

    parser.add_argument("--candles_m_unit", metavar="CANDLES_M_UNIT", type=str, nargs=1, default="minute", \
            choices=candle_units.keys(), help="Candles m parameter's unit used to determine their chronological extension: Check infos.py file for options. Default value is minute")

    parser.add_argument("--strategy", metavar="STRATEGY", type=str, nargs=1, choices=strategies, required=True,\
            help="Strategy to be tested")

    parser.add_argument("--start", metavar="START", type=int, nargs=1, default=10, \
            help="Index of candle from which to start executing strategy. Default is 10")

    parser.add_argument("--end", metavar="END", type=int, nargs=1, default=950, \
            help="Index of candle in which to stop executing strategy. Default is 950")

    parser.add_argument("--calib_proportion", metavar="CALIB_PROPORTION", type=float, nargs=1, default=0.2, \
            help="Calibration rate to be passed to test_stat and test_hold. Default is 0.2")

    parser.add_argument("--updating_stat", metavar="UPDATING_STAT", type=bool, nargs=1, default=True, \
            help="Parameter to indicate whether stat strategy should update parameters often or not. Default is TRUE")

    parser.add_argument("--ema_short", metavar="EMA_SHORT_FACTOR", type=float, nargs=1, default=0.2, \
            help="Parameter indicating short_factor parameter to be passed to test_ema. Default is 0.2")

    parser.add_argument("--ema_long", metavar="EMA_LONG_FACTOR", type=float, nargs=1, default = 0.7, \
            help="Parameter indicating long_factor parameter to be passed to test_ema. Default is 0.7")

    parser.add_argument("--ema_threshold", metavar="EMA_THREASHOLD", type=float, nargs=1, default=0.001, \
            help="Parameter indicating threashold parameter to be passed to test_ema. Default is 0.001")

    parser.add_argument("--stat_buy_th", metavar="STAT_BUY_TH", type=float, nargs=1, default=-2.0, \
            help="Parameter indicating buy_th parameter to be passed to test_stat (negative number!). Default is -2.0")

    parser.add_argument("--stat_sell_th", metavar="STAT_SELL_TH", type=float, nargs=1, default=2.0, \
            help="Parameter indicating sell_th parameter to be passed to test_stat (positive number!). Default is +2.0")

    parser.add_argument("--sandbox_params", metavar="SANDBOX_PARAMS", nargs="+", \
            help="Parameters to be passed to sandbox model")

    return parser


def format_args(args):
    for a in args:
        if a == "exchanges":
            args[a] = [x.lower() for x in args["exchanges"]]
                              
        elif a != "markets":
            val = args[a]
            if type(val) == list and len(val) == 1:
                args[a] = val[0]
            elif val == None:
                args[a] = []

    if args["strategy"] == "ema":
        args["calib_proportion"] = 0.0

    ## format markets argument
    mkts_list = None if args["markets"] == None else [m.upper() for m in args["markets"]]
    args["markets"] = {x: mkts_list for x in args["exchanges"]}


def check_args(args):
    for x in args["exchanges"]:
        if x not in ccxt.exchanges:
            msg = "{} exchange is not supported. Please check ccxt.exchanges for supported exchanges".format(x)
            raise Exception(msg)


def handle_args(args):
    format_args(args)
    check_args
