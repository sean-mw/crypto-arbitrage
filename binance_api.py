from decimal import Decimal
from binance.spot import Spot as Client
from binance.error import ClientError

from symbol_info_util import get_symbol_info
from graph import get_price
from config import config


client = Client(config['key'], config['secret'], base_url='https://api.binance.com')

transaction_fee = 0.00075  # 0.001 if not holding BNB


def client_get_price(symbol):
    return client.book_ticker(symbol)


def round_step_size(quantity, step_size):
    quantity = Decimal(str(quantity))
    return float(quantity - quantity % Decimal(str(step_size)))


def format_quantity(qty, symbol):
    symbol_info = get_symbol_info(symbol)
    precision = int(symbol_info['base_precision'])
    step_size = float(symbol_info['step_size'])
    qty = float('{:0.0{}f}'.format(qty, precision))
    return round_step_size(qty, step_size)


def buy(symbol, qty):
    fills = buy_helper(symbol, qty)
    balance = sum([float(i['qty']) for i in fills])
    avg_executed_price = 1 / sum([(float(i['qty']) / balance) * float(i['price']) for i in fills])
    return balance, avg_executed_price


def sell(symbol, qty):
    fills = sell_helper(symbol, qty)
    balance = sum([float(i['qty']) * float(i['price']) for i in fills])
    avg_executed_price = sum([((float(i['qty']) * float(i['price'])) / balance) * float(i['price']) for i in fills])
    return balance, avg_executed_price


def buy_helper(symbol, qty):
    symbol_info = get_symbol_info(symbol)
    price = get_price(symbol_info['target'], symbol_info['base'])
    order_qty = qty * price
    order_qty = format_quantity(order_qty, symbol)
    try:
        order = place_order(symbol, order_qty, 'BUY')
    except ClientError as e:
        print(e)
        return buy_helper(symbol, qty)
    return order['fills']


def sell_helper(symbol, qty):
    order_qty = format_quantity(qty, symbol)
    order = place_order(symbol, order_qty, 'SELL')
    return order['fills']


def place_order(symbol, qty, side):
    params = {
        'symbol': symbol,
        'side': side,
        'type': 'MARKET',
        'quantity': qty,
    }
    return client.new_order(**params)
