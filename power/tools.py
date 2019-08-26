import pandas as pd

preferences = dict(
    dbtype='sqlite'
)

def preprocess(df, rmid=True):
    '''preprocess dataframe
    
    if rmid is True: remove unique id for bokeh display.

    add : 
    - timeparis : GMT+2
    - dt : corresponding datetime
    - power : calibrated instantaneous power from rms 

    set index to dt 
    '''
    if not len(df):
        return df
    if rmid and '_id' in df: 
        del df['_id']
    df['timeparis'] = df['time'] + 3600*2
    df['dt'] = pd.to_datetime(df['timeparis'],unit='s')
    df['power'] = df['rms'] * 237 * 0.27 / 1000.
    df = df.set_index('dt')
    return df
