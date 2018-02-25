import mysql.connector
import requests
from bs4 import BeautifulSoup
import datetime
from mail import sendMail

connDb = mysql.connector.connect(user='joost', password='passwd',
                                 host='localhost', database='marktplaats')
cursor = connDb.cursor(buffered=True)


def insertAdvert(article, title, description, searchID, maxPrice, minPrice,
                 maxBidPrice, link):
    date = (article.find('div', class_='date').text).strip()
    city = article.find('div', class_='location-name').text
    if date == 'Vandaag':
        date = datetime.date.today()
        date = date.strftime("%Y-%m-%d")
    elif date == 'Gisteren':
        date = datetime.date.today() - datetime.timedelta(1)
        date = date.strftime("%Y-%m-%d")
    elif date == 'Eergisteren':
        date = datetime.date.today() - datetime.timedelta(2)
        date = date.strftime("%Y-%m-%d")
    else:
        date = datetime.datetime.strptime(date, "%d %b. '%y")
        date = date.strftime("%Y-%m-%d")
    price = article.find('span', class_='price-new').text.strip()
    try:
        isPriceString = False
        price = float(price[2:].replace('.', '').replace(',', '.'))
        if price < maxPrice and price > minPrice:
            cursor.execute("INSERT INTO Advert(searchID, title, date," +
                           "description, priceNumber, isPriceString," +
                           "city, link) VALUES (%s, %s, %s, %s, %s," +
                           "%s, %s, %s);", (searchID, title, date,
                                            description, price,
                                            isPriceString, city,
                                            link,))
            #sendMail(title, price, description, city, link, date)
    except ValueError:
        if price == 'Bieden':
            isPriceString = False
            bidSite = requests.get(link)
            bidSoup = BeautifulSoup(bidSite.content, 'lxml')
            try:
                bidoverview = bidSoup.find(id='bids-overview')
                bid = bidoverview.get('data-current-' +
                                      'top-bid-formatted')
                bid = float(bid[2:].replace('.', '').replace(',',
                                                             '.'))
                if bid < maxBidPrice:
                    cursor.execute("INSERT INTO Advert(searchID, title," +
                                   "date, description, priceNumber, " +
                                   "isPriceString, city, link)" +
                                   "VALUES (%s, %s, %s, %s, %s, %s," +
                                   "%s, %s);", (searchID, title, date,
                                                description, bid,
                                                isPriceString, city,
                                                link,))
                    #sendMail(title, bid + ' (Bieden)', description, city,
                    #         link, date)

            except Exception as e:
                'Old advert'
                pass
        elif price == 'N.o.t.k.' or price == 'Zie omschrijving':
            isPriceString = True
            cursor.execute("INSERT INTO Advert(searchID, title, date," +
                           "description, priceString, isPriceString, city, " +
                           "link) VALUES (%s, %s, %s, %s, %s, %s, %s, %s);",
                           (searchID, title, date, description, price,
                            isPriceString, city, link,))
            #sendMail(title, price, description, city, link, date)


def deleteAdverts():
    cursor.execute("SELECT link FROM Advert")
    for link in cursor.fetchall():
        page = requests.get(link[0])
        soup = BeautifulSoup(page.content, 'lxml')
        old = soup.find('div', class_='mp-Alert mp-Alert--tip evip-caption')
        if old is not None:
            cursor.execute("DELETE * FROM Advert WHERE link = %s", (link,))


def addSearch(title, maxPrice, minPrice, maxBidPrice, distance, zipCode, link):
    cursor.execute("INSERT INTO Search (query, maxPrice, minPrice," +
                   "maxBidPrice, distance, zipCode, link) " +
                   "VALUES (%s, %s, %s, %s, %s, %s, %s)", (title,
                                                           maxPrice,
                                                           minPrice,
                                                           maxBidPrice,
                                                           distance,
                                                           zipCode,
                                                           link))
    connDb.commit()
