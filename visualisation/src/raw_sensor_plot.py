import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc

import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go

import pandas as pd
import sqlite3
from time import time
import json

# https://dash.plotly.com/interactive-graphing for update on hover example

def get_conn(db_name="rssi"):
    
    sqlite_path = f"../../data/processed/{db_name}.db" 
    try:
        con = sqlite3.connect(sqlite_path)
    except Exception as e:
        print(f"connection error: {e}")
    
    return con


def get_raw_sensor_data(position_start=None,
                        position_end=None,
                        date_start=None,
                        date_end=None):
    
    print(f"getting raw sensor data for {position_start}")
    if not position_end:
        position_end = position_start + 1000 

    if date_start:
        date_start = int(date_start)
    else:
        date_start = pd.to_datetime("2021-01-01").value
    if date_end:
        date_end = int(date_end)
    else:
        date_end = pd.to_datetime("2022-01-01").value

    qry = f"""
    SELECT DateTime,DateTimeInt, PositionNoLeap, Latitude, Longitude, A1_TotalTel, A1_ValidTel, A2_RSSI, A2_TotalTel, A2_ValidTel
    FROM rssi
    WHERE PositionNoLeap > :position_start AND 
          PositionNoLeap < :position_end AND
          DateTimeInt > :date_start AND
          DateTimeInt < :date_end
    LIMIT 100;
    """
    qry = f"""
    SELECT DateTime,DateTimeInt, PositionNoLeap, Latitude, Longitude, A1_TotalTel, A1_ValidTel, A2_RSSI, A2_TotalTel, A2_ValidTel
    FROM rssi
    WHERE PositionNoLeap > :position_start AND 
          PositionNoLeap < :position_end
    LIMIT 100;
    """

    con = get_conn(db_name="raw")
    qry_params = {"position_start":position_start,
                  "position_end":position_end,
                  "date_start":date_start,
                  "date_end":date_end,
                  }
    df = pd.read_sql(qry, con, params=qry_params)
    df["DateTime"] = pd.to_datetime(df["DateTime"])
    df["DateTimeInt"] = pd.to_datetime(df["DateTime"]).astype(int).values
    df["PositionNoLeap"] = df["PositionNoLeap"]  / 1000
    print(df)
    return df


dark_mode=False
TEMPLATE = "plotly_dark" if dark_mode else "plotly"
stylesheet = dbc.themes.CYBORG if dark_mode else dbc.themes.BOOTSTRAP

app = dash.Dash("ZSL Zen - sensor data", external_stylesheets=[stylesheet])

value_options = ["A1_TotalTel", "A1_ValidTel", "A2_RSSI", "A2_TotalTel", "A2_ValidTel"]
value_options = [{"label":v,"value":v} for v in value_options]

position_min = 322
position_max = 428
position_current = position_min
df_raw = get_raw_sensor_data(position_current*1000)

@app.callback(
    Output(component_id="graph-raw-sensor-data", component_property="figure"),
    Input(component_id="data_type_dropdown", component_property="value"),
    Input('position-slider', 'value')
)
def update_plot_2(selected_data_type, position_current):
    print("data_type_dropdown, position_slider", selected_data_type, position_current)
    df = get_raw_sensor_data(position_current*1000)
    # print(df.head())
    if selected_data_type in ["A1_TotalTel", "A2_TotalTel", "A1_ValidTel","A2_ValidTel",]:
        log_y_axis = True
        y_axis_title = selected_data_type + " (log)"
    else:
        log_y_axis = False
        y_axis_title = selected_data_type

    fig = px.scatter(df,
                    x="PositionNoLeap", 
                    y=selected_data_type,
                    # color=selected_data_type,
                    # color_continuous_scale="Bluered_r",
                    opacity=0.5,
                    hover_name=selected_data_type, 
                    hover_data=["DateTime", "Latitude", "Longitude"],
                    height=300,
                    log_y=log_y_axis,
                    template=TEMPLATE)
    fig.update_yaxes(title_text=y_axis_title)
    fig.update_xaxes(title_text="PositionNoLeap (km)")
    fig.update_layout(transition_duration=200)

    return fig


@app.callback(
    Output('position-text', 'children'),
    Input('position-slider', 'value')
)
def update_position_text(val):
    return f"""current position: {val} kms (adjust with arrows keys when active)"""


