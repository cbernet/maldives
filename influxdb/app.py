from influxdb import InfluxDBClient
import requests

import time
import datetime
import math
import pprint
import os
import signal
import sys

client = None
dbname = 'mydb'
measurement = 'sinwave'


def db_exists():
    '''returns True if the database exists'''
    dbs = client.get_list_database()
    for db in dbs:
        if db['name'] == dbname:
            return True
    return False

def wait_for_server(host, port, nretries=5, waiting_time=1):
    '''wait for the server to come online for waiting_time, nretries times.'''
    url = 'http://{}:{}'.format(host, port)
    for i in range(nretries):
        try:
            requests.get(url)
            return 
        except requests.exceptions.ConnectionError:
            print('waiting for', url)
            time.sleep(waiting_time)
            pass
    print('cannot connect to', url)
    sys.exit(1)

def connect_db(host, port, reset):
    '''connect to the database, and create it if it does not exist'''
    global client
    print('connecting to database: {}:{}'.format(host,port))
    client = InfluxDBClient(host, port, retries=5, timeout=1)
    wait_for_server(host, port)
    create = False
    if not db_exists():
        create = True
        print('creating database...')
        client.create_database(dbname)
    else:
        print('database already exists')
    client.switch_database(dbname)
    if not create and reset:
        client.delete_series(measurement=measurement)

    
def measure(nmeas):
    '''insert dummy measurements to the db.
    nmeas = 0 means : insert measurements forever. 
    '''
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
    '''returns all entries in the database.'''
    results = client.query('select * from {}'.format(measurement))
    # we decide not to use the x tag
    return list(results[(measurement, None)])

    
if __name__ == '__main__':
    import sys
    
    from optparse import OptionParser
    parser = OptionParser('%prog [OPTIONS] <host> <port>')
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
    if len(args)!=2:
        parser.print_usage()
        print('please specify two arguments')
        sys.exit(1)
    host, port = args
    connect_db(host, port, options.reset)
    def signal_handler(sig, frame):
        print()
        print('stopping')
        pprint.pprint(get_entries())
        sys.exit(0)
    signal.signal(signal.SIGINT, signal_handler)

    measure(options.nmeasurements)
        
    pprint.pprint(get_entries())

