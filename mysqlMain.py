import requests
from bs4 import BeautifulSoup
import mysql.connector
import locale
import re
from dbManager import insertAdvert
from dbManager import connDb
from dbManager import deleteAdverts

locale.setlocale(locale.LC_ALL, 'nl_NL.utf8')
# connect to database
conn = mysql.connector.connect(user='joost', password='passwd',
                               host='localhost', database='marktplaats')
cursor = conn.cursor(buffered=True)

dbList = []

included = ['barst', 'Barst', 'scherm', 'Scherm', 'accu', 'Accu', 'camera',
            'Camera', 'defect', 'Defect', 'speaker', 'Speaker', 'home', 'Home',
            'button', 'Button']
excluded = ['Gezocht', 'gezocht', 'NU', 'ACTIE!!', 'ruilen', 'Afgeprijsd!',
            'Aktie!', 'Refurbished', 'gegarandeerd', 'trixon.nl', 'KPN',
            'GARANTIE!', 'Phonestuff', 'inruil', 'Garantie', 'garantie',
            'Informatie']
secondCursor = conn.cursor(buffered=True)
secondCursor.execute("SELECT link FROM Advert")
for advert in secondCursor.fetchall():
    dbList.append(advert[0])
# get all searches
cursor.execute("SELECT * FROM Search")
for search in cursor.fetchall():
    print(search)
    firstPage = search[7]
    loadPage = requests.get(str(firstPage) + '&postcode=' + str(search[6]))
    firstSoup = BeautifulSoup(loadPage.content, 'lxml')
    try:
        pageCount = int(firstSoup.find('span', class_='last').text)
    except ValueError as e:
        pageCount = 1
    for pageNumber in range(1, pageCount + 1, 1):
        print('On page ' + str(pageNumber) + ' of ' + str(pageCount)
              + '. Loading...\n')
        page = requests.get(str(firstPage) + str('&currentPage=') +
                            str(pageNumber) + '&postcode=' + str(search[6]))
        soup = BeautifulSoup(page.content, 'lxml')
        for article in soup.select('article.row.search-result'):
            link = article.get('data-url')
            if link not in dbList:
                description1 = article.find('span', class_='mp-listing-' +
                                            'description').text
                description1 = description1.strip()
                description2 = article.find('span', class_='mp-listing-desc' +
                                            'ription-extended wrapped')

                title = article.find('span', class_='mp-listing-title').text
                if description2 is None:
                    description = description1
                else:
                    description2 = re.sub('\s', ' ', description2.text)
                    description2 = description2.strip()
                    description = description1 + description2

                if (all(exclude not in title and exclude not in description
                        for exclude in excluded) and
                        any(include in title or include in description
                            for include in included)):
                    insertAdvert(article, title, description, search[0],
                                 search[2], search[3], search[4], link)
connDb.commit()
deleteAdverts()
connDb.commit()
conn.close()
