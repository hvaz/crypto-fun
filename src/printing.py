import colorama

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
