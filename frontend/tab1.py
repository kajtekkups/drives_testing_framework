from dash import html, dcc
import plotly.express as px
import numpy as np

def generate_plot():
    X_AXIS_SIZE = 160
    Y_AXIS_SIZE = 90
    fig = px.imshow(np.zeros((Y_AXIS_SIZE, X_AXIS_SIZE, 4)),
                    origin='lower')  # origin='upper' makes y=0 at top
    fig.update_xaxes(showticklabels=True, range=[0, X_AXIS_SIZE], fixedrange=True, autorange=False)
    fig.update_yaxes(showticklabels=True, range=[0, Y_AXIS_SIZE], fixedrange=False, autorange=False)
    fig.update_layout(clickmode='event+select')  # enable click events
    return fig


def generate_tab1():
    fig = generate_plot()

    return html.Div([
                html.H3("Click anywhere on the blank canvas"),
                dcc.Graph(id='clickable-canvas', figure=fig, style={'height': '800px'}),
                dcc.Store(id='click-store', data={'x': [], 'y': []})
            ])  
    