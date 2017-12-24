from jsondb.db import Database
import time
db = Database('articles.db')
lst = [{'price' : 'Bieden'}, {'price' : 10}]
for row in lst:
    if row['price'] == 'Bieden':
        row['price'] = 10
print(lst)
print(db['iphone 6'])
