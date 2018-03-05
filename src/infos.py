info_exchanges = { \
    "binance": \
    { \
        "name": "binance", \
        "percentage_fee": 0.1, \
        "every_transaction_fee": True, \
        "api_endpoint": "https://api.binance.com", \
        "data_ascending": True, \
        "symbols": ["ETHBTC", "TRXBTC", "NANOBTC"], \
        "candles_endpoint": "/api/v1/klines", \
        "candles_intervals": {'minute': {1: '1m', 3: '3m', 5: '5m', 15: '15m', 30: '30m'}, \
                              'hour': {1: '1h', 2: '2h', 4: '4h', 6: '6h', 8: '8h', 12: '12h'}, \
                              'day': {1: '1d', 3: '3d'}, 'week': {1: '1w'}, 'month': {1: '1M'} \
                             } \
    }, \

    "hitbtc": \
    { \

        "name": "hitbtc", \
        "percentage_fee": 0.1, \
        "every_transaction_fee": True, \
        "api_endpoint": "https://api.hitbtc.com/api/2", \
        "data_ascending": True, \
        "symbols": ["ETHBTC", "TRXBTC", "BTCUSD", "MIPSBTC"], \
        "candles_endpoint": "/public/candles/{}", \
        "candles_intervals": {'minute': {1: 'M1', 3: 'M3', 5: 'M5', 15: 'M15', 30: 'M30'}, \
                              'hour': {1: 'H1', 4: 'H4'}, 'day': {1: 'D1', 7: 'D7'}, 'month': {1: '1M'} \
                             } \
    } \
}

strategies = [ \
    "ema", \
    "stat" \
]
