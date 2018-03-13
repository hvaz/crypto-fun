import colorama

def print_comparing_hold(info, profit, hold_profit):
    colorama.init()
    try:
        if (profit == 0):
            print colorama.Fore.YELLOW + info

        elif profit >= hold_profit:
            print colorama.Fore.GREEN + info

        else:
            print colorama.Fore.RED + info

    except Exception as e:
        print e

    finally:
        print colorama.Fore.RESET
        colorama.deinit()
