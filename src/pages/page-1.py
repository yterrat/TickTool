#!/usr/bin/env python3
# Import packages

import dash
from dash import dcc, html, Input, Output, callback, State
import dash_daq as daq
import random

dash.register_page(__name__, path='/')

allowed_values = [0.5, 1.5, 2.5]
step_size = 0.05
pause_ticks = 20  # How many ticks to pause at each target (e.g. 10 * 100ms = 1 second)

# Initial state includes wait counter
initial_state = {
    "gauge_in1": {"current": 0.0, "target": 0.0, "wait": 0},
    "gauge_in2": {"current": 0.0, "target": 0.0, "wait": 0},
    "gauge_in3": {"current": 0.0, "target": 0.0, "wait": 0}
}

layout = html.Div([
    html.Img(src='/assets/TickTOOL_logo.png', style={'width': '40%', 'height': '40%'}, className='image-gallery'),
    html.Hr(className='orange_line'),
    html.Br(),
    html.Div([
    html.B('Evaluate your prevention strategy', style={'font-size': '60px'})
        ], style={'text-align': 'center'}),
    html.Br(),
    html.P(["The potential risk from tick bites - and how to prevent tick bites - can sometimes feel a little overwhelming",
            html.Br(),
            "Would you like to better understand your risk of being bitten by a tick and learn how to improve your tick bite prevention strategy for yourself and your family?",
           html.Br(),
           html.Br(),
           "Complete the questionnaire and receive a personalised report so you can make informed decisions and take action in a way that is right for you, to help keep you and your family safe.",
           html.Br(),
           "The questionnaire should take approximately 15 minutes to complete."],
           style={'textAlign': 'center', 'marginLeft': '20px','marginRight': '20px','fontSize': '20px'}),
    html.Br(),
    html.Div([
        html.P('Potential for BLT in environment', style={'font-size' : '25px', "font-weight": "bold"}),
        html.P('Risk of exposure', style={'font-size' : '25px', "font-weight": "bold"}),
        html.P('Level of preventive behaviours', style={'font-size' : '25px', "font-weight": "bold"})
    ], style={
        # Flexbox styling to arrange gauges horizontally
        'display': 'flex',
        'justify-content': 'space-evenly',   # Evenly distribute space between gauges
        'align-items': 'center',           # Align gauges vertically in the center
        'margin-top': '20px'
    }),
    html.Div([
        daq.Gauge(
            id='gauge_in1',
            color={"gradient": False, "ranges": {"grey": [0, 0.1], "limegreen": [0.1, 1], "orange": [1, 2], "red": [2, 3]}},
            scale={"custom": {
                0.6: {"label": "Low", 'style': {'fontSize': 20, 'fontWeight': 'bold'}},
                1.5: {"label": "Moderate", 'style': {'fontSize': 20, 'fontWeight': 'bold'}},
                2.4: {"label": "High", 'style': {'fontSize': 20, 'fontWeight': 'bold'}}
            }},
            max=3, min=0, value=0.0,
            showCurrentValue=False
        ),
        daq.Gauge(
            id='gauge_in2',
            color={"gradient": False, "ranges": {"grey": [0, 0.1], "limegreen": [0.1, 1], "orange": [1, 2], "red": [2, 3]}},
            scale={"custom": {
                0.6: {"label": "Low", 'style': {'fontSize': 20, 'fontWeight': 'bold'}},
                1.5: {"label": "Moderate", 'style': {'fontSize': 20, 'fontWeight': 'bold'}},
                2.4: {"label": "High", 'style': {'fontSize': 20, 'fontWeight': 'bold'}}
            }},
            max=3, min=0, value=0.0,
            showCurrentValue=False
        ),
        daq.Gauge(
            id='gauge_in3',
            color={"gradient": False, "ranges": {"grey": [0, 0.1], "red": [0.1, 1], "orange": [1, 2], "limegreen": [2, 3]}},
            scale={"custom": {
                0.6: {"label": "Low", 'style': {'fontSize': 20, 'fontWeight': 'bold'}},
                1.5: {"label": "Moderate", 'style': {'fontSize': 20, 'fontWeight': 'bold'}},
                2.4: {"label": "High", 'style': {'fontSize': 20, 'fontWeight': 'bold'}}
            }},
            max=3, min=0, value=0.0,
            showCurrentValue=False
        ),
    ], style={
        'display': 'flex',
        'justify-content': 'space-evenly',
        'align-items': 'center',
        'margin-top': '40px',
    }),
    html.Br(),
    html.Br(),
    html.Div(
    dcc.Link("Begin the questionnary and get you scores and personalized report", href='/page-2', style={
        'font-size': '20px',
        'text-decoration': 'none',
        'color': 'white',
        'background-color': '#FF9636',
        'padding': '10px 20px',
        'border-radius': '8px',
        'font-weight': '500',
        'display': 'inline-block'
    }),
    style={'text-align': 'center', 'margin-top': '30px'}
    ),
    #dcc.Link('Begin the questionnary and get you scores', href='/page-2', className='modern-link', style={'text-align': 'center'}),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Img(src='/assets/UdeM.png', style={'width': '20%', 'height': '20%'}, className='image-gallery'),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    dcc.Store(id='gauge-state', data=initial_state),
    dcc.Interval(id='interval', interval=100, n_intervals=0)
])



# @callback(
#     Output('record_answers', 'data',  allow_duplicate=True),
#     Input('consent', 'value'),
#     State('record_answers', 'data'),
#     prevent_initial_call=True,
# )
# def update_dic_page1(Q1, data):
#     data = data or {}
#     if Q1 is not None:
#         data['consent'] = Q1
#     return data


# @callback(
#     Output('consent', 'value'),
#     Input('record_answers', 'data')
# )
# def set_radioitem_value(data):
#     return (
#         data.get('consent', None)
#     )

@callback(
    Output('gauge_in1', 'value'),
    Output('gauge_in2', 'value'),
    Output('gauge_in3', 'value'),
    Output('gauge-state', 'data'),
    Input('interval', 'n_intervals'),
    State('gauge-state', 'data'),
    allow_duplicate=True
)
def animate_gauges(n, state):
    updated_state = {}

    def update_value(gauge_data):
        current = gauge_data["current"]
        target = gauge_data["target"]
        wait = gauge_data.get("wait", 0)

        if wait > 0:
            # Still pausing
            return {"current": current, "target": target, "wait": wait - 2}

        if abs(current - target) < step_size:
            # Target reached, start waiting and pick a new target
            new_target = random.choice([v for v in allowed_values if v != target])
            return {"current": round(target, 2), "target": new_target, "wait": pause_ticks}
        else:
            direction = 1 if target > current else -1
            new_current = round(current + direction * step_size, 2)
            return {"current": new_current, "target": target, "wait": 0}

    updated_state["gauge_in1"] = update_value(state["gauge_in1"])
    updated_state["gauge_in2"] = update_value(state["gauge_in2"])
    updated_state["gauge_in3"] = update_value(state["gauge_in3"])

    return (
        updated_state["gauge_in1"]["current"],
        updated_state["gauge_in2"]["current"],
        updated_state["gauge_in3"]["current"],
        updated_state
    )

