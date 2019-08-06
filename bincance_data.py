import matplotlib.pyplot as plt
import pandas as pd
from binance.client import Client
from sklearn import linear_model
import statsmodels.api as sm
import pdb

client = Client('1gqQOhuF5q1WG0FQqnAXZ8m5upxlM8ZhYZ9X0J7M2gjWrud4JsJku9mOKm3FthN0',
                '2yKgN17XMwyKw7K5S0qMeqbNhaNmy9ljtXQmonVdr8N3LCQ5DLzL4Cu3iTzV56P3')


def plot_graph(coin1df, coin2df, coin1_name, coin2_name):
    """
    Plota os graficos Coin1 x Coin2
    """
    marker_size = 0.2
    plt.locator_params(nbins=10)
    plt.scatter(coin2df[0:2000], coin1df[0:2000], marker_size, color='red')
    plt.title("%s Vs %s" % (coin1_name, coin2_name), fontsize=14)
    plt.xlabel("%s" % coin2_name, fontsize=14)
    plt.ylabel("%s" % coin1_name, fontsize=14)
    # plt.grid(True)
    plt.show()
    return None


def dataframe_cleanup(client):
    """
    Dataframe principal contendo 3 meses de dados do Binance.
    """

    # Pego quais sao as moedas terminas em USD
    prices = client.get_all_tickers()
    df = pd.DataFrame(prices)
    mask = df["symbol"].str.endswith('USD')
    listofcoins = df[mask].iloc[:, 1].to_list()

    cols = ['coin', 'opentime', 'open', 'high',
            'low', 'close', 'volume', 'close time',
            'quote asset volume', 'number of trades',
            'taker buy volume', 'taker buy quote vol', 'ignore']

    # Pego candle sticks de 30 mins
    df = pd.DataFrame()

    klines = []
    for coin in listofcoins[0:6]:
        data = client.get_historical_klines("%s" % coin, Client.KLINE_INTERVAL_30MINUTE, "13 Mar, 2019", "1 Jun, 2019")
        # Insiro a moeda no Dataframe
        for candle in data:
            candle.insert(0, "%s" % coin)
        klines.append(data)
        df = df.append(pd.DataFrame(data), ignore_index=True)
        print("%s" % coin + " DONE!")

    df.columns = cols
    # df.set_index(cols, drop=False, append=False, inplace=False, verify_integrity=True)

    df['opentime'] = df['opentime'].astype(str)
    date_times = pd.to_datetime(df['opentime'], unit='ms')

    return df.set_index(date_times), listofcoins


# DF CLEAN
df_clean, list_of_coins = dataframe_cleanup(client)
df_clean['opentime'] = pd.to_datetime(df_clean['opentime'], unit='ms')
df_clean.sort_index(inplace=True)

BTCTUSD = df_clean['open'].where(df_clean['coin'] == 'BTCTUSD').dropna()
ETHTUSD = df_clean['open'].where(df_clean['coin'] == 'ETHTUSD').dropna()
BNBTUSD = df_clean['open'].where(df_clean['coin'] == 'BNBTUSD').dropna()
XRPTUSD = df_clean['open'].where(df_clean['coin'] == 'XRPTUSD').dropna()
EOSTUSD = df_clean['open'].where(df_clean['coin'] == 'EOSTUSD').dropna()
XLMTUSD = df_clean['open'].where(df_clean['coin'] == 'XLMTUSD').dropna()
# ADATUSD = df_clean['open'].where(df_clean['coin'] == 'ADATUSD').dropna()
# TRXTUSD = df_clean['open'].where(df_clean['coin'] == 'TRXTUSD').dropna()
# NEOTUSD = df_clean['open'].where(df_clean['coin'] == 'NEOTUSD').dropna()


plot_graph(BTCTUSD, ETHTUSD, "BTCTUSD", "ETHTUSD")
plot_graph(BTCTUSD, BNBTUSD, "BTCTUSD", "BNBTUSD")
plot_graph(BTCTUSD, XRPTUSD, "BTCTUSD", "XRPTUSD")
plot_graph(BTCTUSD, EOSTUSD, "BTCTUSD", "EOSTUSD")
plot_graph(BTCTUSD, ETHTUSD, "BTCTUSD", "ETHTUSD")
plot_graph(BTCTUSD, XLMTUSD, "BTCTUSD", "XLMTUSD")
# plot_graph(BTCTUSD, ADATUSD, "BTCTUSD", "ADATUSD")
# plot_graph(BTCTUSD, TRXTUSD, "BTCTUSD", "TRXTUSD")
# plot_graph(BTCTUSD, NEOTUSD, "BTCTUSD", "NEOTUSD")

independent_vars = pd.DataFrame()
cols = ['BTCTUSD', 'ETHTUSD', 'BNBTUSD', 'XRPTUSD', 'EOSTUSD', 'XLMTUSD']
regression_vars = pd.concat([BTCTUSD, ETHTUSD, BNBTUSD, XRPTUSD, EOSTUSD, XLMTUSD], axis=1).dropna()
regression_vars.columns = cols

export_csv = regression_vars.to_csv(r'/tmp/coins_to_excel.csv', index=True, header=True)

X = regression_vars[['ETHTUSD', 'BNBTUSD', 'XRPTUSD', 'EOSTUSD', 'XLMTUSD']].astype(float)
Y = regression_vars['BTCTUSD'].astype(float)

regr = linear_model.LinearRegression()
regr.fit(X, Y)

print('Intercept: \n', regr.intercept_)
print('Coefficients: \n', regr.coef_)

pdb.set_trace()

# with statsmodels
X = sm.add_constant(X)  # adding a constant

model = sm.OLS(Y, X).fit()
predictions = model.predict(X)
print_model = model.summary()

print(print_model)
# X = df[['Interest_Rate','Unemployment_Rate']]
# Y = df['Stock_Index_Price']
#

# # with sklearn
# regr = linear_model.LinearRegression()
# regr.fit(X, Y)
#
# print('Intercept: \n', regr.intercept_)
# print('Coefficients: \n', regr.coef_)
