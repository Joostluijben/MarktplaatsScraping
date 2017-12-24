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
time.sleep(0.2)
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
priceFrom = driver.find_element_by_xpath("//input[@name='priceFrom']")
priceFrom.send_keys('50')

priceTo = driver.find_element_by_xpath("//input[@name='priceTo']")
priceTo.send_keys('200')
refreshPrice = driver.find_element_by_xpath("//button[@class='button mp-Button mp-Button--secondary mp-Button--sm search-attribute-submit']")
refreshPrice.click()
pageCount = (driver.find_element_by_xpath("//div[@id='page-wrapper']/div[@class='l-page']/div[@class='l-main-right']/div[@id='search-results']/div[@id='pagination']/span[@id='pagination-pages']/span[@class='last']")).get_attribute('innerHTML')
print(pageCount)
siteArticles = []
try:
    nextClick = (driver.find_element_by_xpath("//div[@id='page-wrapper']/div[@class='l-page']/div[@class='l-main-right']/div[@id='search-results']/div[@id='pagination']/a[@class='mp-Button mp-Button--round pagination-next']")).get_attribute('href')
    while True:
        print('hoi')
        try:
            nextClick = (driver.find_element_by_xpath("//div[@id='page-wrapper']/div[@class='l-page']/div[@class='l-main-right']/div[@id='search-results']/div[@id='pagination']/a[@class='mp-Button mp-Button--round pagination-next']")).get_attribute('href')
            print(nextClick)
            titles = [title.text for title in driver.find_elements_by_xpath("//section[@class='search-results-table table']/article/div/div[@class='cell column-listing']/div[@class='listing-title-description']/h2/a")]
            print(len(titles))
            dates = [date.text for date in driver.find_elements_by_xpath("//section[@class='search-results-table table']/article/div/div[@class='cell column-price meta-info']/div[@class='date']")]
            print(len(dates))
            dates = [datetime.date.today().strftime("%d %b. '%y") if date=='Vandaag' else date for date in dates]
            print(len(dates))
            descriptions = [description.text for description in driver.find_elements_by_xpath("//section[@class='search-results-table table']/article/div/div[@class='cell column-listing']/div[@class='listing-title-description']/a/span[@class='mp-listing-description']")]
            print(len(descriptions))
            descriptions2 = [description.text for description in driver.find_elements_by_xpath("//section[@class='search-results-table table']/article/div/div[@class='cell column-listing']/div[@class='listing-title-description']/a/span[@class='mp-listing-description-extended wrapped']")]
            for i in range(len(titles)):
                print(i)
                siteArticles.append((titles[i], dates[i], descriptions[i]))
            try:
                driver.get(nextClick)
            except:
                break
            time.sleep(0.5)
        except:
            raise
            break
except:
    raise
    print('doe dit maar 1 keer')
print(siteArticles)
