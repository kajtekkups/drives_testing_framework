import sys

if sys.platform.startswith('win'):
    from windows_stubs.backend import backend_engine
elif sys.platform.startswith('linux'):
    from backend.backend import backend_engine
else:
    print("Unsupported OS")

from common.data_classes import ServerId

import plotly.graph_objs as go
from dash import Input, Output, html, dcc, State, ctx

speed_plot_layout = {
                "title": {"text": "Velocity [rpm]"},                        
                "xaxis": {"title": {"text": "Time [s]"}},  
                "yaxis": {"title": {"text": "velocity [RPM]"}},       
                'width': 1000,
                'height': 700}

torque_plot_layout = {
                "title": {"text": "Torque [Nm]"},
                "xaxis": {"title": {"text": "Time [s]"}},
                "yaxis": {"title": {"text": "Torque [Nm]"}},
                "width": 1000,
                "height": 700
}

SECTION_STYLE = {
    "border": "1px solid #e1e4e8",
    "borderRadius": "8px",
    "padding": "16px",
    "background": "#fffdfd",
    "boxShadow": "0 1px 2px rgba(0,0,0,0.05)",
    'marginTop': '20px'
}


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


def generate_test_control_panel():
    return html.Div([
        # Control Panel Section
        section(
            "Control panel",
            [
                html.Div([
                    html.Button("Run Motor - map", id="run_motor_map_button", n_clicks=0, style={"width": "150px"}),
                    html.Button("Stop Motor", id="stop_motor_button", n_clicks=0, style={"width": "150px"}),
                    html.Div(id="motor_setpoint")
                ], style={
                    "display": "flex",
                    "flexDirection": "column",  # stack vertically
                    "gap": "10px"               # spacing between buttons
                }
                )
            ],
            section_id="control_panel",
        ),

        section(
            "plots",
            [
 
             # Two plots side-by-side
                html.Div([
                    # Left: Velocity plot
                    html.Div([
                        dcc.Graph(
                            id='velocity_plot',
                            figure={
                                'data': [],
                                'layout': speed_plot_layout  # define elsewhere
                            },
                            style={'width': '900px', 'height': '700px'}
                        )
                    ], style={"flex": "50%", "padding": "10px"}),

                    # Right: Second plot (e.g., torque, load, current)
                    html.Div([
                        dcc.Graph(
                            id='torque_plot',
                            figure={
                                'data': [],
                                'layout': torque_plot_layout
                            },
                            style={'width': '900px', 'height': '700px'}
                        )
                    ], style={"flex": "50%", "padding": "10px"}),

                ], style={"display": "flex"}),  # row for the two plots
            ],
            section_id="plots",
        ),

        # Interval for updates
        dcc.Interval(id='control_panel_interval', interval=200, n_intervals=0)
    ])


def callback_test_control_panel(app):
    @app.callback(
        # Output("motor_velocity_output", "children"),
        Output("torque_plot", "figure"),
        Output("velocity_plot", "figure"),
        Output("motor_setpoint", "children"),
        
        # Input("motor_velocity_button", "n_clicks"),
        Input('control_panel_interval', 'n_intervals'),
        # State("motor_velocity_input", "value"),
        # Input("run_motor_setpoint_button", "n_clicks"),
        Input("run_motor_map_button", "n_clicks"),        
        Input("stop_motor_button", "n_clicks")        
    )
    # def update_output(n_clicks, n_intervals, input_value, run_clicks, run_map_clicks, stop_click): 
    def update_output(n_intervals,  run_map_clicks, stop_click):     
        #TODO: refactor i trigger conditions for all 
        velocity_plots = backend_engine.get_velocity_plots() 
        vel_fig = {
            "data": [
                {
                    "x": velocity_plots[ServerId.motor_drive].meassurement_time,
                    "y": velocity_plots[ServerId.motor_drive].rpm,
                    "type": "scatter",
                    "mode": "lines+markers",
                    "name": "motor_drive"
                },
                {
                    "x": velocity_plots[ServerId.load_drive].meassurement_time,
                    "y": velocity_plots[ServerId.load_drive].rpm,
                    "type": "scatter",
                    "mode": "lines+markers",
                    "name": "load_drive",
                    # Optional styling for distinction:
                    "line": {"color": "orange", "width": 2, "dash": "dash"},
                    "marker": {"size": 6, "symbol": "circle-open"}
                },
                ],
            'layout': speed_plot_layout
        }


        torque_plots = backend_engine.get_torque_plots() 
        torque_fig = {
            "data": [
                {
                    "x": torque_plots[ServerId.motor_drive].meassurement_time,
                    "y": torque_plots[ServerId.motor_drive].torque,
                    "type": "scatter",
                    "mode": "lines+markers",
                    "name": "motor_drive"
                },
                {
                    "x": torque_plots[ServerId.load_drive].meassurement_time,
                    "y": torque_plots[ServerId.load_drive].torque,
                    "type": "scatter",
                    "mode": "lines+markers",
                    "name": "load_drive",
                    # Optional styling for distinction:
                    "line": {"color": "orange", "width": 2, "dash": "dash"},
                    "marker": {"size": 6, "symbol": "circle-open"}
                },
                ],
            'layout': torque_plot_layout
        }


        # if ctx.triggered_id == "motor_velocity_button":
        #     backend_engine.set_velocity(input_value) 

        # if ctx.triggered_id == "run_motor_setpoint_button":
        #     backend_engine.set_control_type(backend_engine.SETPOINT_CONTROL)
        #     backend_engine.motor_controller.trigger_motor()        

        if ctx.triggered_id == "run_motor_map_button":
            backend_engine.set_control_type(backend_engine.MAP_CONTROL)
            backend_engine.get_server(ServerId.motor_drive).trigger_motor()     #TODO: change the way map control is triggered              

        if ctx.triggered_id == "stop_motor_button":
            backend_engine.get_server(ServerId.motor_drive).reset() #TODO: make sure stoping is handled properly
        
        setpoint =  f"Current setpoint: {backend_engine.get_server(ServerId.motor_drive).get_stpoint()}"
        return torque_fig, vel_fig, setpoint