from bokeh.layouts import column
from bokeh.plotting import figure, curdoc
from bokeh.models import ColumnDataSource, HoverTool

import numpy as np
import pandas as pd
from datetime import datetime, timedelta

import pymongo

def preprocess_df(df):
    del df['_id']
    df['timeparis'] = df['time'] + 3600*2*1000
    df['dt'] = pd.to_datetime(df['timeparis'],unit='ms')
    df['rms'] = df['/home/power/rms/0']
    df['minadc'] = df['/home/power/minadc/0']
    df['maxadc'] = df['/home/power/maxadc/0']
    df['power'] = df['rms'] * 237 * 0.27 / 1000.

client = pymongo.MongoClient('rasphome.lan',27017)
db = client.sensors
power = db.home_power_0

nhours = 2
now = datetime.now()
t1 = now - timedelta(hours=nhours)
tt1 = datetime.timestamp(t1)*1000

cursor = power.find({'time': {'$gt':tt1}})
data = list(cursor)
last_id = data[-1]['_id']
df = pd.DataFrame(data)
preprocess_df(df)

source = ColumnDataSource(df)

hover = HoverTool(
        tooltips=[
            ("x", "$x"),
            ("y", "$y")
        ],
    )
tools = [hover,'box_zoom','undo','reset']
p1 = figure(x_axis_type='datetime', plot_width=800, plot_height=400, 
           tools=tools)
p1.line(x='dt', y='power', source=source)
p1.xaxis.axis_label='Time'
p1.yaxis.axis_label='Power (kW)'

def update():
    global last_id
    cursor = power.find({'_id':{'$gt':last_id}})
    data = list(cursor)
    if len(data):
        print('streaming data', len(data))
        last_id = data[-1]['_id']
        df = pd.DataFrame(data)
        preprocess_df(df)
        source.stream(df)

curdoc().add_root(p1)
curdoc().add_periodic_callback(update, 1000)
