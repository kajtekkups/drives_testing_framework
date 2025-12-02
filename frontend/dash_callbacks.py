import sys

if sys.platform.startswith('win'):
    from windows_stubs.backend import backend_engine
    from windows_stubs.backend import SensorID
elif sys.platform.startswith('linux'):
    from backend.backend import backend_engine
    from backend.backend import SensorID
else:
    print("Unsupported OS")

from frontend.tab2 import generate_tab2
from frontend.tab1 import generate_tab1, generate_plot

from dash import Input, Output, html, dcc, State

# Store live data
TEMPERATURE_SENSORS_NUMBER = len(SensorID)
plot_data = {f"plot{i}": {"x": [], "y": []} for i in range(TEMPERATURE_SENSORS_NUMBER)}

def register_callbacks(app):

    ##############################################################
    # Render Tab Content
    ##############################################################
    @app.callback(
        Output("tab-content", "children"),
        Input("tabs", "value")
    )
    def render_tab(tab):
        if tab == "tab1":
            return generate_tab1()
        
        elif tab == "tab2":
            return generate_tab2()

        elif tab == "tab3":
            return html.Div([
                html.H3("Live Plots 5–8"),
                html.Div([
                    html.Div(dcc.Graph(id=f'plot{i}'), style={'width': '25%', 'display': 'inline-block'})
                    for i in range(TEMPERATURE_SENSORS_NUMBER)                    
                ])
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
    # ➤ velocity control input
    ##############################################################
    @app.callback(
        Output("motor_velocity", "children"),
        Input("motor_velocity_button", "n_clicks"),
        State("Motor_velocity_input", "value")
    )
    def update_output(n_clicks, input_value):
        if n_clicks > 0:
            # Store the value in a variable (here just returning for display)
            stored_value = input_value
            return f"You entered: {stored_value}"
        return "No input yet."


    ##############################################################
    # ➤ Update Plots 1–4
    ##############################################################
    @app.callback(
        [Output(f'plot{i}', 'figure') for i in range(TEMPERATURE_SENSORS_NUMBER)],
        Input('interval', 'n_intervals')
    )
    def update_tab3(n):
        figures = []
        measurements = backend_engine.get_measurements()
        time = backend_engine.get_time()
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