'''Not used but kept for future reference
'''

import pandas as pd
from db_sqlite import conn
from tools import preprocess



if __name__ == '__main__':
    
    df = pd.read_sql_query('SELECT * FROM adc ORDER BY time DESC LIMIT 50000', conn)
    df = preprocess(df)
    print(df.head(1000))
    
    dfh = df.resample('H').mean()
    print(dfh)

    dfh.to_sql('hour', conn, if_exists='replace')
    
    # meanh = MongoCollection('meanh')
    # meanh.collection.insert_many(dfh.to_dict('records'))