def update_subplots(df):
    fig = make_subplots(rows=3, cols=1,
                    shared_xaxes=True,
                    vertical_spacing=0.02,
                    )

    fig.add_trace(go.Scattergl(
                    x=df["PositionNoLeap"], 
                    y=df["A2_RSSI"],
                    mode='markers',
                    name="A2_RSSI",
                  ),
                row=1, 
                col=1
    )
    fig.add_trace(go.Scattergl(
                    x=df["PositionNoLeap"], 
                    y=df["A2_TotalTel"],
                    mode='markers',
                    name='A2_TotalTel',
                  ),
                row=2, 
                col=1
    )
    fig.add_trace(go.Scattergl(
                    x=df["PositionNoLeap"], 
                    y=df["A2_ValidTel"],
                    mode='markers',
                    name="A2_ValidTel",
                  ),
                row=3, 
                col=1
    )
    fig.add_trace(
        go.Scattergl(
            x=[322.8,322.8],
            y=[0,3],
            mode="lines",
            name="Actual Failure",
            text="Actual Failure",
            line = dict(color='red', width=8),
            textposition="bottom center"
        ),
        row=1, col=1
    )
    fig.add_trace(
        go.Scattergl(
            x=[322.5,322.5],
            y=[0,3],
            mode="lines",
            name="Predicted Failure",
            text="Predicted Failure",
            line = dict(color='yellow', width=8),
            textposition="bottom center",
        ),
        row=1, col=1
    )
    fig.update_layout(height=500,
                    title_text="Stacked Subplots with Shared X-Axes",
                    template=TEMPLATE)
    fig.update_xaxes(title_text="PositionNoLeap (km)")

    return fig

def map_plot():

    with open("../.env.mapboxtoken", "r") as f:
        mapbox_token = f.read()

    fpath = "../../data/processed/location_sorted.csv"
    df = pd.read_csv(fpath)
    df['text'] = ('position : ' + df['Position_m'].astype(str)) + ' km'

    fig = go.Figure(data=go.Scattergeo(
            lon = df['Longitude'],
            lat = df['Latitude'],
            text = df['text'],
            mode = 'markers',
            marker = dict(
                size = 8,
                opacity = 0.8,
                autocolorscale = False,
                symbol = 'circle',
                colorscale = 'Blues',
            )))
    fig.update_geos(fitbounds="locations")
    fig = px.scatter_mapbox(df, lat="Latitude", lon="Longitude", hover_data=["text",])
    fig.update_layout(autosize=True,
        hovermode='closest',
        mapbox=dict(
            accesstoken=mapbox_token,
            bearing=0,
            pitch=0,
            zoom=9.5,
        ),
        width=500,
        title = 'Map View',
        template=TEMPLATE
    )
    return fig

@app.callback(
    Output('click-info-output', 'children'),
    Input('map-plot', 'clickData'),
    Input('map-plot', 'hoverData')
)
def display_clicked_content(value_click,value_hover):
    print(value_hover)
    return json.dumps(value_click, indent=2)

@app.callback(
    Output("daterange-picker-title","children"),
    [Input('daterange-picker','start_date'),
    Input('daterange-picker','end_date'),
    ]
)
def update_date_range_filter(start_date, end_date):
    print("dates: ", start_date, end_date)

    return start_date, end_date



fig_subplots = update_subplots(df_raw)

app.layout = html.Div(style={"margin":"15px"}, children=[
    dcc.Store(id='position-store'),

    
    html.H1(children=[html.Img(src="./assets/zsl_zen_logo.png",),'Siemens Track Debugger', ], style={"margin":0}),
    # html.Div(id="subtitle", children='''Dash: A web application framework for your data.'''),
    dcc.Graph(
        id='graph-raw-sensor-data'
    ),
    html.Label(children="select data type to display", htmlFor="data_type_dropdown"),
    dcc.Dropdown(
        id="data_type_dropdown",
        options=value_options,
        value="A2_RSSI",
    ),
    html.Div(id="position-container", children=[
        html.Div(id="position-text", children="", style={"align-content":"center"}),
        dcc.Slider(
            id='position-slider',
            min=position_min,
            max=position_max,
            step=1,
            value=position_current,
        )
    ]),
    html.Div(id="daterange-picker-container", children=[
        html.Div(id="daterange-picker-title", children=[]),
        dcc.DatePickerRange(
            id="daterange-picker",
            updatemode="singledate",
            display_format="DD-MMM-YY"),
    ]),

    dcc.Graph(id="multi", figure=fig_subplots),
    dcc.Graph(id="map-plot", figure=map_plot()), 
    html.Div(id="click-info-output", children=[])
])

if __name__ == '__main__':
    app.run_server(debug=True, port=8060)