import pymongo 
import math
import time

# define the client, the database, and the collection
# the database and the collection are created at first insert 
# if needed
client = pymongo.MongoClient('localhost',27017)
mydb = client["test"]
sinfun = mydb["sin"]
sinfun.remove({})
print('insert')
for i in range(1000):
    x = i/10.
    y = math.sin(x)
    print(x,y)
    sinfun.insert({'x':x,'y':y})
    time.sleep(0.5)
# the list of records is written to the database in one go:
print('done')