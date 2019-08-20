from bokeh.layouts import column
from bokeh.plotting import figure, curdoc
from bokeh.models import ColumnDataSource, HoverTool

import pandas as pd
from datetime import datetime

# set up data

import pymongo
client = pymongo.MongoClient('localhost',27017)
db = client.test
sinfun = db.sin

cursor = sinfun.find()
df = pd.DataFrame(list(cursor))
del df['_id']

hover = HoverTool(
        tooltips=[
            ("x", "$x"),
            ("y", "$y")
        ],
    )
tools = [hover,'box_zoom','undo','reset']

source = ColumnDataSource(df)
p1 = figure(plot_width=800, plot_height=400, 
            tools=tools)
p1.line(x='x', y='y', source=source)
p1.xaxis.axis_label='x'
p1.yaxis.axis_label='y'

curdoc().add_root(p1)
