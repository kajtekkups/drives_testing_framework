import sys

if sys.platform.startswith('win'):
    from windows_stubs.backend import backend_engine
elif sys.platform.startswith('linux'):
    from backend.backend import backend_engine
else:
    print("Unsupported OS")

from backend.system_engine import VelocityPlot #TODO: remove dependency on system_engine
from common.data_classes import ServerId, SERVERS

from dash import Input, Output, html, dcc, Dash, State, ctx
import plotly.express as px
import plotly.graph_objects as go

import numpy as np

input_figure_speed = None
input_figure_torque = None

RESET_PLOT = True
KEEP_PLOT = False

SECTION_STYLE = {
    "border": "1px solid #e1e4e8",
    "borderRadius": "8px",
    "padding": "16px",
    "background": "#f7f6f6",
    "boxShadow": "0 1px 2px rgba(0,0,0,0.05)",
    'marginTop': '20px'
}

def reset_plots(test_lenght_input):
    backend_engine.set_map_test_time(test_lenght_input)
    backend_engine.clean_test_maps()

def handle_new_point(clickData, test_map):
    # Extract click coordinates
    x = clickData['points'][0]['x']
    y = clickData['points'][0]['y']
    print(f"You clicked at x={x}, y={y}")

    # Toggle point: remove if exists, else add
    if (x, y) in zip(test_map.timestamp, test_map.setpoint): #TODO: fix floating point comparision
        idx = list(zip(test_map.timestamp, test_map.setpoint)).index((x, y))
        test_map.timestamp.pop(idx) #TODO: Dash sometimes doesn't detect in-place mutations, but sometimes throws error
        test_map.setpoint.pop(idx) #TODO: Dash sometimes doesn't detect in-place mutations, but sometimes throws error
        return test_map, RESET_PLOT
    elif all(x > previos_x for previos_x in test_map.timestamp):
        test_map.timestamp.append(x) #TODO: Dash sometimes doesn't detect in-place mutations, but sometimes throws error
        test_map.setpoint.append(y) #TODO: Dash sometimes doesn't detect in-place mutations, but sometimes throws error
    else:
        print("\ncan not insert point here\n")

    return test_map, KEEP_PLOT


def add_input_point(figure: go.Figure, test_map):
    figure.add_scatter(
        x=test_map.timestamp,
        y=test_map.setpoint,
        mode='lines+markers',
        line=dict(color='black', width=1),
        marker=dict(color='red', size=10),
        line_shape='hv',        # <-- key: horizontal-then-vertical (step)
        showlegend=False
    )


def generate_plot_torque():
    X_AXIS_SIZE, Y_AXIS_SIZE, SCALE_RATIO = backend_engine.get_torque_map_size()

    fig = px.imshow(np.zeros((Y_AXIS_SIZE, X_AXIS_SIZE, 4)),
                    origin='lower')  # origin='upper' makes y=0 at top
    fig.update_xaxes(showticklabels=True, range=[0, X_AXIS_SIZE], fixedrange=True, autorange=False)
    fig.update_yaxes(showticklabels=True, range=[0, Y_AXIS_SIZE],fixedrange=True, autorange=False, scaleanchor="x", scaleratio=SCALE_RATIO) #TODO: calculate scaling from axis size
    fig.update_layout(
                        clickmode='event+select',                                               
                        xaxis_title='time [s]',
                        yaxis_title='motor torque [Nm]',
                        
                        title={
                            'text': 'Torque map input figure',
                            'x': 0.5,
                            'xanchor': 'center',
                            'yanchor': 'top'
                        },
                        title_font=dict(size=24, family='Arial', color='black')  

                )
    return fig

def generate_plot_speed():
    X_AXIS_SIZE, Y_AXIS_SIZE, SCALE_RATIO = backend_engine.get_speed_map_size()

    fig = px.imshow(np.zeros((Y_AXIS_SIZE, X_AXIS_SIZE, 4)),
                    origin='lower')  # origin='upper' makes y=0 at top
    fig.update_xaxes(showticklabels=True, range=[0, X_AXIS_SIZE], fixedrange=True, autorange=False)
    fig.update_yaxes(showticklabels=True, range=[0, Y_AXIS_SIZE],fixedrange=True, autorange=False, scaleanchor="x", scaleratio=SCALE_RATIO) #TODO: calculate scaling from axis size
    fig.update_layout(
                        clickmode='event+select',                                               
                        xaxis_title='time [s]',
                        yaxis_title='motor set speed [rpm]',
                        
                        title={
                            'text': 'Speed map input figure',
                            'x': 0.5,
                            'xanchor': 'center',
                            'yanchor': 'top'
                        },
                        title_font=dict(size=24, family='Arial', color='black')  

                )
    return fig

