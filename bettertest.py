from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import datetime
import locale
import time
locale.setlocale(locale.LC_ALL, 'nl_NL.utf8')
from jsondb.db import Database
driver = webdriver.Chrome('/home/joost/Downloads/chromedriver')


driver.get('https://www.marktplaats.nl/z/telecommunicatie/mobiele-telefoons-apple-iphone/iphone-6.html?query=iphone%206&categoryId=1953&distance=15000&sortBy=price&sortOrder=increasing')
cookie = driver.find_element_by_xpath("//input[@value='Cookies accepteren']");
cookie.click()
descriptions2 = [description.get_attribute('innerHTML') for description in driver.find_elements_by_xpath("//section[@class='search-results-table table']/article/div/div[@class='cell column-listing']/div[@class='listing-title-description']/a/span[@class='mp-listing-description-extended wrapped']")]
print(descriptions2)
