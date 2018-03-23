from flask import render_template
from flask import Flask
from flask import request
from bs4 import BeautifulSoup
import requests
from flask import redirect
from flask import url_for
from flask import session
import mysql.connector
import datetime
from dbManager import addSearch
from dbManager import deleter
import re

dbUser = 'joost'
dbPasswd = 'passwd'
dbHost = 'localhost'
dbName = 'marktplaats'
connector = mysql.connector

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def main():
    conn = connector.connect(user=dbUser, password=dbPasswd, host=dbHost, database=dbName)
    cursor = conn.cursor()
    searches = []
    adverts = []
    cursor.execute("SELECT * FROM Search")
    for search in cursor.fetchall():
        search = list(search)
        search[5] = search[5] / 1000
        search = tuple(search)
        searches.append(search)
    cursor.execute("SELECT * FROM Advert")
    for advert in cursor.fetchall():
        advert = list(advert)
        advert[3] = datetime.datetime.strftime(advert[3], "%d-%m-%Y")
        advert = tuple(advert)
        adverts.append(advert)
    if request.method == 'POST':
        if request.form['submit'] == 'Nieuwe zoekopdracht':
            return redirect(url_for('add'))
    cursor.close()
    conn.close()
    return render_template('index.html', searches=searches, adverts=adverts)


@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        search = request.form['search']
        try:
            articleMax = float(request.form['articleMax'])
            articleMin = float(request.form['articleMin'])
            biddingMax = float(request.form['biddingMax'])
            distance = int(request.form['distance'])
            distance = distance * 1000
        except ValueError:
            return redirect('/')
        zipCode = request.form['zipCode']
        getNewSearch = requests.get('https://www.marktplaats.nl/z.html?query='
                                    + str(search.replace(' ', '+')))
        session['newSearch'] = [search, articleMax, articleMin, biddingMax,
                                distance, zipCode, getNewSearch.url]
        newSearchSoup = BeautifulSoup(getNewSearch.content, 'lxml')
        firstCategoriesCoded = newSearchSoup.find_all('a',
                                                      class_='category-name')
        session['firstCategories'] = [str(category)
                                      for category in firstCategoriesCoded]
        firstCategories = [category.text for category in firstCategoriesCoded]
        return render_template('firstCategories.html',
                               firstCategories=firstCategories)
    return render_template('add.html')


@app.route('/secondCategories', methods=['GET', 'POST'])
def secondCategories():
    if request.method == 'POST':
        index = int(request.form['firstCategory'])
        if index != 0:
            soup = BeautifulSoup(str(session.get('firstCategories')),
                                 'html.parser')
            texts = soup.find_all('a')
            links = []
            for text in texts:
                links.append(text.get('href'))
            getSecondCategory = requests.get(links[index-1])
            session['firstCategory'] = links[index-1]
            secondCategorySoup = BeautifulSoup(getSecondCategory.content,
                                               'lxml')
            secondCategoriesCoded = secondCategorySoup.select('li.level-two')
            session['secondCategories'] = [
                str(category) for category in secondCategoriesCoded]
            secondCategories = [category.text
                                for category in secondCategoriesCoded]
            return render_template('secondCategories.html',
                                   secondCategories=secondCategories)
        else:
            info = session.get('newSearch')
            info[6] = info[6] + '&postcode=' + info[5]
            addSearch(info[0], info[1], info[2], info[3], info[4],
                      info[5], info[6])
            return redirect(url_for('process'))
    return render_template('secondCategories.html')


@app.route('/process', methods=['POST', 'GET'])
@app.route('/process/<isAdvert>/<dbID>', methods=['POST', 'GET'])
def process(isAdvert=None, dbID=None):
    deleter(dbID=dbID, isAdvert=isAdvert)
    if request.method == 'POST':
        conn = connector.connect(user=dbUser, password=dbPasswd, host=dbHost,
                                 database=dbName)
        cursor = conn.cursor()
        index = int(request.form['secondCategory'])
        if index != 0:
            soup = BeautifulSoup(str(session.get('secondCategories')),
                                 'html.parser')
            texts = soup.find_all('a')
            links = []
            for text in texts:
                links.append(text.get('href'))
            link = links[index-1]
            info = session.get('newSearch')
            cursor.close()
            conn.close()
            addSearch(info[0], info[1], info[2], info[3], info[4],
                      info[5], link)
        else:
            link = session.get('firstCategory')
            info = session.get('newSearch')
            addSearch(info[0], info[1], info[2], info[3], info[4],
                      info[5], link)
            cursor.close()
            conn.close()
            return redirect(url_for('process'))
        cursor.close()
        conn.close()
    return render_template('process.html')


