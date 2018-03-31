import logging
from collections import defaultdict
from markets import Market
from ccxt_exchanges import ccxtExchange
from parser import set_parser, handle_args
from printing import print_comparing_hold, print_env_info, print_model_results
from models_manager import TestManager
from sandbox import SandboxManager


def run_model(strategy, exchange_name, portfolio, candles_magnitude, args):
    mkt_symbol_profit = {}
    test_manager = None
    try:
        if strategy == "sandbox":
            test_manager = SandboxManager(exchange_name, portfolio, candles_magnitude)
        else:
            test_manager = TestManager(exchange_name, portfolio, candles_magnitude, strategy)
    except:
        raise
    else:
        mkt_obj_profit = test_manager.apply_model_to_portfolio(args)
        mkt_symbol_profit = {mkt_obj.symbol : prf for mkt_obj, prf in mkt_obj_profit.items()}
        return mkt_symbol_profit


def start_testing(args):
    ## instantiate exchanges, update candles, and run strategy
    profits = defaultdict(dict)
    for x in args["exchanges"]:
        new_exchange = ccxtExchange(x)
        portfolio = [Market(m, new_exchange) for m in args["markets"][x]]
        new_exchange.markets = {mkt_obj.symbol : mkt_obj for mkt_obj in portfolio}
        candles_magnitude = new_exchange.get_ccxt_candles_magnitude_format(args["candles_m_size"], args["candles_m_unit"])
        
        ## run real strategy
        strat_profits = run_model(args["strategy"], x, portfolio, candles_magnitude, args)

        ## run benchmark strategy (holding)
        hold_profits = run_model("hold", x, portfolio, candles_magnitude, args)

        ## run study stats (it does not return anything)
        run_model("study_stats", x, portfolio, candles_magnitude, args)

        exchange_profits = {mkt: {args["strategy"]: strat_prf, "hold": hold_profits[mkt]} \
                            for mkt, strat_prf in \
                            zip(strat_profits.keys(), strat_profits.values())}

        profits[x] = exchange_profits
        
    return profits


def init_routine():
    parser = set_parser()
    args = vars(parser.parse_args())
    handle_args(args)

    profits = start_testing(args)
    print_env_info(args)
    print_model_results(profits, args)


init_routine()
