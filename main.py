import time
from timeit import default_timer
from threading import Thread

from trade import buy_path, test_path
from graph import find_negative_cycle, path_product
from price_websocket import start_price_websocket
from config import config


def main():
    print('Starting main thread...')

    start = config['holding_currencies'][0]
    returns = []

    print('Searching for cycles...')
    while True:
        time.sleep(0.1)  # Yield to allow t_price thread to catch up
        cycle = find_negative_cycle(start)

        if cycle and cycle[0] in config['holding_currencies']:

            for i in cycle:
                if i in config['blacklist']:
                    continue

                print('Cycle found:', cycle)

                if config['live_trading']:
                    start_time = default_timer()
                    pct_return = buy_path(cycle, config['holding_balance'])
                    print('Time for buy path:', default_timer() - start_time)
                    returns.append(pct_return)
                    print('Pct return:', pct_return, '%')
                    est_pct_ret = (path_product(cycle) - 1) * 100
                    print('Estimated trade return (graph price):', est_pct_ret, '%')
                else:
                    start_time = default_timer()
                    est_pct_ret = test_path(cycle)
                    print('Time for test path:', default_timer() - start_time)
                    print('Estimated trade return (client price):', est_pct_ret, '%')
                    est_pct_ret = (path_product(cycle) - 1) * 100
                    returns.append(est_pct_ret)
                    print('Estimated trade return (graph price):', est_pct_ret, '%')

                print('Cumulative return from all trades:', sum(returns), '%')


if __name__ == '__main__':
    t_price = Thread(target=start_price_websocket)
    t_main = Thread(target=main)
    t_price.start()
    t_main.start()
    t_main.join()

