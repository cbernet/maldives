import pandas as pd
from tools import MongoCollection, preprocess

if __name__ == '__main__':

    collection = MongoCollection('adc')

    data = collection.time_find(72)
    df = pd.DataFrame(data)

    df = preprocess(df, rmid=False)
    print(df.head())
    
    dfh = df.resample('H').mean()
    print(dfh)

    meanh = MongoCollection('meanh')
    meanh.collection.insert_many(dfh.to_dict('records'))


