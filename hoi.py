from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from jsondb.db import Database
import time
db = Database('articles.db')
driver = webdriver.Chrome('/home/joost/Downloads/chromedriver')
driver.get('https://marktplaats.nl')
cookie = driver.find_element_by_xpath("//input[@value='Cookies accepteren']");
cookie.click()
dbList = [article for article in db['iphone 6']]
for article in dbList:
    if article['price'] == 'Bieden':
        driver.get(article['link'])
        bid = driver.find_element_by_xpath("//div[@id='page-wrapper']/div[@id='content']/aside[@class='l-side-right']/section[@id='vip-bidding-block']/div[@id='vip-list-bids-block']/div[@id='bids-overview']").get_attribute('data-current-top-bid-formatted')
        article['price'] = float((bid[2:]).replace(',', '.'))
db['iphone 6'] = dbList
driver.quit()
