import pymongo 
import math

# define the client, the database, and the collection
# the database and the collection are created at first insert 
# if needed
client = pymongo.MongoClient('localhost',27017)
mydb = client["test"]
sinfun = mydb["sin"]

print('insert')
data = []
for i in range(100):
    x = i/10.
    y = math.sin(x)
    data.append({'x':x,'y':y})
# the list of records is written to the database in one go:
sinfun.insert_many(data)
print('done')