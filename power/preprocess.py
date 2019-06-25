def preprocess(df):
    del df['_id']
    df['timeparis'] = df['time'] + 3600*2
    df['dt'] = pd.to_datetime(df['timeparis'],unit='s')
    df['power'] = df['rms'] * 237 * 0.27 / 1000.
