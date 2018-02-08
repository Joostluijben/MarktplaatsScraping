from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from jsondb.db import Database
import time
db = Database('articles.db')
#driver = webdriver.Chrome('/home/joost/Downloads/chromedriver')
def addSearch():
    newSearch = input('Voer een nieuwe zoekopdracht in: ')
    while True:
        try:
            articleMax = str(int(input('Voer de MAXIMALE zoekprijs in voor advertenties: ')))
            articleMin = str(int(input('Voer de MINIMALE zoekprijs in voor advertenties: ')))
            biddingMax = str(int(input('Voer de MAXIMALE zoekrpijs in voor bieden: ')))
            distance = str(int(input('Voer een afstand in meters in(getal). Dus 1 km is 1000: ')))
        except ValueError:
            print('Een van de ingevulde waardes is geen getal!')
            continue
        else:
            break
    zipCode = input('Geef de postcode op vanaf waar u wilt zoeken: ')
    searches = []
    opener = open('searches.txt')
    for line in opener:
        searches.append(tuple(line.strip().split(',')))
    opener.close()
    while True:
        if tuple((newSearch, articleMax, articleMin, biddingMax, distance, zipCode)) not in searches:
            writer = open('searches.txt', 'a+')
            searchCritiria = (newSearch, articleMax, articleMin, biddingMax, distance, zipCode)
            writer.write(",".join(searchCritiria)+'\n')
            writer.close()
            break
        else:
            print('Deze zoekcriteria bestaat al, geef een andere op')
            pass
    return searches
def readSearches():
    searches = []
    opener = open('searches.txt')
    for line in opener:
        searches.append(tuple(line.strip().split(',')))
    opener.close()
    return searches
