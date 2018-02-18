import requests
from bs4 import BeautifulSoup
import datetime
import re
from itertools import zip_longest
import locale
from jsondb.db import Database
from searchManager import readSearches
from mail import sendMail
from collections import OrderedDict
locale.setlocale(locale.LC_ALL, 'nl_NL.utf8')
db = Database('/home/joost/Documents/Markplaats_prototype/http/articles.db')
for search in readSearches():
    firstPage = search[6]
    loadPage = requests.get(str(firstPage) + '&postcode=' + str(search[5]))
    firstSoup = BeautifulSoup(loadPage.content, 'lxml')
    try:
        pageCount = int(firstSoup.find('span', class_='last').text)
    except:
        pageCount = 1
    if db[search[0]] == None:
        db[search[0]] = []
    else:
        pass
    siteArticles = []

    for pageNumber in range(1,pageCount+1,1):
        print('On page ' + str(pageNumber) + ' of ' + str(pageCount) + '. Loading...\n')
        page = requests.get(str(firstPage) + str('&currentPage=') + str(pageNumber)+ '&postcode=' + str(search[5]))
        soup = BeautifulSoup(page.content, 'lxml')
        print(page.url)
        titles = []
        dates = []
        descriptions1 = []
        descriptions2 = []
        prices = []
        cities = []
        links = []

        for article in soup.select('article.row.search-result'):
            dates.append((article.find('div', class_='date').text).strip())
            titles.append(article.find('span', class_='mp-listing-title').text)
            descriptions1.append(article.find('span', class_='mp-listing-description').text)
            try:
                descriptions2.append(re.sub( '\s', ' ',article.find('span', class_='mp-listing-description-extended wrapped').text).strip())
            except:
                descriptions2.append('')
                pass
            prices.append((article.find('span', class_='price-new').text).strip())
            cities.append(article.find('div', class_='location-name').text)
            links.append(article.get('data-url'))

        descriptions = [description[0] if description[1] == None else ''.join((description[0], description[1])) for description in zip_longest(descriptions1, descriptions2)]
        dates = [datetime.date.today().strftime("%d %b. '%y") if date=='Vandaag' else (datetime.datetime.today() - datetime.timedelta(1)).strftime("%d %b. '%y") if date == 'Gisteren' else
                 (datetime.date.today() - datetime.timedelta(1)).strftime("%d %b. '%y") if date=='Eergisteren' else date
                 for date in dates]
        prices = [price if (price == 'Bieden' or price == 'Gereserveerd' or price == 'Zie omschrijving' or price == 'Gratis' or price == 'N.o.t.k.' or price == 'Ruilen' or price == 'Op aanvraag')
                  else  float(price[2:].replace('.', '').replace(',', '.')) for price in prices]

        for i in range(len(dates)):
            siteArticles.append((titles[i], dates[i], descriptions[i], prices[i], cities[i], links[i]))

    dbList = []
    for article in db[search[0]]:
        dbList.append((article['title'], article['date']))
    for siteArticle in siteArticles:
        if tuple((siteArticle[0], siteArticle[1])) not in dbList:
            if (
                'Refurbished' not in siteArticle[0] and
                'refurbished' not in siteArticle[0] and
                'Refurbished' not in siteArticle[2] and
                'refurbished' not in siteArticle[2] and
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
                'icloud gelockt' not in siteArticle[2] and
                'Inkoop' not in siteArticle[0] and
                'Inkoop' not in siteArticle[2] and
                'inkoop' not in siteArticle[0] and
                'inkoop' not in siteArticle[2] and
                'INKOOP' not in siteArticle[0] and
                'INKOOP' not in siteArticle[2] and
                (
                'kapot' in siteArticle[0] or
                'kapot' in siteArticle[2] or
                'Kapot' in siteArticle[0] or
                'Kapot' in siteArticle[2] or
                'defect' in siteArticle[0] or
                'defect' in siteArticle[2] or
                'Defect' in siteArticle[0] or
                'Defect' in siteArticle[2] or
                'barsten' in siteArticle[0] or
                'barsten' in siteArticle[2] or
                'Barsten' in siteArticle[0] or
                'Barsten' in siteArticle[2] or
                'barst' in siteArticle[0] or
                'barst' in siteArticle[2] or
                'Barst' in siteArticle[0] or
                'Barst' in siteArticle[2]
                )
                ):
                print('Checking interesting adverts')
                articleList = list(db[search[0]])
                if type(siteArticle[3]) == float:
                    if (siteArticle[3] <= int(search[1]) and siteArticle[3] > int(search[2])):
                        articleList.append({"title" : siteArticle[0], "date" : siteArticle[1], "description" : siteArticle[2], "price" : siteArticle[3], "city" : siteArticle[4], "link" : siteArticle[5]})
                        #sendMail(title=siteArticle[0], price=siteArticle[3], description=siteArticle[2], city=siteArticle[4], link=siteArticle[5], date=siteArticle[1])
                        print('float send\n')

                    else:
                        pass
                else:
                    if siteArticle[3] == 'Gratis' or siteArticle[3] == 'Gereserveerd' or siteArticle[3]=='Ruilen':
                        pass
                    elif siteArticle[3] == 'Bieden':
                        bidSite = requests.get(siteArticle[5])
                        bidSoup = BeautifulSoup(bidSite.content, 'lxml')
                        print('Checking out highest bid')
                        try:
                            bid = bidSoup.find(id='bids-overview').get('data-current-top-bid-formatted')
                        except:
                            'Old advert'
                            pass
                        temp_siteArticle = list(siteArticle)
                        temp_siteArticle[3] = float(bid[2:].replace(',', '.'))
                        siteArticle = temp_siteArticle
                        if siteArticle[3]    < int(search[3]):
                            articleList.append({"title" : siteArticle[0], "date" : siteArticle[1], "description" : siteArticle[2], "price" : siteArticle[3], "city" : siteArticle[4], "link" : siteArticle[5]})
                            #sendMail(title=siteArticle[0], price=(str(siteArticle[3]) +' (Bieden)'), description=siteArticle[2], city=siteArticle[4], link=siteArticle[5], date=siteArticle[1])
                            print('Bieden send\n')
                            pass
                        pass
                    else:
                        articleList.append({"title" : siteArticle[0], "date" : siteArticle[1], "description" : siteArticle[2], "price" : siteArticle[3], "city" : siteArticle[4], "link" : siteArticle[5]})
                        #sendMail(title=siteArticle[0], price=siteArticle[3], description=siteArticle[2], city=siteArticle[4], link=siteArticle[5], date=siteArticle[1])
                        print('String send\n')

                db[search[0]] = articleList
            else:
                pass
