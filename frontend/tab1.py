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


def generate_plot():
    X_AXIS_SIZE, Y_AXIS_SIZE = backend_engine.get_map_size()

    fig = px.imshow(np.zeros((Y_AXIS_SIZE, X_AXIS_SIZE, 4)),
                    origin='lower')  # origin='upper' makes y=0 at top
    fig.update_xaxes(showticklabels=True, range=[0, X_AXIS_SIZE], fixedrange=True, autorange=False)
    fig.update_yaxes(showticklabels=True, range=[0, Y_AXIS_SIZE],fixedrange=True, autorange=False, scaleanchor="x", scaleratio=0.3) #TODO: calculate scaling from axis size
    fig.update_layout(clickmode='event+select')
    return fig

input_figure = None

def generate_tab1():
    global input_figure
    input_figure = generate_plot()

    return html.Div([
                html.H3("Click anywhere on the blank canvas"),
                dcc.Graph(id='clickable-canvas', 
                          figure=input_figure, 
                          style={'height': '800px'}),
                dcc.Store(id='click-store', data={'x': [], 'y': []})
            ])  

def callback_tab1(app):   
    @app.callback(
        Output("click-store", "data"),
        Output("clickable-canvas", "figure"),
        Input("clickable-canvas", "clickData"),
        State("click-store", "data")
    )
    def display_click(clickData, data):
        global input_figure
        if clickData is None:
            # Return figure without changes            
            return data, input_figure  #generate_plot(), data

        # Extract click coordinates
        x = clickData['points'][0]['x']
        y = clickData['points'][0]['y']

        # Toggle point: remove if exists, else add
        if (x, y) in zip(data['x'], data['y']): #TODO: fix floating point comparision
            idx = list(zip(data['x'], data['y'])).index((x, y))
            data['x'].pop(idx) #TODO: Dash sometimes doesn't detect in-place mutations, but sometimes throws error
            data['y'].pop(idx) #TODO: Dash sometimes doesn't detect in-place mutations, but sometimes throws error
            input_figure = generate_plot()
        elif all(x > previos_x for previos_x in data['x']):
            data['x'].append(x) #TODO: Dash sometimes doesn't detect in-place mutations, but sometimes throws error
            data['y'].append(y) #TODO: Dash sometimes doesn't detect in-place mutations, but sometimes throws error
        else:
            print("\ncan not insert point here\n")

        # Add points **and connect them with lines**
        input_figure.add_scatter(
            x=data['x'],
            y=data['y'],
            mode='lines+markers',  # <-- lines + points
            line=dict(color='black', width=2),  # customize line
            marker=dict(color='black', size=10),
            showlegend=False
        )
        
        print(f"You clicked at x={x}, y={y}")
        return data, input_figure