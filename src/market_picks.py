import ccxt
import json

# top 20 volume exchanges supported by ccxt
# poloniex should be here but not working

exchanges = ['binance', 'bitfinex', 'huobi', 'okex', 'bithumb', 'kraken', 'gdax', 'bitstamp', 'bitflyer', 'bittrex', 'hitbtc2', 'bitz', 'gemini', 'lbank', 'coinone', 'bitbank', 'wex']

# top 50 market cap coins

top50mc = ['BTC', 'ETH', 'XRP', 'BCH', 'LTC', 'EOS', 'ADA', 'XLM', 'NEO', 'MIOTA', 'XMR', 'TRX', 'DASH', 'USDT', 'XEM', 'ETC', 'QTUM', 'VEN', 'BNB', 'ICX', 'OMG', 'LSK', 'BTG', 'NANO', 'ZEC', 'ONT', 'XVG', 'BTM', 'DGD', 'PPT', 'STEEM', 'BCN', 'AE', 'STRAT', 'WAVES', 'SC', 'RHOC', 'BCD', 'BTS', 'DOGE', 'MKR', 'SNT', 'REP', 'ZIL', 'DCR', 'ZRX', 'WTC', 'VERI', 'KMD', 'HSR']

# top 50 volume coins

top50vol = ['BTC', 'USDT', 'ETH', 'EOS', 'XRP', 'LTC', 'BCH', 'TRX', 'ETC', 'STORM', 'HT', 'NEO', 'ADA', 'QTUM', 'DASH', 'ICX', 'BNB', 'ONT', 'IOST', 'ATMC', 'ZEC', 'VEN', 'XMR', 'XLM', 'MIOTA', 'OMG', 'ABT', 'XEM', 'SNT', 'BTM', 'MITH', 'LSK', 'QLC', 'OCN', 'CMT', 'ELF', 'WAVES', 'XVG', 'HSR', 'BTG', 'NANO', 'ELA', 'DGD', 'MEE', 'ZIL', 'NCASH', 'NAS', 'BITCNY', 'WAN', 'BTS']

# handpicked coins (mainly some sketchy high volume hitbtc coins)

handpicks = ['NOAH', 'XDN', 'W3C','ARDR', 'MAID', 'ORME', 'EMC', 'SCC', 'SENT']

# unique coins appearing in any of the previous categories:

uniquecoins = list(set(top50mc + top50vol + handpicks))



# base currencies

bases = ['USD', 'EUR', 'KRW', 'JPY', 'USDT', 'BTC', 'ETH']


# all possible coin/base pairs between the previous

pairs = []
for x in uniquecoins:
    for y in bases:
        pairs.append(x+"/"+y)



pair_in_exchange = []

for e in exchanges:
    s = "ex = ccxt." + e + "()"
    exec(s)
    ex_mkts = ex.load_markets()
    for p in pairs:
        if p in ex_mkts:
            pair_in_exchange.append((p, e))
            

file_object  = open("market_picks.txt", "w")
json_string = json.dumps(pair_in_exchange)
file_object.write(json_string)
file_object.close() 

print("Total number of markets:")
print(len(pair_in_exchange))