@app.route('/change/<changeHead>/<dbID>', methods=['POST', 'GET'])
def change(changeHead, dbID):
    if request.method == 'POST':
        conn = connector.connect(user=dbUser, password=dbPasswd, host=dbHost,
                                 database=dbName)
        changing = request.form['changing']
        cursor = conn.cursor()

        if (changeHead == 'maxPrice' or changeHead == 'minPrice'
                or changeHead == 'maxBidPrice' or changeHead == 'distance'):
            try:
                changing = int(changing)
                if changeHead == 'distance':
                    changing = changing * 1000
                    pass
                cursor = conn.cursor()
                sql = """UPDATE Search SET {} = %s WHERE searchID = %s""".format(changeHead)
                cursor.execute(sql, (changing, dbID,))
                conn.commit()
                return redirect('/')
            except ValueError:
                pass
                return redirect('/')
            except TypeError:
                pass
                return redirect('/')
        elif changeHead == 'zipCode':
            try:
                str(changeHead)
            except ValueError:
                return redirect('/')
            cursor = conn.cursor()
            sql = """UPDATE Search SET {} = %s WHERE searchID = %s""".format(changeHead)
            cursor.execute(sql, (changing, dbID,))
            conn.commit()
            return redirect('/')
        cursor.close()
        conn.close()
    return render_template('changing.html', changeHead=changeHead)


@app.route('/getInclude/<searchID>/', methods=['GET', 'POST'])
@app.route('/getInclude/<searchID>/<includedID>', methods=['GET', 'POST'])
def getInclude(searchID, includedID=None):
    try:
        int(searchID)
    except TypeError:
        return redirect('/')
    except ValueError:
        return redirect('/')
    conn = connector.connect(user=dbUser, password=dbPasswd, host=dbHost,
                             database=dbName)
    cursor = conn.cursor()
    sql = "SELECT include, Included.includedID FROM Included, Search, SearchIncluded WHERE Search.searchID = %s AND SearchIncluded.searchID = Search.searchID AND Included.includedID = SearchIncluded.includedID;"
    cursor.execute(sql, (searchID,))
    includes = cursor.fetchall()
    if request.method == 'POST':
        if request.form['submit'] == 'Verwijder':
            cursor = conn.cursor()
            getSql = "SELECT Included.includedID FROM Included, Search, SearchIncluded WHERE Search.searchID = %s AND Included.includedID = %s AND SearchIncluded.searchID = Search.searchID AND Included.includedID = SearchIncluded.includedID"
            cursor.execute(getSql, (searchID, includedID,))
            deleteID = int(cursor.fetchone()[0])
            cursor.execute("DELETE FROM Included WHERE includedID = %s", (deleteID,))
            conn.commit()
            return redirect(url_for('getInclude', searchID=searchID))
        elif request.form['submit'] == 'Voeg nieuw woord toe':
            cursor = conn.cursor()
            newInclude = request.form['newInclude']
            insertSql = "INSERT INTO Included(include) VALUES(%s)"
            cursor.execute(insertSql, (newInclude,))
            conn.commit()
            secondInsertSql = "INSERT INTO SearchIncluded(searchID, includedID) VALUES (%s, %s)"
            cursor.execute(secondInsertSql, (searchID, cursor.lastrowid))
            conn.commit()
            return redirect(url_for('getInclude', searchID=searchID))
    return render_template('include.html', includes=includes, searchID=searchID)


@app.route('/getExclude/<searchID>/', methods=['GET', 'POST'])
@app.route('/getExclude/<searchID>/<excludedID>', methods=['GET', 'POST'])
def getExclude(searchID, excludedID=None):
    try:
        int(searchID)
    except TypeError:
        return redirect('/')
    except ValueError:
        return redirect('/')
    conn = connector.connect(user=dbUser, password=dbPasswd, host=dbHost,
                             database=dbName)
    cursor = conn.cursor()
    sql = "SELECT exclude, Excluded.excludedID FROM Excluded, Search, SearchExcluded WHERE Search.searchID = %s AND SearchExcluded.searchID = Search.searchID AND Excluded.excludedID = SearchExcluded.excludedID;"
    cursor.execute(sql, (searchID,))
    excludes = cursor.fetchall()
    if request.method == 'POST':
        if request.form['submit'] == 'Verwijder':
            cursor = conn.cursor()
            getSql = "SELECT Excluded.excludedID FROM Excluded, Search, SearchExcluded WHERE Search.searchID = %s AND Excluded.ExcludedID = %s AND SearchExcluded.searchID = Search.searchID AND Excluded.ExcludedID = SearchExcluded.ExcludedID"
            cursor.execute(getSql, (searchID, excludedID,))
            deleteID = int(cursor.fetchone()[0])
            cursor.execute("DELETE FROM Excluded WHERE excludedID = %s", (deleteID,))
            conn.commit()
            return redirect(url_for('getExclude', searchID=searchID))
        elif request.form['submit'] == 'Voeg nieuw woord toe':
            cursor = conn.cursor()
            newExclude = request.form['newExclude']
            insertSql = "INSERT INTO Excluded(exclude) VALUES(%s)"
            cursor.execute(insertSql, (newExclude,))
            conn.commit()
            secondInsertSql = "INSERT INTO SearchExcluded(searchID, excludedID) VALUES (%s, %s)"
            cursor.execute(secondInsertSql, (searchID, cursor.lastrowid))
            conn.commit()
            return redirect(url_for('getExclude', searchID=searchID))
    return render_template('exclude.html', excludes=excludes, searchID=searchID)

app.secret_key = 'Marktplaats'
app.run('0.0.0.0', 8080, debug=True, threaded=True)
