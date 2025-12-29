import sys

if sys.platform.startswith('win'):
    from windows_stubs.backend import backend_engine
elif sys.platform.startswith('linux'):
    from backend.backend import backend_engine
else:
    print("Unsupported OS")

from backend.system_engine import VelocityPlot #TODO: remove dependency on system_engine

from dash import Input, Output, html, dcc, Dash, State, ctx
import plotly.express as px
import plotly.graph_objects as go

import numpy as np

input_figure = None

def add_input_point(figure: go.Figure, test_map):
    figure.add_scatter(
        x=test_map.timestamp,
        y=test_map.rpm,
        mode='lines+markers',
        line=dict(color='black', width=1),
        marker=dict(color='red', size=10),
        line_shape='hv',        # <-- key: horizontal-then-vertical (step)
        showlegend=False
    )


def generate_plot():
    X_AXIS_SIZE, Y_AXIS_SIZE, SCALE_RATIO = backend_engine.get_map_size()

    fig = px.imshow(np.zeros((Y_AXIS_SIZE, X_AXIS_SIZE, 4)),
                    origin='lower')  # origin='upper' makes y=0 at top
    fig.update_xaxes(showticklabels=True, range=[0, X_AXIS_SIZE], fixedrange=True, autorange=False)
    fig.update_yaxes(showticklabels=True, range=[0, Y_AXIS_SIZE],fixedrange=True, autorange=False, scaleanchor="x", scaleratio=SCALE_RATIO) #TODO: calculate scaling from axis size
    fig.update_layout(clickmode='event+select')
    return fig

def generate_test_map_input_figures():
    global input_figure
    input_figure = generate_plot()
    test_map =  backend_engine.get_motor_test_map()
    add_input_point(input_figure, test_map)

    return html.Div([
                html.H3("Click anywhere on the blank canvas"),
                dcc.Graph(id='clickable-canvas', 
                          figure=input_figure, 
                          style={'height': '800px'}),

            html.Div([
                dcc.Input(
                    id='test_lenght',
                    type='number',
                    placeholder='input test lenght [s]',
                    style={'marginRight': '10px'}
                ),
                html.Button('Submit', id='test_lenght_submit_button', n_clicks=0)
            ], style={'marginTop': '20px'})
            ])  

def callback_test_map_input_figures(app: Dash):   
    @app.callback(
        Output("clickable-canvas", "figure"),
        [
            Input("clickable-canvas", "clickData"),
            Input("test_lenght_submit_button", "n_clicks")
        ],
        State("test_lenght", "value")

    )
    def display_click(clickData, n_clicks, test_lenght_input):
        global input_figure

        if ctx.triggered_id == "test_lenght_submit_button":
            backend_engine.set_map_test_time(test_lenght_input)
            backend_engine.clean_test_map()
            input_figure = generate_plot()
            return input_figure
        
        #TODO: make sure, that the rpm differences are not too big
        if clickData is None:
            # Return figure without changes            
            return input_figure

        # Extract click coordinates
        x = clickData['points'][0]['x']
        y = clickData['points'][0]['y']

        test_map =  backend_engine.get_motor_test_map()

        # Toggle point: remove if exists, else add
        if (x, y) in zip(test_map.timestamp, test_map.rpm): #TODO: fix floating point comparision
            idx = list(zip(test_map.timestamp, test_map.rpm)).index((x, y))
            test_map.timestamp.pop(idx) #TODO: Dash sometimes doesn't detect in-place mutations, but sometimes throws error
            test_map.rpm.pop(idx) #TODO: Dash sometimes doesn't detect in-place mutations, but sometimes throws error
            input_figure = generate_plot()
        elif all(x > previos_x for previos_x in test_map.timestamp):
            test_map.timestamp.append(x) #TODO: Dash sometimes doesn't detect in-place mutations, but sometimes throws error
            test_map.rpm.append(y) #TODO: Dash sometimes doesn't detect in-place mutations, but sometimes throws error
        else:
            print("\ncan not insert point here\n")

        # Add points **and connect them with lines**
        add_input_point(input_figure, test_map)
        
        backend_engine.set_motor_test_map(test_map) #TODO: add button and if statement to send map
        print(f"You clicked at x={x}, y={y}")
        print(test_map.timestamp, test_map.rpm)
        return input_figure