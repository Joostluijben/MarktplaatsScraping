import requests
from bs4 import BeautifulSoup
import mysql.connector
import locale
import re
from dbManager import insertAdvert
from dbManager import deleteAdverts
from dbManager import bidRefresher

locale.setlocale(locale.LC_ALL, 'nl_NL.utf8')
# connect to database
conn = mysql.connector.connect(user='joost', password='passwd',
                               host='localhost', database='marktplaats')
cursor = conn.cursor(buffered=True)

dbList = []

secondCursor = conn.cursor(buffered=True)
secondCursor.execute("SELECT link FROM Advert")
for advert in secondCursor.fetchall():
    dbList.append(advert[0])
thirdCursor = conn.cursor(buffered=True)
fourthCursor = conn.cursor(buffered=True)
# get all searches
cursor.execute("SELECT * FROM Search")
webLinks = []
for search in cursor.fetchall():
    firstPage = search[7] + '&distance=' + str(search[5]) + "&postcode=" + search[6]
    print(firstPage)
    loadPage = requests.get(firstPage)
    firstSoup = BeautifulSoup(loadPage.content, 'lxml')

    try:
        pageCount = int(firstSoup.find('span', class_='last').text)
        print(pageCount)
    except AttributeError as e:
        pageCount = 1
    for pageNumber in range(1, pageCount + 1, 1):
        print('On page ' + str(pageNumber) + ' of ' + str(pageCount)
              + '. Loading...\n')
        page = requests.get(str(firstPage) + str('&currentPage=') +
                            str(pageNumber))
        soup = BeautifulSoup(page.content, 'lxml')
        count = 0
        for article in soup.select('article.row.search-result'):
            link = article.get('data-url')
            webLinks.append(link)
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
                thirdCursor.execute("SELECT include FROM Included, Search, SearchIncluded WHERE Search.searchID = %s AND SearchIncluded.searchID = Search.searchID AND Included.includedID = SearchIncluded.includedID;", (search[0],))
                fourthCursor.execute("SELECT exclude FROM Excluded, Search, SearchExcluded WHERE Search.searchID = %s AND SearchExcluded.searchID = Search.searchID AND Excluded.excludedID = SearchExcluded.excludedID;", (search[0],))
                count += 1
                if (any(include[0] in title or include[0] in description for include in thirdCursor.fetchall()) and
                        all(exclude[0] not in title and exclude[0] not in description for exclude in fourthCursor.fetchall())):
                    insertAdvert(article, title, description, search[0],
                                 search[2], search[3], search[4], link)

cursor.execute("SELECT link, advertID from Advert")
for link in cursor.fetchall():
    if link[0] not in webLinks:
        secondCursor.execute("DELETE FROM Advert WHERE advertID = %s", (link[1],))
conn.commit()
bidRefresher()
deleteAdverts()
cursor.close()
conn.close()
