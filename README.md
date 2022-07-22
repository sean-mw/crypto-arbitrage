# Crypto Arbitrage
A Python crypto arbitrage bot. Uses the Binance API to fetch prices and execute orders. Uses NetworkX to create/update a graph and find negative cycles (using a modified Bellman-Ford algorithm).

NOTE: This bot is not profitable. Do not use this with the expectation of making money.

## Install / Setup
NOTE: Requires Python>=3.8 for NetworkX find_negative_cycle()

### Clone the Repo
```
git clone https://github.com/Sean-MW/crypto-arbitrage.git
```
### Create and Activate a Python Virtual Environment
```
cd crypto-arbitrage
python -m venv .venv
source .venv/bin/activate
```
### Install Dependencies
```
pip install -r requirements.txt
```
### Add Binance API keys
Modify "key" and "secret" in config.json.
```
{
"live_trading": false,
"holding_currencies": ["BUSD", "USDT"],
"holding_balance": 20,
"transaction_fee": 0.00075,
"blacklist": ["BTC", "ETH", "BTTC", "BIDR"],
"key": null,
"secret": null
}
```
#### OR
Create a .env file.
```
touch.env
```
Add key and secret.
```
key=<INSERT BINANCE API KEY HERE>
secret=<INSERT BINANCE SECRET KEY HERE>
```

## Getting Started

### Running the Bot
Start the bot by calling main.
```
python main.py
```
### Modifying Config.json
Other than key and secret, the config.json file has five modifiable variables: live_trading, holding_currencies, holding_balance, transaction_fee, blacklist.
#### Live Trading (WARNING: Expect to lose money)
By default this is set to false. Change it to true to if you wish to trade with real money. Ensure you are holding enough of each holding currency before doing so.

NOTE: The results you see while live_trading=false are not representative of the results you will see with live_trading=true.
#### Holding Currencies
These are the currencies that will always be at the start and end of each arbitrage cycle (e.g. holding currency -> currency 1 -> currency 2 -> holding currency). I would strongly suggest using stable coins here.
#### Holding Balance
This is how much of your holding currencies the bot will trade. Ensure that you have more than this amount worth of each of your holding currencies in your account before live trading.
#### Transaction Fee
This controls the fees charged while live_trading=false. For more information on fees see the [Binance fee schedule](https://www.binance.com/en/fee/schedule).
#### Blacklist
These are blacklisted currencies. If any of these currencies appear in a cycle, the bot will not make the trade.
