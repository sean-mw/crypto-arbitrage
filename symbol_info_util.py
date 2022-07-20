import os
import json


symbols = None
symbol_info = None


def get_all_symbols():
    global symbols
    if symbols is None:
        symbols = [remove_suffix(i, '.json') for i in os.listdir('data/prices')]
    return symbols


def save_symbol_info(data):
    with open('data/symbol_info/symbols.json', 'w') as f:
        json.dump(data, f)


def get_symbol_info(symbol):
    global symbol_info
    if symbol_info is None:
        with open('data/symbol_info/symbols.json', 'r') as f:
            symbol_info = json.load(f)
    try:
        return symbol_info[symbol]
    except KeyError:
        return None


def remove_suffix(input_string, suffix):
    if suffix and input_string.endswith(suffix):
        return input_string[:-len(suffix)]
    return input_string
