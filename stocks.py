from urllib.request import urlopen
from bs4 import BeautifulSoup
from openpyxl import load_workbook
import pandas as pd
import datetime
import requests

funds = ["RBF263.CF", "RBF590.CF", "RBF557.CF", "INA48603.CF", "INA36081.CF"]
# funds = ["RBF263.CF", "RBF263.CF"]
stocks = ["AAPL", "META", "NVDA", "AMZN", "MSFT", "SHOP", "TSLA", "GOOG", "AVGO"] #apple，meta，nvidia，amazon，Microsoft，shopify，tesla，alphabet，broadcom

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

file_path = "data.xlsx"
df = pd.read_excel(file_path, engine="openpyxl")

def add_data(df, name, symbol, price):
    date = datetime.date.today().strftime("%Y-%m-%d")
    # date = datetime.datetime.now()
    # print(name)
    # print(symbol)
    # print(price)
    # print(date)

    if symbol in df['symbol'].values:
        # Add {date} column where 'symbol' is '{symbol}
        df.loc[df['symbol'] == symbol, date] = price
    else:
        # Add a new row with symbol '{symbol} and column {date}
        new_row = {'name': name, 'symbol': symbol, date: price}
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)

    return df

for stock in stocks:
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/114.0'}
    url = "https://ca.finance.yahoo.com/quote/" + stock + "/"

    response = requests.get(url, headers=headers)

    # html = urlopen(url).read()
    soup = BeautifulSoup(response.text, "html.parser")

    headerElement = soup.find("h1",{"class": "yf-xxbei9"})
    foundElement = soup.find("fin-streamer",{"data-testid": "qsp-price"})
    
    # print("headerElement", headerElement)
    # print("foundElement", foundElement)
    
    # print(df)
    name = headerElement.text
    symbol = foundElement["data-symbol"]
    price = foundElement["data-value"]

    print(name)
    print(symbol)
    print(price)

    # name = instrument_name.text
    # symbol = instrument_symbol.text[1: -1]
    # price = price_attribute["value"]

    df = add_data(df, name, symbol, price)
    
print(df)
df.to_excel('data.xlsx', index=False)