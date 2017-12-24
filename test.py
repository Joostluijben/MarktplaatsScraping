from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import datetime
import locale
import time
locale.setlocale(locale.LC_ALL, 'nl_NL.utf8')

from jsondb.db import Database
db = Database('articles.db')
driver = webdriver.Chrome('/home/joost/Downloads/chromedriver')

driver.get('https://marktplaats.nl')
cookie = driver.find_element_by_xpath("//input[@value='Cookies accepteren']");
cookie.click()

search = driver.find_element_by_xpath("//input[@name='query']")
search.clear()
querySearch = "iphone 6"
search.send_keys(querySearch)

category = driver.find_element_by_xpath("//select[@name='categoryId']/option[text()='Telecommunicatie']")
category.click()
postcode = driver.find_element_by_xpath("//input[@name='postcode']")
postcode.clear()
postcode.send_keys("3445TA")

distance = driver.find_element_by_xpath("//select[@name='distance']/option[text()='< 15 km']")
distance.click()

submit = driver.find_element_by_xpath("//button[@type='submit']")
submit.click()
iphoneCategory = driver.find_element_by_xpath("//div[@id='page-wrapper']/div[@class='l-page']/section[@id='left-column-container']/div[@id='search-attributes']/form[@id='search-attributes-form']/div[@class='relevant-categories filter-section']/ul/li[@class='level-two parent-category-id-820']/a").get_attribute('href')
driver.get(iphoneCategory)
cities = [city.get_attribute('innerHTML') for city in driver.find_elements_by_xpath("//section[@class='search-results-table table']/article/div/div[@class='cell column-location seller-info']/div/div[@class='location-name']")]
print(cities)
descriptions2 = [description.get_attribute('innerHTML') for description in driver.find_elements_by_xpath("//section[@class='search-results-table table']/article/div/div[@class='cell column-listing']/div[@class='listing-title-description']/a/span[@class='mp-listing-description-extended wrapped']")]
print(descriptions2)
driver.quit()
