import math
import networkx as nx
from threading import Lock

from symbol_info_util import get_symbol_info


G = nx.MultiDiGraph()
graph_mx = Lock()


transaction_fee = 0.00075  # change location of this global


def path_product(path):
    with graph_mx:
        cost = nx.path_weight(G, path, 'weight')
    product = math.e ** (-cost)
    return product


def get_price(base, target):
    weight = G.get_edge_data(base, target, key=0)['weight']
    price = (math.e ** (-weight)) / (1 - transaction_fee)
    return price


def find_negative_cycle(start):
    cycle = []
    with graph_mx:
        try:
            cycle = nx.find_negative_cycle(G, start)
        except (nx.exception.NetworkXError, nx.NodeNotFound):  
            pass  # No negative cycle found or start not in graph
    return cycle


def update_graph(symbol, price_info):
    symbol_info = get_symbol_info(symbol)
    if not symbol_info or not symbol_info['trading']: return

    with graph_mx:
        if not G.has_node(symbol_info['base']): 
            G.add_node(symbol_info['base'])
        if not G.has_node(symbol_info['target']): 
            G.add_node(symbol_info['target'])

        if G.has_edge(symbol_info['base'], symbol_info['target']):
            G.remove_edge(symbol_info['base'], symbol_info['target'])
        if G.has_edge(symbol_info['target'], symbol_info['base']):
            G.remove_edge(symbol_info['target'], symbol_info['base'])

        weight = -math.log(float(price_info['b']) * (1 - transaction_fee))
        G.add_edge(symbol_info['base'], symbol_info['target'], weight=weight)
        weight = -math.log(1 / float(price_info['a']) * (1 - transaction_fee))
        G.add_edge(symbol_info['target'], symbol_info['base'], weight=weight)
