from exchanges import Exchange
from infos import info_exchanges, strategies
from parser import set_parser, handle_args
from printing import print_comparing_hold, print_env_info, print_model_results
import logging


def apply_model(strategy, args, mkt, interval):
    cur_candles = mkt.candles[interval]
    mkt_strategy_profit = 0
    try:
        if strategy == "ema":
            mkt_strategy_profit = mkt.test_ema_model(cur_candles, args["start"], args["end"], \
                                  args["ema_short"], args["ema_long"], args["ema_threshold"])

        elif strategy == "stat":
            mkt_strategy_profit = mkt.test_stat_model(cur_candles, args["start"], args["end"], args["stat_buy_th"], \
                                  args["stat_sell_th"], args["calib_proportion"], updating=args["updating_stat"])[0]

        elif strategy == "hold":
            mkt_strategy_profit = mkt.test_hold_model(cur_candles, args["start"], args["end"], args["calib_proportion"])

        elif strategy == "study_stats":
            mkt.study_stats(cur_candles, args["start"], args["end"], args["calib_proportion"], \
                            updating=args["updating_stat"])

        elif strategy == "sandbox":
            mkt_strategy_profit = mkt.test_sandbox_model(cur_candles, args["sandbox_params"])

    except Exception as e:
        raise e

    else:
        return mkt_strategy_profit


def start_testing(args):
    ## instantiate exchanges, update candles, and run strategy
    profits = {}
    exchange_objs = []
    for x in args["exchanges"]:
        exchange_info = info_exchanges[x]
        new_exchange = Exchange(exchange_info)
        exchange_objs.append(new_exchange)
        profits[x] = {}
        exchange_profits = profits[x]

        for m in args["markets"][x]:
            new_exchange.update_candles(m, args["candles_m_size"], args["candles_m_unit"])
            interval = new_exchange.format_interval(args["candles_m_size"], args["candles_m_unit"])
            mkt = new_exchange.markets[m]
            
            exchange_profits[m] = {}
            mkt_profits = exchange_profits[m]
            mkt_profits[args["strategy"]] = apply_model(args["strategy"], args, mkt, interval)
            
            ## run benckmark strategy (holding)
            mkt_profits["hold"] = apply_model("hold", args, mkt, interval)
            study_stats = apply_model("study_stats", args, mkt, interval)

    return profits


def init_routine():
    parser = set_parser()
    args = vars(parser.parse_args())
    handle_args(args)

    profits = start_testing(args)
    print_env_info(args)
    print_model_results(profits, args)


init_routine()
