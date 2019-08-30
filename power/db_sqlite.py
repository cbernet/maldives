import sqlite3
import os

# default connection to main db: 
db_fname = os.path.join(os.environ['HOME'], 'power.db')
conn = sqlite3.connect(db_fname)

def connect(fname):
    '''connect to a db, possibly different from the main one'''
    global db_fname, conn
    db_fname = fname
    conn = sqlite3.connect(db_fname)

    
def disconnect():
    '''close current connection'''
    conn.close()

    
def cmd(func):
    '''decorator ensuring that the cursor is properly opened and closed'''
    def wrapped(*args, **kwargs):
        crs = conn.cursor()
        results = func(crs, *args, **kwargs)
        crs.close()
        return results
    return wrapped


@cmd
def create_db(crs, fname):
    '''create database, 
    with the adc, hour, and day tables.
    used to create both the main and test databases
    '''
    pass

@cmd
def create_table(crs, tablename='adc'):
    '''Create table (adc by default).
    time, minadc, maxadc are stored as real and not integers, 
    because raw data will be averaged (to real) in the hour
    table
    '''
    crs.execute('''
CREATE TABLE {} (
    time real, 
    channel integer, 
    rms real, 
    mean real, 
    minadc real, 
    maxadc real,
    PRIMARY KEY (time, channel)
);'''.format(tablename)
)

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
    '''insert summary dict as a record.
    '''
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
