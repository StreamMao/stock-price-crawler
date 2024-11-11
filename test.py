from urllib.request import urlopen
from bs4 import BeautifulSoup

funds = []
stocks = []

html = urlopen("https://www.theglobeandmail.com/investing/markets/funds/RBF590.CF/").read()
soup = BeautifulSoup(html, "html.parser")
instrument_name = soup.find("span",{"id":"instrument-name"})
instrument_symbol = soup.find("span",{"id":"instrument-symbol"})
price = soup.find("barchart-field",{"type":"price"})

print(instrument_name.text)
print(instrument_symbol.text)
print(price["value"])