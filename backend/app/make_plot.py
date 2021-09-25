import numpy as np
import pandas as pd
import json

from bokeh.layouts import column, row
from bokeh.models import ColumnDataSource, RangeTool
from bokeh.plotting import figure, show
from bokeh.embed import json_item

def make_dummy_plot():
    # copy/pasted from Bokeh Getting Started Guide
    x = np.linspace(-6, 6, 100)
    y = np.cos(x)
    p = figure(width=500, height=500, toolbar_location="below",
                     title="Plot 1")
    p.circle(x, y, size=7, color="firebrick", alpha=0.5)
 
    # following above points: 
    #  + pass plot object 'p' into json_item
    #  + wrap the result in json.dumps and return to frontend
    return json.dumps(json_item(p, "myplot"))



def make_sensor_plot():

    # dummy data
    distance = np.arange(970,4280, 10).tolist()
    # could replace with elevation
    y = np.zeros(len(distance), dtype=int)
    lat = distance + (np.random.rand(len(distance)) * 10)
    long = (lat / 2)
    data_dict = {"distance":distance,
                            "y":y,
                            "lat":lat,
                            "long":long
                        }
    df = pd.DataFrame(data=data_dict)

    source = ColumnDataSource(data=df)


    main_fig_dims = (300,800)
    p = figure(height=main_fig_dims[0], width=main_fig_dims[1],        
            tools="xpan", toolbar_location=None,
            x_axis_location="above",
            background_fill_color="#efefef", x_range=(distance[10], distance[-1]))

    p.line('distance', 'y', source=source)
    p.xaxis.axis_label = "track distance (m)"


    geo_pos = figure(height=main_fig_dims[0], width=main_fig_dims[0],
            tools="xpan", toolbar_location=None,
            x_axis_location="above",
            background_fill_color="#efefef", 
            x_range=(lat[0], lat[-1],))

    geo_pos.line('lat', 'long',color="black", source=source)
    # update this with slider
    geo_pos.circle(lat[50], long[50], size=10, color="black")
    geo_pos.xaxis.axis_label = "location overview"


    select = figure(title="Drag to view sections of track",
                    height=50, width=800, y_range=[-1,1],
                    x_axis_type=None, y_axis_type=None,
                    tools="", toolbar_location=None, background_fill_color="#efefef")

    range_tool = RangeTool(x_range=p.x_range)
    range_tool.overlay.fill_color = "navy"
    range_tool.overlay.fill_alpha = 0.2

    select.line('distance', 'y', source=source)
    select.ygrid.grid_line_color = None
    select.add_tools(range_tool)
    select.toolbar.active_multi = range_tool

    layout = row(column(p, select), geo_pos)
    
    return json.dumps(json_item(layout, "sensor_plot"))
