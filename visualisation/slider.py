import numpy as np
import pandas as pd

from bokeh.io import output_file
from bokeh.layouts import column
from bokeh.models import ColumnDataSource, RangeTool
from bokeh.plotting import figure, show
# from bokeh import sampledata

# sampledata.download(progress=False)
# from bokeh.sampledata.stocks import AAPL

# get data

fpath = '../data-processing/data/interim/rssi_sample.csv'
df = pd.read_csv(fpath)


# dates = np.array(AAPL['date'], dtype=np.datetime64)
x_col = 'PositionNoLeap'
x_vals = df[x_col].values

# source = ColumnDataSource(data=dict(position=x_vals, close=AAPL['adj_close']))
source = ColumnDataSource(df)


p = figure(height=300, width=800, tools="xpan", toolbar_location=None,
           x_axis_type="datetime", x_axis_location="above",
           background_fill_color="#efefef", x_range=(x_vals[0], x_vals[-1]))

p.line(x_col, 'A1_ValidTel', source=source)
p.yaxis.axis_label = 'Mean Value'

select = figure(title="Drag the middle and edges of the selection box to change the range above",
                height=130, width=800, y_range=p.y_range,
                y_axis_type=None,
                tools="", toolbar_location=None, background_fill_color="#efefef")

range_tool = RangeTool(x_range=p.x_range)
range_tool.overlay.fill_color = "navy"
range_tool.overlay.fill_alpha = 0.2

select.line(x_col, 'A1_ValidTel', source=source)
select.ygrid.grid_line_color = None
select.add_tools(range_tool)
select.toolbar.active_multi = range_tool

show(column(p, select))


output_file("./plots/slider_grouped.html")
