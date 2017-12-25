from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import datetime
import locale
import time
from mail import sendMail
from itertools import zip_longest
locale.setlocale(locale.LC_ALL, 'nl_NL.utf8')
#from pyvirtualdisplay import Display
import re
from jsondb.db import Database
#display = Display(visible=0, size=(800, 600))
#display.start()
db = Database('/home/joost/Documents/Github/Markplaats_scraping/articles.db')
driver = webdriver.Chrome('/home/joost/Downloads/chromedriver')
def initialise():
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
    #priceFrom = driver.find_element_by_xpath("//input[@name='priceFrom']")
    #priceFrom.send_keys('50')

    #priceTo = driver.find_element_by_xpath("//input[@name='priceTo']")
    #priceTo.send_keys('200')
    #refreshPrice = driver.find_element_by_xpath("//button[@class='button mp-Button mp-Button--secondary mp-Button--sm search-attribute-submit']")
    #refreshPrice.click()

    #sort = driver.find_element_by_xpath("//select[@id='sort-order']/option[text()='Prijs (laag-hoog)']")
    #time.sleep(0.2)
    #sort.click()
initialise()
siteArticles = []
try:
    pageCount = int((driver.find_element_by_xpath("//div[@id='page-wrapper']/div[@class='l-page']/div[@class='l-main-right']/div[@id='search-results']/div[@id='pagination']/span[@id='pagination-pages']/span[@class='last']")).get_attribute('innerHTML'))
except:
    pageCount = 1

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
            dates = [datetime.date.today().strftime("%d %b. '%y") if date=='Vandaag' else (datetime.datetime.today() - datetime.timedelta(1)).strftime("%d %b. '%y") if date == 'Gisteren' else
                     (datetime.date.today() - datetime.timedelta(1)).strftime("%d %b. '%y") if date=='Eergisteren' else date
                     for date in dates]
            print(len(dates))
            descriptions1 = [description.text for description in driver.find_elements_by_xpath("//section[@class='search-results-table table']/article/div/div[@class='cell column-listing']/div[@class='listing-title-description']/a/span[@class='mp-listing-description']")]
            descriptions2 = [re.sub( '\s+', ' ', description.get_attribute('innerHTML')).strip() for description in driver.find_elements_by_xpath("//section[@class='search-results-table table']/article/div/div[@class='cell column-listing']/div[@class='listing-title-description']/a/span[@class='mp-listing-description-extended wrapped']")]
            print(str(descriptions2) + '\n')
            descriptions = [description[0] if description[1] == None else ''.join((description[0], description[1])) for description in zip_longest(descriptions1, descriptions2)]
            print([price.text for price in driver.find_elements_by_xpath("//section[@class='search-results-table table']/article/div/div[@class='cell column-price meta-info']/div[@class='price-and-thumb-container']/span/span")])
            prices = [price.text if (price.text == 'Bieden' or price.text == 'Gereserveerd' or price.text == 'Zie omschrijving' or price.text == 'Gratis' or price.text=='N.o.t.k.' or price.text =='Ruilen' or price.text=='Op aanvraag') else float(price.text[2:].replace(',', '.')) for price in driver.find_elements_by_xpath("//section[@class='search-results-table table']/article/div/div[@class='cell column-price meta-info']/div[@class='price-and-thumb-container']/span/span")]
            cities = [city.get_attribute('innerHTML') for city in driver.find_elements_by_xpath("//section[@class='search-results-table table']/article/div/div[@class='cell column-location seller-info']/div/div[@class='location-name']")]
            links = [link.get_attribute('href') for link in driver.find_elements_by_xpath("//section[@class='search-results-table table']/article/div/div[@class='cell column-listing']/div[@class='listing-title-description']/h2/a")]
            for i in range(len(titles)):
                siteArticles.append((titles[i], dates[i], str(descriptions[i]), prices[i], cities[i], links[i]))
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
dbList = []
for row in db:
    for article in db[row]:
        dbList.append((article['title'], article['date']))
