from exchanges import Exchange, NUM_CANDLES
from infos import info_exchanges, strategies
from parser import set_parser, handle_args 

def print_env_info(args):
    print "\n\n" + "*" * 100 + "\n"

    print "------ TEST ENVIRONMENT INFO ------\n"

    print "*** Sample size: {} candles ***\n"\
            .format(NUM_CANDLES)

    print "*** Arguments *** \n"

    print "-----> strategy = {}"\
            .format(args["strategy"])

    print "-----> exchanges = {}"\
            .format(args["exchanges"])

    print "-----> markets = {}"\
            .format(args["markets"])

    print "-----> (candles_m_size, candles_m_unit) = ({}, {})"\
            .format(args["candles_m_size"], args["candles_m_unit"])

    print "-----> (start, end) = ({}, {})"\
            .format(args["start"], args["end"])

    print "-----> calib_proportion = {}"\
            .format(args["calib_proportion"])

    print "-----> (stat_buy_th, stat_sell_th, updating_stat) = ({}, {}, {})"\
            .format(args["stat_buy_th"], args["stat_sell_th"], args["updating_stat"])

    print "-----> (ema_short, ema_long, ema_threshold) = ({}, {}, {})"\
            .format(args["ema_short"], args["ema_long"], args["ema_threshold"])

    print "\n" + "*" * 100  + "\n\n"


def print_model_results(profits, args):
    dots = "." * 11
    arrows = ">" * 10
    print "\nvvvvvvvvvvvv RESULTS vvvvvvvvvvvvvv"
    ## print results
    for x, mkts_profits in profits.items():
        
        print "\n" + "x" * 100 +  "\n"
        print "---> Exchange: {}\n".format(x)

        for mkt, strat_profits in mkts_profits.items():
            for strat_name, profit in strat_profits.items():
                if strat_name == "stat":
                    print arrows + " Market: {} ".format(mkt) + dots + \
                            " Strategy: stat updating={} ".format(args["updating_stat"]) + dots + " Profit: {}".format(profit)
                else:
                    print arrows + " Market: {} ".format(mkt) + dots + " Strategy: {} ".format(strat_name) + \
                          dots * 2 + "..." + " Profit: {}".format(profit)
            
            print "\n" + "." * 100 +  "\n"

        print "\n"+ "x" * 100 + "\n\n"


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
            
            mkt_strategy_profit = 0
            cur_candles = mkt.candles[interval]
            if (args["strategy"] == "ema"):
                mkt_strategy_profit = mkt.test_ema_model(cur_candles, start, end, ema_short, ema_long, ema_threshold)

            elif (args["strategy"] == "stat"):
                mkt_strategy_profit = mkt.test_stat_model(cur_candles, args["start"], args["end"], args["stat_buy_th"], \
                                      args["stat_sell_th"], args["calib_proportion"], updating=args["updating_stat"])[0]

            elif (args["strategy"] == "sandbox"):
                mkt_strategy_profit = mkt.test_sandbox_model(sandbox_params)
            
            exchange_profits[m] = {}
            mkt_profits = exchange_profits[m]
            mkt_profits[args["strategy"]] = mkt_strategy_profit
            
            ## run benckmark strategy (holding)
            hold_profit = mkt.test_hold_model(cur_candles, args["start"], args["end"], args["calib_proportion"])
            mkt_profits["hold"] = hold_profit

            mkt.study_stats(cur_candles, args["start"], args["end"], args["calib_proportion"], \
                            updating=args["updating_stat"])

    return profits


def init_routine():
    parser = set_parser()
    args = vars(parser.parse_args())
    handle_args(args)

    profits = start_testing(args)
    print_env_info(args)
    print_model_results(profits, args)


init_routine()
