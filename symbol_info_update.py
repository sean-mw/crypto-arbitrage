import time

from binance_api import get_raw_tickers, get_symbol_info
from symbol_info_util import save_symbol_info


get_info_delay = 0.3


def update_symbol_info():
    symbols = {}
    tickers = get_raw_tickers()

    for ticker in tickers:
        symbol_info = get_symbol_info(ticker['symbol'])
        trading = (symbol_info['status'] == 'TRADING') and symbol_info['isSpotTradingAllowed']
        symbols[ticker['symbol']] = {'base': symbol_info['baseAsset'], 
                                     'target': symbol_info['quoteAsset'], 
                                     'trading': trading,
                                     'base_precision': symbol_info['baseAssetPrecision'],
                                     'step_size': symbol_info['filters'][2]['stepSize']}
        time.sleep(get_info_delay)
    
    save_symbol_info(symbols)


if __name__ == '__main__':
    update_symbol_info()
