from bokeh.layouts import column
from bokeh.plotting import figure, curdoc
from bokeh.models import ColumnDataSource
import numpy as np

# gauges 
channels = ['Main', 'Pool', 'Heater']
counts = [1,3,2]
source = ColumnDataSource(dict(channels=channels, counts=counts))
p2 = figure(x_range=channels, 
            plot_height=250, title='Current power',
            y_range=(0,5))
p2.vbar(top='counts',
        x='channels',
        source = source,
        width=0.9)
p2.yaxis.axis_label='Power (kW)'

def update():
    rnd = np.random.normal(1,0.2,3)
    print(rnd)
    new_counts = np.array(counts)*rnd
    print(new_counts)
    source.data.update({'channels':channels,'counts':new_counts})

curdoc().add_root(p2)
curdoc().add_periodic_callback(update, 500)
