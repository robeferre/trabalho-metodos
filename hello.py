from binance.client import Client
import pdb
import pandas as pd

client = Client('1gqQOhuF5q1WG0FQqnAXZ8m5upxlM8ZhYZ9X0J7M2gjWrud4JsJku9mOKm3FthN0',
                '2yKgN17XMwyKw7K5S0qMeqbNhaNmy9ljtXQmonVdr8N3LCQ5DLzL4Cu3iTzV56P3')



from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json

url = 'https://sandbox.coinmarketcap.com/v1/exchange/quotes/historical?id=270&time_start=2018-01-01&time_end=2018-05-01&interval=30d&count=12'
parameters = {
  'convert' :'USD'
}

headers = {
  'Accepts': 'application/json',
  'X-CMC_PRO_API_KEY': '863804bc-ebab-43c2-a99b-e32138a49183',
}

session = Session()
session.headers.update(headers)

try:
  response = session.get(url, params=parameters)
  data = json.loads(response.text)
  print(data)
except (ConnectionError, Timeout, TooManyRedirects) as e:
  print(e)



pdb.set_trace()


# get all symbol prices
tickers = pd.read_json("https://sandbox.coinmarketcap.com/v1/exchange/quotes/historical?id=270&time_start=2018-01-01&time_end=2018-05-01&interval=30d&count=12")
df = pd.DataFrame(tickers)
df = df.set_index("id")



market_cap_raw = df[['id', 'market_cap_usd']]

print(market_cap_raw.count())


cap = market_cap_raw.query('market_cap_usd > 0')

# Counting the number of values again

print(cap.count())


#Declaring these now for later use in the plots
TOP_CAP_TITLE = 'Top 10 market capitalization'
TOP_CAP_YLABEL = '% of total cap'

# Selecting the first 10 rows and setting the index
cap10 = cap[0:10].set_index("id")

# Calculating market_cap_perc
cap10 = cap10.assign(market_cap_perc =
    lambda x: (x.market_cap_usd / cap.market_cap_usd.sum()) * 100)

# Plotting the barplot with the title defined above
ax = cap10.plot.bar(title=TOP_CAP_TITLE  ) # withdraw 100 ETH
# check docs for assumptions around withdrawals
# from binance.exceptions import BinanceAPIException, BinanceWithdrawException
# try:
#     result = client.withdraw(
#         asset='ETH',
#         address='<eth_address>',
#         amount=100)
# except BinanceAPIException as e:
#     print(e)
# except BinanceWithdrawException as e:
#     print(e)
# else:
#     print("Success")

# # fetch list of withdrawals
# withdraws = client.get_withdraw_history()
#
# # fetch list of ETH withdrawals
# eth_withdraws = client.get_withdraw_history(asset='ETH')

# get a deposit address for BTC
# address = client.get_deposit_address(asset='BTC')

# start aggregated trade websocket for BNBBTC
# def process_message(msg):
#     if msg['e'] == 'error':
#         # close and restart the socket
#     else:
#         # process message normally
#     print("message type: {}".format(msg['e']))
#     print(msg)
#     pdb.set_trace()
#     # do something
#
# from binance.websockets import BinanceSocketManager
# bm = BinanceSocketManager(client)
# bm.start_aggtrade_socket('BNBBTC', process_message)
# bm.start()
# #
#
# # klines = client.get_historical_klines("NEOBTC Client.KLINE_INTERVAL_1WEEK, "1 Jan, 2017")
# dfPrices = client.get_historical_klines("ALL",  Client.KLINE_INTERVAL_1WEEK, "1 Jan, 2017")
# df = pd.DataFrame(dfPrices)

# # get historical kline data from any date range
#
# # fetch 1 minute klines for the last day up until now
# klines = client.get_historical_klines("BNBBTC", Client.KLINE_INTERVAL_1MINUTE, "1 day ago UTC")
#
# # fetch 30 minute klines for the last month of 2017
# klines = client.get_historical_klines("ETHBTC", Client.KLINE_INTERVAL_30MINUTE, "1 Dec, 2017", "1 Jan, 2018")
#
# # fetch weekly klines since it listed
# klines = client.get_historical_klines("NEOBTC", Client.KLINE_INTERVAL_1WEEK, "1 Jan, 2017")
#
#
