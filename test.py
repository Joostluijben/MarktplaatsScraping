import mysql.connector
conn = mysql.connector.connect(user='joost', password='passwd',
                               host='localhost', database='marktplaats')
thirdCursor = conn.cursor(buffered=True)

sql = "SELECT include FROM Included, Search, SearchIncluded WHERE Search.searchID = %s AND SearchIncluded.searchID = Search.searchID AND Included.includedID = SearchIncluded.includedID;"

#for i in range(2):
#    for include in thirdCursor.fetchall():
#        ''
        #print(include[0])

lst = []
for i in range(2):
    thirdCursor.execute(sql, (1,))
    lst.append([include[0] for i in range(2) for include in thirdCursor.fetchall()])

print(lst)
if any(include[0] in "test" for include in thirdCursor.fetchall()):
    print("hey")
else:
    print("goed")

#if (all(exclude not in title and exclude not in description
#                        for exclude in excluded) and
#                        any(include[0] in title for include in thirdCursor.fetchall())):
#                    insertAdvert(article, title, description, search[0],
#                                 search[2], search[3], search[4], link)
