from bokeh.layouts import column
from bokeh.plotting import figure, curdoc
from bokeh.models import ColumnDataSource, HoverTool, Range1d, Label

import numpy as np
import pandas as pd
# from datetime import datetime, timedelta
import time

import pymongo
import math
import sys

def preprocess_df(df):
    del df['_id']
    df['timeparis'] = df['time'] + 3600*2
    df['dt'] = pd.to_datetime(df['timeparis'],unit='s')
    df['power'] = df['rms'] * 237 * 0.27 / 1000.

client = pymongo.MongoClient('localhost',27017)
mydb = client['power']
adc = mydb['adc']

nhours = 0.5
now = time.time()
t1 = now - 3600*nhours

cursor = adc.find({'time': {'$gt':t1}})
data = list(cursor)
last_id = data[-1]['_id']
df = pd.DataFrame(data)
# print(df.head)
# sys.exit(1)

preprocess_df(df)

source = ColumnDataSource(df)

# history plot 
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

p = figure(width=400, height=200, tools=[])

maxv = 10
def angle(x):
    x = min(x,maxv)
    return (1-x/maxv)*math.pi
value = 8.1
sa = angle(value)

ds = ColumnDataSource(dict(sa=[sa],valtext=['{:3.2f}'.format(value)]))
p.annular_wedge(x=0, y=0, inner_radius=0.55, outer_radius=0.8,
                start_angle='sa', end_angle=math.pi, color="red", alpha=0.6, source = ds)

# cosmetics
p.y_range=Range1d(-0.1,1)
p.toolbar_location=None
p.axis.visible = False
p.grid.visible = False
mytext = Label(x=0, y=0, 
               text='{:3.2f}'.format(value), 
               text_font_size='50pt', text_align='center')
mytext2 = Label(x=0, y=-0.07, text='Main', text_font_size='16pt', text_align='center')
p.add_layout(mytext)
p.add_layout(mytext2)

def update():
    global last_id
    cursor = adc.find({'_id':{'$gt':last_id}})
    data = list(cursor)
    if len(data):
        print('streaming data', len(data))
        last_id = data[-1]['_id']
        df = pd.DataFrame(data)
        preprocess_df(df)
        source.stream(df)
        last_val = df['power'].values[-1]
        mytext.text = '{:3.2f}'.format(last_val)
        ds.patch({'sa':[(0,angle(last_val))]})


layout = column([p1,p])
curdoc().add_root(layout)
curdoc().add_periodic_callback(update, 1000)
