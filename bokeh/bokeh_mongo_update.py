from bokeh.layouts import column
from bokeh.plotting import figure, curdoc
from bokeh.models import ColumnDataSource, HoverTool

import numpy as np
import pandas as pd
from datetime import datetime

import pymongo
client = pymongo.MongoClient('localhost',27017)
sinfun = client.test.sin

cursor = sinfun.find()
data = list(cursor)
last_id = data[-1]['_id']
df = pd.DataFrame(data)
del df['_id']
source = ColumnDataSource(df)

hover = HoverTool(
        tooltips=[
            ("x", "$x"),
            ("y", "$y")
        ],
    )
tools = [hover,'box_zoom','undo','reset']
p1 = figure(plot_width=800, plot_height=400, 
            tools=tools)
p1.line(x='x', y='y', source=source)
p1.xaxis.axis_label='x'
p1.yaxis.axis_label='y'

def update():
    global last_id
    cursor = sinfun.find({'_id':{'$gt':last_id}})
    data = list(cursor)
    if len(data):
        print('streaming data', len(data))
        last_id = data[-1]['_id']
        df = pd.DataFrame(data)
        del df['_id']
        source.stream(df)

curdoc().add_root(p1)
curdoc().add_periodic_callback(update, 1000)

