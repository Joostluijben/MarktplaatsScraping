from bs4 import BeautifulSoup
import requests
import time
firstCategoriesCoded = None
def addSearch(search, maxPrice, minPrice, maxBidPrice, distance, zipCode):
    getNewSearch = requests.get('https://www.marktplaats.nl/z.html?query=' + str(search.replace(' ', '+')) + '&distance=' + str(distance) + '&postcode=' + str(zipCode))
    newSearchSoup = BeautifulSoup(getNewSearch.content, 'lxml')
    global firstCategoriesCoded
    firstCategoriesCoded = newSearchSoup.find_all('a', class_='category-name')
    firstCategories = [category.text for category in firstCategoriesCoded]
    return firstCategoriesCoded
def getFirstCategory(index):
    return firstCategoriesCoded[int(index)]
