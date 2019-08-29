from influxdb import InfluxDBClient
from requests.exceptions import ConnectionError

import time
import datetime
import math
import pprint
import os
import signal

client = None
dbname = 'mydb'
measurement = 'sinwave'

def db_exists():
    for db in client.get_list_database():
        if db['name'] == dbname:
            return True
    return False

def connect_db(reset):
    '''connect to the database, and create it if it does not exist'''
    global client
    print('connecting to database')
    client = InfluxDBClient('influxdb', 8086)
    while 1:
        try: 
            print(client.get_list_database())
            break
        except ConnectionError:
            print('retrying')
            time.sleep(1)
    create = False
    if not db_exists():
        create = True
        print('creating database...')
        client.create_database(dbname)
        while not db_exists():
            time.sleep(1)
    else:
        print('database already exists')
    client.switch_database(dbname)
    if not create and reset:
        client.delete_series(measurement=measurement)

    
def measure(nmeas):
    '''insert dummy measurements to the db'''
    i = 0
    if nmeas==0:
        nmeas = sys.maxsize
    for i in range(nmeas):
        x = i/10.
        y = math.sin(x)
        data = [{
            'measurement':measurement,
            'time':datetime.datetime.now(),
            'tags': {
                'x' : x
                },
                'fields' : {
                    'y' : y
                    },
            }]
        client.write_points(data)
        pprint.pprint(data)
        time.sleep(1)

def get_entries():
    results = client.query('select * from {}'.format(measurement))
    # we decide not to use the x tag
    return list(results[(measurement, None)])

    
if __name__ == '__main__':
    import sys
    
    from optparse import OptionParser
    parser = OptionParser()
    parser.add_option(
        '-r', '--reset', dest='reset',
        help='reset database',
        default=False,
        action='store_true'
        )
    parser.add_option(
        '-n', '--nmeasurements', dest='nmeasurements',
        type='int', 
        help='reset database',
        default=0
        )
    
    options, args = parser.parse_args()
    
    connect_db(options.reset)

    def signal_handler(sig, frame):
        print()
        print('stopping')
        pprint.pprint(get_entries())
        sys.exit(0)
    signal.signal(signal.SIGINT, signal_handler)

    measure(options.nmeasurements)
        
    pprint.pprint(get_entries())