for siteArticle in siteArticles:
    if tuple((siteArticle[0], siteArticle[1])) not in dbList:
        if (
            'Refurbished' not in siteArticle[0] and
            'refurbished' not in siteArticle[0] and
            'Refurbished' not in siteArticle[2] and
            'refurbished' not in siteArticle[2] and
            'Reparatie' not in siteArticle[0] and
            'reparatie' not in siteArticle[0] and
            'Reparatie' not in siteArticle[2] and
            'reparatie' not in siteArticle[2] and
            'LCD' not in siteArticle[0] and
            'LCD' not in siteArticle[2] and
            'Onderdelen' not in siteArticle[0] and
            'onderdelen' not in siteArticle[0] and
            'Onderdelen' not in siteArticle[2] and
            'onderdelen' not in siteArticle[2] and
            'geluidsversterker' not in siteArticle[0] and
            'geluidsversterker' not in siteArticle[2] and
            'Radio' not in siteArticle[0] and
            'radio' not in siteArticle[0] and
            'Radio' not in siteArticle[2] and
            'radio' not in siteArticle[2] and
            'garantie' not in siteArticle[0] and
            'garantie' not in siteArticle[2] and
            'KRAGARANTIE' not in siteArticle[0] and
            'GARANTIE' not in siteArticle[2] and
            'Garantie' not in siteArticle[0] and
            'Garantie' not in siteArticle[2] and
            'WiFi' not in siteArticle[0] and
            'WiFi' not in siteArticle[2] and
            'wifi' not in siteArticle[0] and
            'wifi' not in siteArticle[2] and
            'Sim only' not in siteArticle[0] and
            'Sim only' not in siteArticle[2] and
            'sim only' not in siteArticle[0] and
            'sim only' not in siteArticle[2] and
            'abonnement' not in siteArticle[0] and
            'abonnement' not in siteArticle[2] and
            'gezocht' not in siteArticle[0] and
            'gezocht' not in siteArticle[2] and
            'Gezocht' not in siteArticle[0] and
            'Gezocht' not in siteArticle[2] and
            'GEZOCHT' not in siteArticle[0] and
            'GEZOCHT' not in siteArticle[2] and
            'Phonestuff' not in siteArticle[0] and
            'Phonestuff' not in siteArticle[2] and
            'Leeg' not in siteArticle[0] and
            'Leeg' not in siteArticle[2] and
            'KRASVRIJ + GARANTIE !!!' not in siteArticle[0] and
            'KRASVRIJ + GARANTIE !!!' not in siteArticle[2] and
            'voorraad' not in siteArticle[0] and
            'voorraad' not in siteArticle[2] and
            'Moederbord' not in siteArticle[0] and
            'Moederbord' not in siteArticle[2] and
            'moederbord' not in siteArticle[0] and
            'moederbord' not in siteArticle[2] and
            'Productbeschrijving' not in siteArticle[0] and
            'Productbeschrijving' not in siteArticle[2] and
            'iCloud gelockt' not in siteArticle[0] and
            'iCloud gelockt' not in siteArticle[2] and
            'icloud gelockt' not in siteArticle[0] and
            'icloud gelockt' not in siteArticle[2]
            ):
            articleList = list(db['iphone 6'])
            if type(siteArticle[3]) == float:
                if (siteArticle[3] <= 100 and siteArticle[3] > 50):
                    articleList.append({"title" : siteArticle[0], "date" : siteArticle[1], "description" : siteArticle[2], "price" : siteArticle[3], "city" : siteArticle[4], "link" : siteArticle[5]})
                    sendMail(title=siteArticle[0], price=siteArticle[3], description=siteArticle[2], city=siteArticle[4], link=siteArticle[5], date=siteArticle[1])
                    print('float send\n')

                else:
                    pass
            else:
                if siteArticle[3] == 'Gratis' or siteArticle[3] == 'Gereserveerd' or siteArticle[3]=='Ruilen':
                    pass
                elif siteArticle[3] == 'Bieden':
                    driver.get(siteArticle[5])
                    bid = driver.find_element_by_xpath("//div[@id='page-wrapper']/div[@id='content']/aside[@class='l-side-right']/section[@id='vip-bidding-block']/div[@id='vip-list-bids-block']/div[@id='bids-overview']").get_attribute('data-current-top-bid-formatted')
                    temp_siteArticle = list(siteArticle)
                    temp_siteArticle[3] = float(bid[2:].replace(',', '.'))
                    siteArticle = temp_siteArticle
                    articleList.append({"title" : siteArticle[0], "date" : siteArticle[1], "description" : siteArticle[2], "price" : siteArticle[3], "city" : siteArticle[4], "link" : siteArticle[5]})
                    if siteArticle[3] < 120:
                        sendMail(title=siteArticle[0], price=siteArticle[3], description=siteArticle[2], city=siteArticle[4], link=siteArticle[5], date=siteArticle[1])
                        print('Bieden send\n')
                        pass
                    pass
                else:
                    articleList.append({"title" : siteArticle[0], "date" : siteArticle[1], "description" : siteArticle[2], "price" : siteArticle[3], "city" : siteArticle[4], "link" : siteArticle[5]})
                    sendMail(title=siteArticle[0], price=siteArticle[3], description=siteArticle[2], city=siteArticle[4], link=siteArticle[5], date=siteArticle[1])
                    print('string send\n')

            db['iphone 6'] = articleList
        else:
            pass

driver.quit()
#display.stop()
