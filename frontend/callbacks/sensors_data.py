import sys

if sys.platform.startswith('win'):
    from windows_stubs.backend import backend_engine
    from windows_stubs.sensor_reader import SensorID
elif sys.platform.startswith('linux'):
    from backend.backend import backend_engine
    from backend.sensor_reader import SensorID
else:
    print("Unsupported OS")

# Store live data
TEMPERATURE_SENSORS_NUMBER = len(SensorID)
plot_data = {f"plot{i}": {"x": [], "y": []} for i in range(TEMPERATURE_SENSORS_NUMBER)}
from dash import Input, Output, html, dcc

def generate_sensors_data():
    return html.Div([
                html.H3("Live Plots 5–8"),
                html.Div([
                    html.Div(dcc.Graph(id=f'plot{i}'), style={'width': '25%', 'display': 'inline-block'})
                    for i in range(TEMPERATURE_SENSORS_NUMBER)                    
                ])
            ])

def callback_sensors_data(app):
    @app.callback(
        [Output(f'plot{i}', 'figure') for i in range(TEMPERATURE_SENSORS_NUMBER)],
        Input('interval', 'n_intervals')
    )
    def update_sensors_data(n_intervals):
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