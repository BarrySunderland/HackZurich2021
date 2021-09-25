import numpy as np
import pandas as pd
from bokeh.io import curdoc
from bokeh.layouts import column, row

from bokeh.models import ColumnDataSource, Slider, TextInput, DateRangeSlider, NumeralTickFormatter
from bokeh.plotting import figure

# Set up data
# N = 200
# x = np.linspace(0, 4*np.pi, N)
# y = np.sin(x)
# source = ColumnDataSource(data=dict(x=x, y=y))


# GET DATA
fpath = '../data-processing/data/interim/rssi_sample.csv'
df = pd.read_csv(fpath, parse_dates=['DateTime'])
df = df.set_index('DateTime')

print('df',df.head())

start_date = df.index.min()
end_date = df.index.max()
print("start_date: ", start_date)
print("end_date: ", end_date)
SOURCE = ColumnDataSource(data=df)



# Set up plot
# plot = figure(height=200, width=200, title="sine wave",
#               tools="crosshair,pan,reset,save,wheel_zoom",
#               x_range=[0, 4*np.pi], y_range=[-2.5, 2.5])

# plot.line('x', 'y', source=source, line_width=3, line_alpha=0.6)


p = figure(height=400, width=800, title="sensor",
              tools="crosshair,pan,reset,save,wheel_zoom",
             )

y_col='A2_RSSI'
p.line('PositionNoLeap', y_col, 
        legend_label=y_col,
        line_width=3, line_alpha=0.6,
        source=SOURCE
        )


# y_col='A2_ValidTel'
# p.line('PositionNoLeap', y_col, 
#         legend_label=y_col,
#         line_width=3, line_alpha=0.6,
#         source=SOURCE
        # )


p.xaxis.axis_label = 'Track Distance (m)'
p.yaxis.axis_label = 'Mean Value'
p.legend.location = "top_left"
p.legend.click_policy="hide"
p.xaxis[0].formatter = NumeralTickFormatter(format="0")  



# Set up widgets
date_range_slider = DateRangeSlider(value=(start_date, end_date),
                                    start=start_date, 
                                    end=end_date,
                                    )

text = TextInput(title="title", value="dates: ")
offset = Slider(title="offset", value=0.0, start=-5.0, end=5.0, step=0.1)
amplitude = Slider(title="amplitude", value=1.0, start=-5.0, end=5.0, step=0.1)
phase = Slider(title="phase", value=0.0, start=0.0, end=2*np.pi)
freq = Slider(title="frequency", value=1.0, start=0.1, end=5.1, step=0.1)


# Set up callbacks
def update_title(attr, old, new):
    p.title.text = text.value

text.on_change('value', update_title)

def filter_data(df, min_date, max_date):

    fltr = df.index.to_series().between(min_date, max_date)
    return df.loc[fltr,:]

def update_data(attr, old, new):

    # Get the current slider values
    d = date_range_slider.value_as_datetime
    a = amplitude.value
    b = offset.value
    w = phase.value
    k = freq.value
    print("date range: ",d)

    # Generate the new curve
    min_date = pd.to_datetime(d[0])
    max_date = pd.to_datetime(d[1])
    # print("date range: ", min_date,",", min_date)

    SOURCE.data = filter_data(df, min_date, max_date)


for w in [offset, amplitude, phase, freq, date_range_slider]:
    w.on_change('value', update_data)


# Set up layouts and add to document
inputs = column(text, date_range_slider, offset, amplitude, phase, freq)
inputs = column(date_range_slider,)
layout = column(
                # row(inputs, plot, width=800),
                row(inputs, p, width=1600))
curdoc().add_root(layout)

curdoc().title = "Sliders"
