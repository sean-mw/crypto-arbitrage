from binance_api import buy, sell, client_get_price, transaction_fee

from symbol_info_util import get_all_symbols


def test_path(path):
    symbols = get_all_symbols()
    balance = 1
    for idx in range(len(path) - 1):
        if path[idx] + path[idx+1] in symbols:
            price = float(client_get_price(path[idx] + path[idx+1])['bidPrice'])
        else:
            price = 1.0 / float(client_get_price(path[idx+1] + path[idx])['askPrice'])
        balance *= price
        balance -= balance * transaction_fee
    return (balance - 1) * 100



def convert_currency(balance, cur_from, cur_to):
    symbols = get_all_symbols()
    if cur_from + cur_to in symbols:
        symbol = cur_from + cur_to
        return sell(symbol, balance)
    else:
        symbol = cur_to + cur_from
        return buy(symbol, balance)


def calculate_pct_return(prices):
    pct_return = 1
    for price in prices:
        pct_return *= price
        pct_return -= pct_return * transaction_fee
    pct_return -= 1
    pct_return *= 100
    return pct_return


def buy_path(path, balance):
    executed_prices = []

    for idx in range(len(path) - 1):
        balance, avg_executed_price = convert_currency(balance, path[idx], path[idx+1])
        executed_prices.append(avg_executed_price)

    return calculate_pct_return(executed_prices)
