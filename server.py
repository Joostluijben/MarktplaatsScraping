from flask import render_template
from flask import Flask
from jsondb.db import Database
from searchManager import readSearches
from itertools import zip_longest
from flask import request
from jsondb.db import Database
from bs4 import BeautifulSoup
import requests
from flask import redirect
from flask import url_for
from flask import session

app = Flask(__name__)
db = Database('/home/joost/Documents/Markplaats_prototype/http/articles.db')


@app.route('/', methods=['GET', 'POST'])
def main():
    articles = []
    for search in db:
        articles.append([article for article in db[search]])
    searches = readSearches()
    if request.method == 'POST':
        if request.form['submit'] == 'Nieuwe zoekopdracht':
            return redirect(url_for('add'))
    return render_template('index.html', searches=searches, articles=articles)


@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        search = request.form['search']
        articleMax = request.form['articleMax']
        articleMin = request.form['articleMin']
        biddingMax = request.form['biddingMax']
        distance = request.form['distance']
        zipCode = request.form['zipCode']
        getNewSearch = requests.get('https://www.marktplaats.nl/z.html?query='
                                    + str(search.replace(' ', '+')) +
                                    '&distance=' + str(distance)
                                    + '&postcode='
                                    + str(zipCode))
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
            print(link)
        else:
            return redirect(url_for(''))
    return render_template('process.html')


app.secret_key = 'Marktplaats'
app.run('0.0.0.0', 8080, debug=True, threaded=True)