def section(title, children, section_id=None):
    """Small helper to render a consistent card-like section."""
    return html.Div(
        [
            html.H4(title, style={"marginTop": 0, "marginBottom": "12px"}),
            html.Div(children)
        ],
        id=section_id,
        style=SECTION_STYLE
    )

def generate_test_map_input_figures():
    ############################
    ### SPEED PLOT
    ############################
    global input_figure_speed
    input_figure_speed = generate_plot_speed()
    test_map_speed =  backend_engine.get_motor_test_map(ServerId.motor_drive)
    add_input_point(input_figure_speed, test_map_speed)

    ############################
    ### TORQUE PLOT
    ############################
    global input_figure_torque
    input_figure_torque = generate_plot_torque()
    test_map_torque =  backend_engine.get_motor_test_map(ServerId.load_drive)
    add_input_point(input_figure_torque, test_map_torque)



    return html.Div(
        [
        html.H3(style={"marginBottom": "16px"}),
        
            section(
                "Set test lenght",
                [
                html.Div([
                    dcc.Input(
                        id='test_lenght',
                        type='number',
                        placeholder='input test lenght [s]',
                        style={'marginRight': '10px'}
                    ),
                    html.Button('Submit', id='test_lenght_submit_button', n_clicks=0)
                ], style={'marginTop': '20px'})
                ],
                section_id="test_lenght",
            ),

            section(
                "Speed input",
                [
                html.Div(
                    [
                    
                    dcc.Graph(id='clickable_canvas_speed', 
                                figure=input_figure_speed, 
                                style={'height': '600px'}),

                    ])  
                ],
                section_id="speed_input",
            ),

            section(
                "Torque input",
                [
                html.Div(
                    [
                    
                    dcc.Graph(id='clickable_canvas_torque', 
                                figure=input_figure_torque, 
                                style={'height': '600px'}),

                    ])  
                ],
                section_id="torque_input",
            )
        ]
    )

def callback_test_map_input_figures(app: Dash):   
    ###################################
    ####### CHANGE TEST LENGHT
    ###################################
    @app.callback(
        Output("clickable_canvas_speed", "figure"),
        Output("clickable_canvas_torque", "figure"),
        Input("test_lenght_submit_button", "n_clicks"),
        State("test_lenght", "value"),
        prevent_initial_call=True,
    )
    def display_click_speed(n_clicks, test_lenght_input):
        global input_figure_speed
        global input_figure_torque

        reset_plots(test_lenght_input)
        input_figure_speed = generate_plot_speed()
        input_figure_torque = generate_plot_torque()
        return input_figure_speed, input_figure_torque


    @app.callback(
        Output("clickable_canvas_speed", "figure", allow_duplicate=True),
        Input("clickable_canvas_speed", "clickData"),
        prevent_initial_call=True,
    )
    def display_click_speed(clickData):
        global input_figure_speed
        
        #TODO: make sure, that the rpm differences are not too big
        if clickData is None:
            # Return figure without changes            
            return input_figure_speed

        test_map =  backend_engine.get_motor_test_map(ServerId.motor_drive)

        test_map, reset_request = handle_new_point(clickData, test_map)
        if reset_request:
            input_figure_speed = generate_plot_speed()
        
        # Add points **and connect them with lines**
        add_input_point(input_figure_speed, test_map)
        
        backend_engine.set_motor_test_map_speed(test_map) #TODO: add button and if statement to send map
        
        print(test_map.timestamp, test_map.setpoint)
        return input_figure_speed
    

    @app.callback(
    Output("clickable_canvas_torque", "figure", allow_duplicate=True),
    Input("clickable_canvas_torque", "clickData"),
    prevent_initial_call=True,
    )
    def display_click_torque(clickData):
        global input_figure_torque
        
        #TODO: make sure, that the rpm differences are not too big
        if clickData is None:
            # Return figure without changes            
            return input_figure_torque

        test_map =  backend_engine.get_motor_test_map(ServerId.load_drive)

        test_map, reset_request = handle_new_point(clickData, test_map)
        if reset_request:
            input_figure_torque = generate_plot_torque()
        
        # Add points **and connect them with lines**
        add_input_point(input_figure_torque, test_map)
        
        backend_engine.set_motor_test_map_torque(test_map) #TODO: add button and if statement to send map
        
        print(test_map.timestamp, test_map.setpoint)
        return input_figure_torque


    