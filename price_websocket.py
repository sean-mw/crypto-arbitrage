from binance.websocket.spot.websocket_client import SpotWebsocketClient as WebsocketClient
from graph import update_graph


def message_handler(message):
    try:
        symbol = message['s']
    except KeyError:
        return
    update_graph(symbol, message)


def start_price_websocket():
    ws_client = WebsocketClient()
    ws_client.start()
    ws_client.book_ticker(id=1, callback=message_handler)
