from dash import Input, Output, html, dcc
import random

from backend.backend import backend_runner

# Store live data
plot_data = {f"plot{i}": {"x": [], "y": []} for i in range(1, 9)}

def register_callbacks(app):

    # Render Tab Content
    @app.callback(
        Output("tab-content", "children"),
        Input("tabs", "value")
    )
    def render_tab(tab):
        if tab == "tab2":
            return html.Div([
                html.H3("Live Plots 1–4"),
                html.Div([
                    html.Div(dcc.Graph(id=f'plot{i}'), style={'width': '25%', 'display': 'inline-block'})
                    for i in range(5, 9)
                ])
            ])

        elif tab == "tab3":
            return html.Div([
                html.H3("Live Plots 5–8"),
                html.Div([
                    html.Div(dcc.Graph(id=f'plot{i}'), style={'width': '25%', 'display': 'inline-block'})
                    for i in range(1, 5)                    
                ])
            ])

        return html.Div([
            html.H3("Welcome to Tab 1"),
            html.P("This is a placeholder tab before the plots.")
        ])


    # ➤ Update Plots 1–4
    @app.callback(
        [Output(f'plot{i}', 'figure') for i in range(5, 9)],
        Input('interval', 'n_intervals')
    )
    def update_tab2(n):
        figures = []
        for i in range(5, 9):
            plot_data[f'plot{i}']['x'].append(n)
            plot_data[f'plot{i}']['y'].append(random.randint(0, 10))
            figures.append({
                'data': [{
                    'x': plot_data[f'plot{i}']['x'],
                    'y': plot_data[f'plot{i}']['y'],
                    'type': 'scatter',
                    'mode': 'lines+markers'
                }],
                'layout': {'title': f'Plot {i}'}
            })
        return figures


    @app.callback(
        [Output(f'plot{i}', 'figure') for i in range(1, 5)],
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
        for plot_index, key_index in enumerate(range(4), start=1):
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