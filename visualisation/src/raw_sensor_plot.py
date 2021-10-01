import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output, State

import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go

import pandas as pd
import sqlite3
from time import time


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

    qry = f"""
    SELECT DateTime, PositionNoLeap, Latitude, Longitude, A1_TotalTel, A1_ValidTel, A2_RSSI, A2_TotalTel, A2_ValidTel
    FROM rssi
    WHERE PositionNoLeap > {position_start} AND PositionNoLeap <{position_end}
    LIMIT 10000;"""
    print(qry)
    con = get_conn(db_name="rssi")
    df = pd.read_sql(qry, con)
    df["DateTime"] = pd.to_datetime(df["DateTime"])
    df["PositionNoLeap"] = df["PositionNoLeap"]  / 1000
    return df


app = dash.Dash(__name__)

con = get_conn(db_name="rssi")


value_options = ["A1_TotalTel", "A1_ValidTel", "A2_RSSI", "A2_TotalTel", "A2_ValidTel"]
value_options = [{"label":v,"value":v} for v in value_options]

position_min = 322
position_max = 428
position_current = position_min
# min PositionNoLeap in database table is 322075
# min PositionNoLeap in database table is 428066
df_raw = get_raw_sensor_data(position_current*1000)

@app.callback(
    Output(component_id="graph-raw-sensor-data", component_property="figure"),
    Input(component_id="data_type_dropdown", component_property="value"),
    Input('position-slider', 'value')
)
def update_plot_2(selected_data_type, position_current):
    print("data_type_dropdown, position_slider", selected_data_type, position_current)
    df = get_raw_sensor_data(position_current*1000)
    print(df.head())
    fig = px.scatter(df,
                    x="PositionNoLeap", 
                    y=selected_data_type,
                    opacity=0.5,
                    hover_name=selected_data_type, 
                    hover_data=["DateTime", "Latitude", "Longitude"],
                    height=300,)
    fig.update_xaxes(title_text="PositionNoLeap (km)")
    fig.update_layout(transition_duration=200)

    return fig

@app.callback(
    Output('position-text', 'children'),
    Input('position-slider', 'value')
)
def update_position_text(val):
    return f"""current position: {val} kms (move using left & right key arrows"""


def update_subplots(df):
    fig = make_subplots(rows=4, cols=1,
                    shared_xaxes=True,
                    vertical_spacing=0.02)

    fig.add_trace(go.Scattergl(
                    x=df["PositionNoLeap"], 
                    y=df["A2_RSSI"],
                    mode='lines+markers',
                  ),
                row=1, 
                col=1
    )
    fig.add_trace(
        go.Scattergl(
            x=[37.4,37.4],
            y=[0,3],
            mode="lines",
            text="Actual Failure",
            line = dict(color='red', width=10),
            marker_color='rgba(255, 0, 0, .2)',
            marker_size=5,
            textposition="bottom center"
        ),
        row=1, col=1
    )
    fig.add_trace(
        go.Scattergl(
            x=[40.7,40.7],
            y=[0,1],
            mode="lines",
            text="Predicted Failure",
            textposition="bottom center",
            marker_color='rgba(255, 255, 0, .6)',
            marker_size=2,
        ),
        row=1, col=1
    )
    fig.add_trace(go.Scattergl(
                    x=df["PositionNoLeap"], 
                    y=df["A2_TotalTel"],
                    mode='markers',
                  ),
                row=2, 
                col=1
    )
    fig.add_trace(go.Scattergl(
                    x=df["PositionNoLeap"], 
                    y=df["A2_ValidTel"],
                    mode='markers',
                  ),
                row=3, 
                col=1
    )
    fig.update_layout(height=600,
                    title_text="Stacked Subplots with Shared X-Axes")
    fig.update_xaxes(title_text="PositionNoLeap (km)")

    return fig

fig_subplots = update_subplots(df_raw)

app.layout = html.Div(children=[

    dcc.Store(id='position-store'),

    html.H1(children='Siemens Track Debugger'),

    html.Div(id="subtitle", 
        children='''Dash: A web application framework for your data.'''
    ),
    dcc.Graph(
        id='graph-raw-sensor-data'
    ),
    
    html.Div(id="line", children="---------------------------------"),
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
    dcc.Dropdown(
        id="data_type_dropdown",
        options=value_options,
        value="A2_RSSI"
    ),
    dcc.Graph(id="multi", figure=fig_subplots)
])

if __name__ == '__main__':
    app.run_server(debug=True)