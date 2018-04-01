import mysql.connector
import requests
from bs4 import BeautifulSoup
import datetime
from mail import sendMail

dbUser = 'joost'
dbPasswd = 'passwd'
dbHost = 'localhost'
dbName = 'marktplaats'
connector = mysql.connector


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
    photoDiv = article.find('div', class_='listing-image')
    try:
        photoLink = str('http://') + photoDiv.img.get('data-img-src')[2:]
    except TypeError:
        pass
    price = article.find('span', class_='price-new').text.strip()
    conn = connector.connect(user=dbUser, password=dbPasswd, host=dbHost,
                             database=dbName)
    cursor = conn.cursor()
    try:
        isPriceString = False
        price = float(price[2:].replace('.', '').replace(',', '.'))
        if price < maxPrice and price > minPrice:
            cursor.execute("INSERT INTO Advert(searchID, title, date," +
                           "description, priceNumber, isPriceString," +
                           "isBidding, city, link, photoLink) VALUES (%s, %s, %s, %s, %s,"
                           + "%s, %s, %s, %s, %s);", (searchID, title, date,
                                              description, price,
                                              isPriceString, False, city,
                                              link, photoLink,))
            sendMail(title, price, description, city, link, date, photoLink)
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
                                   "isPriceString, isBidding, city, link, photoLink)" +
                                   "VALUES (%s, %s, %s, %s, %s, %s," +
                                   "%s, %s, %s, %s);", (searchID, title, date,
                                                        description, bid,
                                                        isPriceString, True,
                                                        city, link,
                                                        photoLink,))
                    sendMail(title, str(bid) + ' (Bieden)', description, city,
                             link, date, photoLink)
            except Exception as e:
                'Old advert'
                pass
        elif price == 'N.o.t.k.' or price == 'Zie omschrijving':
            isPriceString = True
            cursor.execute("INSERT INTO Advert(searchID, title, date," +
                           "description, priceString, isPriceString," +
                           "isBidding, city, " +
                           "link, photoLink) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);",
                           (searchID, title, date, description, price,
                            isPriceString, False, city, link, photoLink,))
            sendMail(title, price, description, city, link, date, photoLink)
    conn.commit()
    cursor.close()
    conn.close()


def deleteAdverts():
    conn = connector.connect(user=dbUser, password=dbPasswd, host=dbHost,
                             database=dbName)
    cursor = conn.cursor()
    cursor.execute("SELECT link FROM Advert")
    for link in cursor.fetchall():
        page = requests.get(link[0])
        soup = BeautifulSoup(page.content, 'lxml')
        old = soup.find('div', class_='mp-Alert mp-Alert--tip evip-caption')
        if old is not None:
            cursor.execute("DELETE FROM Advert WHERE link = %s", (link[0],))
    conn.commit()
    cursor.close()
    conn.close()


def bidRefresher():
    conn = connector.connect(user=dbUser, password=dbPasswd, host=dbHost,
                             database=dbName)
    cursor = conn.cursor(buffered=True)
    secondCursor = conn.cursor(buffered=True)
    cursor.execute("SELECT link, advertID, priceNumber FROM Advert WHERE isBidding = 1")
    for link in cursor.fetchall():
        page = requests.get(link[0])
        soup = BeautifulSoup(page.content, 'lxml')
        price = soup.find(id='bids-overview').get('data-current-top-bid-formatted')
        price = float(price[2:].replace('.', '').replace(',', '.'))
        if price != float(link[2]):
            secondCursor.execute("UPDATE Advert SET priceNumber = %s WHERE advertID = %s", (price, link[1]))
    thirdCursor = conn.cursor(buffered=True)
    sql = "SELECT searchID, priceNumber FROM Advert WHERE isPriceString = 0"
    cursor.execute(sql)
    for advert in cursor.fetchall():
        secondCursor.execute("SELECT maxBidPrice FROM Search WHERE searchID = %s", (advert[0],))
        if advert[1] > int(secondCursor.fetchone()[0]):
            thirdCursor.execute("DELETE FROM Advert WHERE searchID = %s", (advert[0],))
    conn.commit()
    cursor.close()
    conn.close()


def addSearch(title, maxPrice, minPrice, maxBidPrice, distance, zipCode, link):
    conn = connector.connect(user=dbUser, password=dbPasswd, host=dbHost,
                             database=dbName)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Search (query, maxPrice, minPrice," +
                   "maxBidPrice, distance, zipCode, link) " +
                   "VALUES (%s, %s, %s, %s, %s, %s, %s)", (title,
                                                           maxPrice,
                                                           minPrice,
                                                           maxBidPrice,
                                                           distance,
                                                           zipCode,
                                                           link))
    conn.commit()
    cursor.close()
    conn.close()


def deleter(dbID, isAdvert):
    conn = connector.connect(user=dbUser, password=dbPasswd, host=dbHost,
                             database=dbName)
    cursor = conn.cursor()
    try:
        bool(isAdvert)
        int(dbID)
        if isAdvert == 'True':
            cursor.execute("DELETE FROM Advert WHERE advertID = %s;",
                           (dbID,))
            conn.commit()
        if isAdvert == 'False':
            cursor.execute("DELETE FROM Search WHERE searchID = %s;",
                           (dbID,))
            conn.commit()
    except ValueError:
        pass
    except TypeError:
        pass
    cursor.close()
    conn.close()
