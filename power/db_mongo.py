'''Not used but kept for future reference
'''

import pymongo
import time

class MongoCollection(object):

    client = pymongo.MongoClient('localhost',27017)
    
    def __init__(self, collname, dbname='power'):
        self.collection = self.__class__.client[dbname][collname]  

    def time_query(self, hmin, hmax=None):
        '''returns mongo query for entries between now-hmin and now-hmax'''
        now = time.time()
        t1 = now - 3600*hmin
        t2 = now
        if hmax:
            t2 = now - 3600*hmax
            query = { '$and': [{'time': {'$gt':t1}},
                               {'time': {'$lt':t2}}]}
        else: 
            query = {'time': {'$gt':t1}}
        return query

        
    def time_find(self, hmin, hmax=None):
        '''returns entries between now-hmin and now-hmax'''
        query = self.time_query(hmin, hmax)
        cursor = self.collection.find(query)
        data = list(cursor)
        return data

    def time_remove(self, hmin, hmax=None):
        '''remove entries between now-hmin and now-hmax'''
        query = self.time_query(hmin, hmax)
        self.collection.remove(query)
