import numpy as np
import pandas as pd

from bokeh.io import curdoc
from bokeh.layouts import column, row
from bokeh.models import ColumnDataSource, Slider, TextInput
from bokeh.plotting import figure

# Set up data
# N = 200
# x = np.linspace(0, 4*np.pi, N)
# y = np.sin(x)

# GET DATA
fpath = '../data-processing/data/interim/rssi_sample.csv'
df = pd.read_csv(fpath, parse_dates=['DateTime'])

start_date = df['DateTime'].min()
end_date = df['DateTime'].max()
SOURCE = ColumnDataSource(data=df)


# def make  Set up plot
p = figure(height=300, width=1500, toolbar_location="right",
            x_axis_location="above",
            background_fill_color="#efefef")

p.xaxis[0].formatter = NumeralTickFormatter(format="0")    
p.xaxis.axis_label = 'Track Distance (m)'
p.yaxis.axis_label = 'Mean Value'
p.legend.location = "top_left"
p.legend.click_policy="hide"

y_col = "A2_RSSI"

for i, track_number in enumerate([1,2,42]):
    tdf = df.loc[df['Track']==track_number,:]
    p.line(x_col, y_col, legend_label=str(track_number), color=Colorblind[8][i], line_width=2, source=SOURCE)


# Set up widgets
date_range_slider = DateRangeSlider(value=(start_date, end_date),start=start_date, end=end_date)

# text = TextInput(title="title", value='my sine wave')
# offset = Slider(title="offset", value=0.0, start=-5.0, end=5.0, step=0.1)
# amplitude = Slider(title="amplitude", value=1.0, start=-5.0, end=5.0, step=0.1)
# phase = Slider(title="phase", value=0.0, start=0.0, end=2*np.pi)
# freq = Slider(title="frequency", value=1.0, start=0.1, end=5.1, step=0.1)


# # Set up callbacks
# def update_title(attrname, old, new):
#     plot.title.text = text.value


# def update_data(attrname, old, new):

#     # Get the current slider values
#     d = date_range_slider.value
#     # a = amplitude.value
#     # b = offset.value
#     # w = phase.value
#     # k = freq.value

#     # Generate the new curve

#     SOURCE.data = dict(x=x, y=y)


# text.on_change('value', update_title)


# for w in [date_range_slider, ]: #offset, amplitude, phase, freq]:
#     w.on_change('value', update_data)


# Set up layouts and add to document
inputs = column(text, date_range_slider) # offset, amplitude, phase, freq)

curdoc().add_root(row(inputs, plot, width=800))
curdoc().title = "Sliders"