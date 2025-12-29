import sys

if sys.platform.startswith('win'):
    from windows_stubs.backend import backend_engine
elif sys.platform.startswith('linux'):
    from backend.backend import backend_engine
else:
    print("Unsupported OS")

import plotly.express as px
import pandas as pd
from dash import Input, Output, html, dcc, State, ctx

# Example plot
example_data = pd.DataFrame({
    "x": [1, 2, 3, 4],
    "y": [10, 15, 13, 17]
})
example_fig = px.line(example_data, x="x", y="y")
example_fig.update_layout(
    width=1100,   # width in pixels
    height=700   # height in pixels
)


def generate_test_control_panel():
    return html.Div([
        html.H3("Example input", style={"textAlign": "center"}),

        html.Div([

            # Left side: plot
            html.Div([
                dcc.Graph(id='velocity_plot')
            ], style={"flex": "70%", "padding": "10px"}),

            # Right side: stacked inputs + buttons
            html.Div([
                dcc.Input(
                    id='motor_velocity_input',
                    type='number',
                    placeholder='Enter motor velocity (0-3000 rpm)'
                ),

                html.Button("Submit", id="motor_velocity_button", n_clicks=0),

                html.Button("Run Motor - setpoint ", id="run_motor_setpoint_button", n_clicks=0),

                html.Button("Run Motor - map ", id="run_motor_map_button", n_clicks=0),

                html.Button("Stop Motor", id="stop_motor_button", n_clicks=0),

                html.Div(id="motor_setpoint") 
            ],
            style={
                "flex": "30%",
                "padding": "10px",
                "display": "flex",
                "flexDirection": "column",   # STACK vertically
                "gap": "10px"                # spacing between items
            }),

        ], style={"display": "flex"})  # Flex container
    ])


def callback_test_control_panel(app):
    @app.callback(
        # Output("motor_velocity_output", "children"),
        Output("velocity_plot", "figure"),
        Output("motor_setpoint", "children"),
        
        Input("motor_velocity_button", "n_clicks"),
        Input('interval', 'n_intervals'),
        State("motor_velocity_input", "value"),
        Input("run_motor_setpoint_button", "n_clicks"),
        Input("run_motor_map_button", "n_clicks"),        
        Input("stop_motor_button", "n_clicks")        
    )
    def update_output(n_clicks, n_intervals, input_value, run_clicks, run_map_clicks, stop_click):     
        #TODO: refactor i trigger conditions for all 
        velocity_plot = backend_engine.get_velocity_plot() 
        vel_fig = {
            'data': [{
                'x': velocity_plot.meassurement_time,
                'y': velocity_plot.rpm,
                'type': 'scatter',
                'mode': 'lines+markers'
            }],
            'layout': {
                'title': 'Velocity [rpm]',
                'width': 1100,
                'height': 700}
        }
        if ctx.triggered_id == "motor_velocity_button":
            backend_engine.set_velocity(input_value) 

        if ctx.triggered_id == "run_motor_setpoint_button":
            backend_engine.set_control_type(backend_engine.SETPOINT_CONTROL)
            backend_engine.motor_controller.trigger_motor()        

        if ctx.triggered_id == "run_motor_map_button":
            backend_engine.set_control_type(backend_engine.MAP_CONTROL)
            backend_engine.motor_controller.trigger_motor()     #TODO: change the way map control is triggered              

        if ctx.triggered_id == "stop_motor_button":
            backend_engine.motor_controller.reset() #TODO: make sure stoping is handled properly
        
        setpoint =  f"Current setpoint: {backend_engine.motor_controller.get_stpoint()}"
        return vel_fig, setpoint