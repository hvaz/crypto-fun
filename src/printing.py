import colorama
from utils import active_internet
from candles import NUM_CANDLES 


def print_comparing_hold(info, profit, hold_profit):
    colorama.init()
    try:
        
        if profit == None:
            print colorama.Fore.MAGENTA + info

        elif profit == 0:
            print colorama.Fore.YELLOW + info

        elif profit > hold_profit:
            print colorama.Fore.GREEN + info

        elif profit == hold_profit:
            print colorama.Fore.CYAN + info

        elif profit < hold_profit:
            print colorama.Fore.RED + info

        else:
            print colorama.Fore.MAGENTA + info

    except Exception as e:
        print e

    finally:
        print colorama.Fore.RESET
        colorama.deinit()


def print_env_info(args):
    print "\n\n" + "*" * 100 + "\n"

    print "------ TEST ENVIRONMENT INFO ------\n"

    if not active_internet():
        print "Internet connection seems to be OFFLINE. Tests will use the candle data available offline\n"
    else:
        print "Internet connection is ACTIVE. Test using most up to date candles data\n"

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

    print "-----> sandbox_params = " + ", ".join(args["sandbox_params"])

    print "\n" + "*" * 100  + "\n\n"


def print_model_results(profits, args):
    dots = "." * 11
    arrows = ">" * 10
    print "\nvvvvvvvvvvvv RESULTS vvvvvvvvvvvvvv"
    for x, mkts_profits in profits.items():
        
        print "\n" + "x" * 100 +  "\n"
        print "---> Exchange: {}\n".format(x)
        print "\n" + "." * 100 +  "\n"

        for mkt, strat_profits in mkts_profits.items():
            hold_profit = strat_profits["hold"]
            print arrows + " Market: {} / {}\n".format(mkt, x)

            for strat_name, profit in strat_profits.items():
                if strat_name == "stat":
                    print_info = "Strategy: stat updating={} ".format(args["updating_stat"]) + dots + \
                                 " Profit: {}".format(profit)
                else:
                    print_info = "Strategy: {} ".format(strat_name) + dots * 2 + "..." + \
                                 " Profit: {}".format(profit)

                print_comparing_hold(print_info, profit, hold_profit)

            print "." * 100 +  "\n"

        print "\n"+ "x" * 100 + "\n\n"
