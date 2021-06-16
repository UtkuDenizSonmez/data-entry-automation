from bs4 import BeautifulSoup
from selenium import webdriver
import time
import requests

FORM_LINK = "https://docs.google.com/forms/d/e/1FAIpQLSdAnd6rtul2C4qB4KwPXePPnypkTAjNrOiX4wpm8D8bN69UXA/viewform?usp=sf_link"
ENDPOINT = "https://www.zillow.com/san-francisco-ca/rentals/?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22usersSearchTerm%22%3A%22San%20Francisco%2C%20CA%22%2C%22mapBounds%22%3A%7B%22west%22%3A-122.63417281103516%2C%22east%22%3A-122.23248518896484%2C%22south%22%3A37.66204404227982%2C%22north%22%3A37.88836565815623%7D%2C%22mapZoom%22%3A12%2C%22regionSelection%22%3A%5B%7B%22regionId%22%3A20330%2C%22regionType%22%3A6%7D%5D%2C%22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B%22price%22%3A%7B%22min%22%3A0%2C%22max%22%3A872627%7D%2C%22beds%22%3A%7B%22min%22%3A1%7D%2C%22pmf%22%3A%7B%22value%22%3Afalse%7D%2C%22fore%22%3A%7B%22value%22%3Afalse%7D%2C%22mp%22%3A%7B%22min%22%3A0%2C%22max%22%3A3000%7D%2C%22ah%22%3A%7B%22value%22%3Atrue%7D%2C%22auc%22%3A%7B%22value%22%3Afalse%7D%2C%22nc%22%3A%7B%22value%22%3Afalse%7D%2C%22fr%22%3A%7B%22value%22%3Atrue%7D%2C%22fsbo%22%3A%7B%22value%22%3Afalse%7D%2C%22cmsn%22%3A%7B%22value%22%3Afalse%7D%2C%22pf%22%3A%7B%22value%22%3Afalse%7D%2C%22fsba%22%3A%7B%22value%22%3Afalse%7D%2C%22mf%22%3A%7B%22value%22%3Afalse%7D%2C%22land%22%3A%7B%22value%22%3Afalse%7D%2C%22manu%22%3A%7B%22value%22%3Afalse%7D%2C%22baths%22%3A%7B%22min%22%3A1%7D%7D%2C%22isListVisible%22%3Atrue%7D"
WEBSITE_LINK = "https://www.zillow.com"

CHROME_DRIVER_PATH = "YOUR_CHROME_DRIVER_PATH"

headers = {
    "Accept-Language": "YOUR_AL",
    "User-Agent": "YOUR U_A",
}

response = requests.get(url=ENDPOINT, headers=headers)
zillow_items = response.text
soup = BeautifulSoup(zillow_items, "html.parser")
# ################ ALL PRICES #################
house_prices = soup.find_all(name="div", class_="list-card-price")
prices = []
for price in house_prices:
    prices.append(price.getText()[:6])
# ################ ALL ADDRESSES #################
house_addresses = soup.find_all(name="address", class_="list-card-addr")
addresses = []
for address in house_addresses:
    addresses.append(address.getText())
# ################ ALL LINKS #################
house_links = soup.find_all(name="a", class_="list-card-link")
temporary_links = []
for link in house_links:
    a = link.get("href")
    if a[0] != "h":
        a = f"{WEBSITE_LINK}{a}"
    temporary_links.append(a)
links = [temporary_links[i] for i in range(0, len(temporary_links)) if i % 2 == 0]
# ################ Form #################
driver = webdriver.Chrome(executable_path=CHROME_DRIVER_PATH)
for i in range(len(prices)):  # 40 times
    driver.get(url=FORM_LINK)
    time.sleep(2)
    address_bar = driver.find_element_by_xpath('//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')
    address_bar.send_keys(addresses[i])
    prices_bar = driver.find_element_by_xpath('//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')
    prices_bar.send_keys(prices[i])
    link_bar = driver.find_element_by_xpath('//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')
    link_bar.send_keys(links[i])
    send_button = driver.find_element_by_xpath('//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div/div/span/span')
    send_button.click()
    time.sleep(2)










