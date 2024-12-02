from urllib.request import urlopen
from bs4 import BeautifulSoup
from selenium import webdriver
import pandas as pd
import datetime




funds = ["RBF263.CF", "RBF590.CF", "RBF557.CF", "INA48603.CF", "INA36081.CF"]
# funds = ["RBF263.CF", "RBF263.CF"]
stocks = ["AAPL", "META", "NVDA", "AMZN", "MSFT", "SHOP", "TSLA", "GOOG", "AVGO"] #apple，meta，nvidia，amazon，Microsoft，shopify，tesla，alphabet，broadcom

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

file_path = "data.xlsx"
df = pd.read_excel(file_path, engine="openpyxl")

def add_data(df, name, symbol, price):
    price = float(price)
    date = datetime.date.today().strftime("%Y-%m-%d")
    # date = datetime.date.today().strftime("%Y-%m")
    # date = datetime.datetime.now()
    
    # print(name)
    # print(symbol)
    # print(price)
    # print(date)
    
    column_name = symbol + "(" + name + ")"
    
    if date in df['date'].values:
        # Add {column_name} column where 'date'=={date}
        df.loc[df['date'] == date, column_name] = price
    else:
        # Add a new row with date '{date} and column {column_name}
        new_row = {'date': date, column_name: price}
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)

    return df

for stock in stocks:
    url = "https://ca.finance.yahoo.com/quote/" + stock + "/"

    DRIVER_PATH = './utils/chromedriver.exe'
    # initialize an instance of the chrome driver (browser)
    driver = webdriver.Chrome(executable_path=DRIVER_PATH)

    # visit your target site
    driver.get(url)

    soup = BeautifulSoup(driver.page_source, "html.parser")
    headerElement = soup.find("h1",{"class": "yf-xxbei9"})
    foundElement = soup.find("fin-streamer",{"data-symbol":stock, "data-field": "regularMarketPrice"})
    postMarketElement = soup.find("fin-streamer",{"data-symbol":stock, "data-field": "postMarketPrice"})

    print("foundElement", foundElement)
    driver.quit()
    name = headerElement.text
    symbol = foundElement["data-symbol"]
    price = foundElement["data-value"]
    postMarketPrice = postMarketElement["data-value"]

    print(name)
    print(symbol)
    print(price)
    print(postMarketPrice)

    # name = instrument_name.text
    # symbol = instrument_symbol.text[1: -1]
    # price = price_attribute["value"]

    df = add_data(df, name, symbol, price)
    
print(df)
df.to_excel('data.xlsx', index=False)