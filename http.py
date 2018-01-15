import requests
from bs4 import BeautifulSoup
import datetime
import re
from itertools import zip_longest
import locale
locale.setlocale(locale.LC_ALL, 'nl_NL.utf8')
#db = Database('/home/joost/Documents/Markplaats_prototype/iphones_better/articles.db')
#page = requests.get('https://www.marktplaats.nl/z.html?query=iphone+6&categoryId=1953&postcode=3445TA&distance=3000&currentPage=1')
#soup = BeautifulSoup(page.content, 'html.parser')
#titles = [title.get_text() for title in soup.find_all('span', class_='mp-listing-title')]
#print(titles)
#nextClick = soup.find('a', class_='mp-Button mp-Button--round pagination-next')
#pageNew = requests.get(nextClick['href'])
#print(BeautifulSoup(pageNew.content), 'html.parser')

firstPage = 'https://www.marktplaats.nl/z.html?query=iphone+6&categoryId=1953&postcode=3445TA&distance=10000'

loadPage = requests.get(firstPage)
firstSoup = BeautifulSoup(loadPage.content, 'lxml')
#nextPage = firstSoup.find('a', class_='mp-Button mp-Button--round pagination-next')['href']
pageCount = int(firstSoup.find('span', class_='last').text)
dbList = []

for pageNumber in range(1,pageCount+1,1):
    print('On page ' + str(pageNumber) + ' of ' + str(pageCount) + '. Loading...\n')
    page = requests.get(str(firstPage) + str('&currentPage=') + str(pageNumber))
    soup = BeautifulSoup(page.content, 'lxml')
    titles = []
    dates = []
    descriptions1 = []
    descriptions2 = []
    prices = []
    links = []

    for article in soup.select('article.row.search-result'):
        try:
            dates.append((article.find('div', class_='date').text).strip())
        except:
            pass
        try:
            titles.append(article.find('span', class_='mp-listing-title').text)
        except:
            pass
        try:
            descriptions1.append(article.find('span', class_='mp-listing-description').text)
        except:
            pass
        try:
            descriptions2.append(re.sub( '\s', ' ',article.find('span', class_='mp-listing-description-extended wrapped').text).strip())
        except:
            descriptions2.append('')
            pass
        try:
            prices.append(article.find(''))
    #print(str(descriptions1) + '\n')
    #print(str(descriptions2)+ '\n')
    #for description in zip_longest(descriptions1, descriptions2):
    #    print(description)
    descriptions = [description[0] if description[1] == None else ''.join((description[0], description[1])) for description in zip_longest(descriptions1, descriptions2)]
    dates = [datetime.date.today().strftime("%d %b. '%y") if date=='Vandaag' else (datetime.datetime.today() - datetime.timedelta(1)).strftime("%d %b. '%y") if date == 'Gisteren' else
             (datetime.date.today() - datetime.timedelta(1)).strftime("%d %b. '%y") if date=='Eergisteren' else date
             for date in dates]
    for i in range(len(dates)):
        dbList.append((titles[i], dates[i], descriptions[i]))
    #print(articles)
print(dbList)
    #print(str(firstPage) + str('&currentPage=') + str(pageNumber))
#firstPage = nextPage
#print(firstPage)
