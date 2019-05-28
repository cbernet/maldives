from bokeh.layouts import column
from bokeh.plotting import figure, curdoc
from bokeh.models import ColumnDataSource, HoverTool

import numpy as np
import pandas as pd
from datetime import datetime

# set up data
xfirst = 0
dx = 0.1
npoints = 10
rollover = 2000
x = np.linspace(xfirst, xfirst+dx, npoints)
y = np.sin(x)
source = ColumnDataSource(data=dict(x=x, y=y))

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
    global xfirst
    xfirst = xfirst+dx
    x = np.linspace(xfirst, xfirst+dx, npoints)
    y = np.sin(x)
    source.stream({'x':x, 'y':y}, rollover)

curdoc().add_root(p1)
curdoc().add_periodic_callback(update, 50)

