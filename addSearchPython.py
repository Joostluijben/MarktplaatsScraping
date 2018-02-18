from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from jsondb.db import Database
from bs4 import BeautifulSoup
import requests
import time
db = Database('articles.db')

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
    #driver.get('https://www.marktplaats.nl/z.html?query=+'+newSearch)
    getNewSearch = requests.get('https://www.marktplaats.nl/z.html?query=' + str(newSearch.replace(' ', '+')) + '&distance=' + str(distance) + '&postcode=' + str(zipCode))
    newSearchSoup = BeautifulSoup(getNewSearch.content, 'lxml')
    #firstCategories = driver.find_elements_by_xpath("//div[@id='page-wrapper']/div[@class='l-page']/section[@id='left-column-container']/div[@id='search-attributes']/form[@id='search-attributes-form']/div[@class='relevant-categories filter-section']/ul/li/a[@class='category-name']")
    firstCategories = newSearchSoup.find_all('a', class_='category-name')
    for index, category in enumerate(firstCategories):
        print(str(index+1) + ': ' + category.text)

    while True:
        try:
            firstChoice = int(input('Kies een eerste categorie: '))
            break
        except:
            print('Dat is geen getal!')
            continue
    for index, category in enumerate(firstCategories):
        if (index+1) == firstChoice:
            firstCategory = category.get('href')

    while True:
        chooseSecondCategory = input('Wilt u een tweede categorie opgeven? Kies uit ja of nee ')
        if chooseSecondCategory == 'nee':
            link = firstCategory
            break
        elif chooseSecondCategory == 'ja':
            getSecondCategory = requests.get(firstCategory)
            secondCategorySoup = BeautifulSoup(getSecondCategory.content, 'lxml')
            secondCategories = secondCategorySoup.select('li.level-two')
            for index, category in enumerate(secondCategories):
                print(str(index+1) + ': ' + (category.text).strip())
                continue
            while True:
                try:
                    secondChoice = int(input('Kies de tweede categorie: '))
                    break
                except:
                    print('Dat is geen getal')
                    continue
            for index, category in enumerate(secondCategories):
                if (index+1) == secondChoice:
                    link = category.find('a').get('href')
            break
        else:
            print('Kies uit ja of nee!')
            continue
    searches = []
    opener = open('/home/joost/Documents/Markplaats_prototype/http/searches.txt')
    next(opener)
    for line in opener:
        searches.append(tuple(line.strip().split(',')))
    opener.close()
    writer = open('/home/joost/Documents/Markplaats_prototype/http/searches.txt', 'a+')
    while True:
        if tuple((newSearch, articleMax, articleMin, biddingMax, distance, zipCode, link)) not in searches:
            searchCritiria = (newSearch, articleMax, articleMin, biddingMax, distance, zipCode, link)
            writer.write(",".join(searchCritiria)+'\n')
            break
        else:
            print('Deze zoekcriteria bestaat al, geef een andere op')
            pass
    writer.close()
    return searches
addSearch()
