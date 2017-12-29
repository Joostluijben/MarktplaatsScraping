from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from jsondb.db import Database
import time
db = Database('articles.db')
#driver = webdriver.Chrome('/home/joost/Downloads/chromedriver')
def addSearch():
    newSearch = input('Voer een nieuwe zoekopdracht in')
    searches = []
    opener = open('searches.txt')
    for line in opener:
        searches.append(line.strip())
    if newSearch not in searches:
        writer = open('searches.txt', 'a+')
        writer.write(newSearch+'\n')
    else:
        print('Already in database')
        pass
    return searches
def readSearches():
    searches = []
    opener = open('searches.txt')
    for line in opener:
        searches.append(line.strip())
    return searches
