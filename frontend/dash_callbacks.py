from dash import Input, Output, html, dcc, State
import plotly.express as px
import numpy as np
import sys

if sys.platform.startswith('win'):
    from windows_stubs.backend import backend_runner
    from windows_stubs.backend import SensorID
elif sys.platform.startswith('linux'):
    from backend.backend import backend_runner
    from backend.backend import SensorID
else:
    print("Unsupported OS")


# Store live data
TEMPERATURE_SENSORS_NUMBER = len(SensorID)
plot_data = {f"plot{i}": {"x": [], "y": []} for i in range(TEMPERATURE_SENSORS_NUMBER)}


def generate_plot():
    X_AXIS_SIZE = 160
    Y_AXIS_SIZE = 90
    fig = px.imshow(np.zeros((Y_AXIS_SIZE, X_AXIS_SIZE, 4)),
                    origin='lower')  # origin='upper' makes y=0 at top
    fig.update_xaxes(showticklabels=True, range=[0, X_AXIS_SIZE], fixedrange=True, autorange=False)
    fig.update_yaxes(showticklabels=True, range=[0, Y_AXIS_SIZE], fixedrange=False, autorange=False)
    fig.update_layout(clickmode='event+select')  # enable click events
    return fig

def register_callbacks(app):

    ##############################################################
    # Render Tab Content
    ##############################################################
    @app.callback(
        Output("tab-content", "children"),
        Input("tabs", "value")
    )
    def render_tab(tab):
        if tab == "tab2":
            return html.Div([
                html.H3("Live Plots 1–4"),
                html.Button("Click me", id="my-button", n_clicks=0),
                html.Div(id="output"),
            ],
                style={"textAlign": "center"}
            )

        elif tab == "tab3":
            return html.Div([
                html.H3("Live Plots 5–8"),
                html.Div([
                    html.Div(dcc.Graph(id=f'plot{i}'), style={'width': '25%', 'display': 'inline-block'})
                    for i in range(TEMPERATURE_SENSORS_NUMBER)                    
                ])
            ])

        fig = generate_plot()

        return html.Div([
            html.H3("Click anywhere on the blank canvas"),
            dcc.Graph(id='clickable-canvas', figure=fig, style={'height': '800px'}),
            dcc.Store(id='click-store', data={'x': [], 'y': []})
        ])  
    

    ##############################################################
    # ➤ Update input graph
    ##############################################################
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

    ##############################################################
    # ➤ Update button
    ##############################################################
    @app.callback(
        Output("output", "children"),
        Input("my-button", "n_clicks")
    )
    def display_clicks(n_clicks):
        return f"Button clicked {n_clicks} times!"


    ##############################################################
    # ➤ Update Plots 1–4
    ##############################################################
    @app.callback(
        [Output(f'plot{i}', 'figure') for i in range(TEMPERATURE_SENSORS_NUMBER)],
        Input('interval', 'n_intervals')
    )
    def update_tab3(n):
        figures = []
        measurements = backend_runner.get_measurements()
        time = backend_runner.get_time()
        keys = list(measurements.keys())

        print(measurements)
        print(time)
        # Plot T5–T8 → plot5–plot8
        for plot_index, key_index in enumerate(range(TEMPERATURE_SENSORS_NUMBER)):
            key = keys[key_index]
            
            plot_data[f'plot{plot_index}']['x'].append(time)
            plot_data[f'plot{plot_index}']['y'].append(measurements[key])

            figures.append({
                'data': [{
                    'x': plot_data[f'plot{plot_index}']['x'],
                    'y': plot_data[f'plot{plot_index}']['y'],
                    'type': 'scatter',
                    'mode': 'lines+markers'
                }],
                'layout': {'title': f'Plot {plot_index}'}
            })

        return figures