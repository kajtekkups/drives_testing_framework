from dash import Input, Output, html, dcc, State
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

def callback_tab1(app):   
    @app.callback(
        Output('clickable-canvas', 'figure'),
        Output('click-store', 'data'),
        Input('clickable-canvas', 'clickData'),
        State('click-store', 'data')
    )
    def display_click(clickData, data):
        if clickData is None:
            # Return figure without changes            
            return generate_plot(), data

        # Extract click coordinates
        x = clickData['points'][0]['x']
        y = clickData['points'][0]['y']

        # Toggle point: remove if exists, else add
        if (x, y) in zip(data['x'], data['y']):
            idx = list(zip(data['x'], data['y'])).index((x, y))
            data['x'].pop(idx)
            data['y'].pop(idx)
        elif all(x > previos_x for previos_x in data['x']):
            data['x'].append(x)
            data['y'].append(y)
        else:
            print("\ncan not insert point here\n")

        # Create figure and add scatter points
        fig = generate_plot()

        # Add points **and connect them with lines**
        fig.add_scatter(
            x=data['x'],
            y=data['y'],
            mode='lines+markers',  # <-- lines + points
            line=dict(color='black', width=2),  # customize line
            marker=dict(color='black', size=10),
            showlegend=False
        )
        
        print(f"You clicked at x={x:.1f}, y={y:.1f}")
        return fig, data