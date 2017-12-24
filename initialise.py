from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import variables
db = Database('articles.db')
#driver = webdriver.Chrome('/home/joost/Downloads/chromedriver')
def initialise():
    driver = variables.driver
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

    priceFrom = driver.find_element_by_xpath("//input[@name='priceFrom']")
    priceFrom.send_keys('50')

    priceTo = driver.find_element_by_xpath("//input[@name='priceTo']")
    priceTo.send_keys('100')

    refreshPrice = driver.find_element_by_xpath("//button[@class='button mp-Button mp-Button--secondary mp-Button--sm search-attribute-submit']")
    refreshPrice.click()

    sort = driver.find_element_by_xpath("//select[@id='sort-order']/option[text()='Prijs (laag-hoog)']")
    time.sleep(0.2)
    sort.click()
