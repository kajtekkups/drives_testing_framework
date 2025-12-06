import sys

if sys.platform.startswith('win'):
    from windows_stubs.backend import backend_engine
elif sys.platform.startswith('linux'):
    from backend.backend import backend_engine
else:
    print("Unsupported OS")

from dash import Input, Output, html, dcc, State
import plotly.express as px
import numpy as np
import plotly.graph_objects as go

input_figure = None

def add_input_point(figure, timestamp_points, rpm_points):
    figure.add_scatter(
        x=timestamp_points,
        y=rpm_points,
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
    timestamp_points, rpm_points =  backend_engine.get_motor_test_map()
    add_input_point(input_figure, timestamp_points, rpm_points)

    return html.Div([
                html.H3("Click anywhere on the blank canvas"),
                dcc.Graph(id='clickable-canvas', 
                          figure=input_figure, 
                          style={'height': '800px'}),

            ])  

def callback_test_map_input_figures(app):   
    @app.callback(
        Output("clickable-canvas", "figure"),
        Input("clickable-canvas", "clickData"),
    )
    def display_click(clickData):
        #TODO: make sure, that the rpm differences are not too big
        global input_figure
        if clickData is None:
            # Return figure without changes            
            return input_figure

        # Extract click coordinates
        x = clickData['points'][0]['x']
        y = clickData['points'][0]['y']

        timestamp_points, rpm_points =  backend_engine.get_motor_test_map()

        # Toggle point: remove if exists, else add
        if (x, y) in zip(timestamp_points, rpm_points): #TODO: fix floating point comparision
            idx = list(zip(timestamp_points, rpm_points)).index((x, y))
            timestamp_points.pop(idx) #TODO: Dash sometimes doesn't detect in-place mutations, but sometimes throws error
            rpm_points.pop(idx) #TODO: Dash sometimes doesn't detect in-place mutations, but sometimes throws error
            input_figure = generate_plot()
        elif all(x > previos_x for previos_x in timestamp_points):
            timestamp_points.append(x) #TODO: Dash sometimes doesn't detect in-place mutations, but sometimes throws error
            rpm_points.append(y) #TODO: Dash sometimes doesn't detect in-place mutations, but sometimes throws error
        else:
            print("\ncan not insert point here\n")

        # Add points **and connect them with lines**
        add_input_point(input_figure, timestamp_points, rpm_points)
        
        backend_engine.set_motor_test_map(timestamp_points, rpm_points) #TODO: add button and if statement to send map
        print(f"You clicked at x={x}, y={y}")
        print(timestamp_points, rpm_points)
        return input_figure