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

conn = mysql.connector.connect(user='joost', password='passwd',
                               host='localhost', database='marktplaats')
secondCursor = conn.cursor(buffered=True)

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def main():
    connMain = mysql.connector.connect(user='joost', password='passwd',
                                            host='localhost',
                                            database='marktplaats')
    cursor = connMain.cursor()
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
    cursor.close()
    connMain.close()
    if request.method == 'POST':
        if request.form['submit'] == 'Nieuwe zoekopdracht':
            return redirect(url_for('add'))
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
        except ValueError:
            return redirect('/')
        zipCode = request.form['zipCode']
        getNewSearch = requests.get('https://www.marktplaats.nl/z.html?query='
                                    + str(search.replace(' ', '+')) +
                                    '&distance=' + str(distance)
                                    + '&postcode='
                                    + str(zipCode))
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
            addSearch(info[0], info[1], info[2], info[3], info[4],
                      info[5], info[6])
            return redirect(url_for('process'))
    return render_template('secondCategories.html')


@app.route('/process', methods=['POST', 'GET'])
def process():
    if request.method == 'POST':
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
            addSearch(info[0], info[1], info[2], info[3], info[4],
                      info[5], link)
        else:
            link = session.get('firstCategory')
            info = session.get('newSearch')
            addSearch(info[0], info[1], info[2], info[3], info[4],
                      info[5], link)
            return redirect('/')
    return render_template('process.html')


app.secret_key = 'Marktplaats'
app.run('0.0.0.0', 8080, debug=True, threaded=True)
