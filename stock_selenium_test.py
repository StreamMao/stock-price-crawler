from selenium import webdriver
from bs4 import BeautifulSoup

DRIVER_PATH = './utils/chromedriver.exe'
# initialize an instance of the chrome driver (browser)
driver = webdriver.Chrome(executable_path=DRIVER_PATH)

# visit your target site
driver.get("https://ca.finance.yahoo.com/quote/META/")

soup = BeautifulSoup(driver.page_source, "html.parser")
headerElement = soup.find("h1",{"class": "yf-xxbei9"})
foundElement = soup.find("fin-streamer",{"data-symbol":"META", "data-field": "regularMarketPrice"})
postMarketElement = soup.find("fin-streamer",{"data-symbol":"META", "data-field": "postMarketPrice"})
# print(driver.page_source)
print(headerElement)
print(foundElement)
print(postMarketElement)
# price = foundElement["data-value"]
# print(price)

driver.quit()