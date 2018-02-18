from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from jsondb.db import Database
from bs4 import BeautifulSoup
import requests
import time
db = Database('articles.db')


def readSearches():
    searches = []
    opener = open('searches.txt')
    next(opener)
    for line in opener:
        searches.append(tuple(line.strip().split(',')))
    opener.close()
    searches = sorted(searches)
    return searches
