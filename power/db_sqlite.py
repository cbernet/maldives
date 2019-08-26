import sqlite3
import os

db_fname = os.path.join(os.environ['HOME'], 'power.db')
conn = sqlite3.connect(db_fname)

def cmd(func):
    '''decorator ensuring that the cursor is properly opened and closed'''
    def wrapped(*args, **kwargs):
        crs = conn.cursor()
        results = func(crs, *args, **kwargs)
        crs.close()
        return results
    return wrapped

@cmd
def create_db():
    '''Create database and adc table'''
    crs.execute('''
CREATE TABLE adc (
    time integer, 
    channel integer, 
    rms real, 
    mean real, 
    minadc integer, 
    maxadc integer,
    PRIMARY KEY (time, channel)
);
''')

@cmd
def create_index(crs):
    '''create an index for efficient selection on time, channel'''
    crs.execute(
'''
CREATE UNIQUE INDEX idx_time ON adc (
    time, channel
);
'''
    )
    
@cmd
def dump(crs):
    '''print schema'''
    crs.execute(
'''
SELECT sql FROM sqlite_master;
'''
    )
    for res in crs.fetchall():
        if res:
            print(res[0])

@cmd
def migrate_from_mongo(crs):
    import pymongo
    client = pymongo.MongoClient('localhost',27017)
    mg_db = client['power']
    mg_adc = mg_db['adc']
    cursor = mg_adc.find()
    for i,rcd in enumerate(cursor):
        sqlcmd = '''
INSERT INTO adc VALUES (
        {time},
        {channel},
        {rms},
        {mean},
        {minadc},
        {maxadc}
);
'''.format( time=rcd['time'],
            channel=rcd['channel'],
            rms=rcd['rms'],
            mean=rcd['mean'],
            minadc=rcd['minadc'],
            maxadc=rcd['maxadc'] )
        # print(sqlcmd)
        crs.execute(sqlcmd)
        if i%10000==0:
            print(i)
            conn.commit()

@cmd
def insert(crs, summary):
    crs.execute(
'''
INSERT INTO adc (time, channel, rms, mean, minadc, maxadc)
VALUES ({time}, {channel}, {rms}, {mean}, {minadc}, {maxadc})
'''.format( time=summary['time'],
            channel=summary['channel'],
            rms=summary['rms'],
            mean=summary['mean'],
            minadc=summary['minadc'],
            maxadc=summary['maxadc'] )
    )
    conn.commit()

if __name__ == '__main__':
    migrate_from_mongo()
