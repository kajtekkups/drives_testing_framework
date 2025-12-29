import sys

if sys.platform.startswith('win'):
    from windows_stubs.backend import backend_engine
    from windows_stubs.sensor_reader import SensorID
elif sys.platform.startswith('linux'):
    from backend.backend import backend_engine
    from backend.sensor_reader import SensorID
else:
    print("Unsupported OS")

from dash import Input, Output, html, dcc

SECTION_STYLE = {
    "border": "1px solid #e1e4e8",
    "borderRadius": "8px",
    "padding": "16px",
    "background": "#f2f1f1",
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
    
# Store live data
TEMPERATURE_SENSORS_NUMBER = len(SensorID)
PLOT_NAME = "sensor_plot_"

def generate_sensors_data():
    return html.Div(
        [
            html.Div(
                section(
                    title=f"Sensor {i + 1}",
                    children=dcc.Graph(id=f"{PLOT_NAME}{i}"),
                    section_id=f"sensor-section-{i}",
                ),
                style={
                    "width": "25%",
                    "display": "inline-block",
                    "verticalAlign": "top",
                },
            )
            for i in range(TEMPERATURE_SENSORS_NUMBER)
        ]
    )

def callback_sensors_data(app):
    @app.callback(
        [Output(f'{PLOT_NAME}{i}', 'figure') for i in range(TEMPERATURE_SENSORS_NUMBER)],
        Input('interval', 'n_intervals')
    )
    def update_sensors_data(n_intervals):
        figures = []
        measurements = backend_engine.get_measurements()
        time = measurements.meassurement_time

        if not measurements.sensors_meassurement:
            for plot_index in range(TEMPERATURE_SENSORS_NUMBER):
                figures.append({
                    'data': [{
                        'x': [],
                        'y': [],
                        'type': 'scatter',
                        'mode': 'lines+markers'
                    }],
                    'layout': {'title': f'{PLOT_NAME} {plot_index}'}
                })
            return figures

        keys = list(measurements.sensors_meassurement.keys())

        print(measurements)
        print(time)

        for plot_index, key_index in enumerate(range(TEMPERATURE_SENSORS_NUMBER)):
            key = keys[key_index]

            figures.append({
                'data': [{
                    'x': time,
                    'y': measurements[key],
                    'type': 'scatter',
                    'mode': 'lines+markers'
                }],
                'layout': {'title': f'{PLOT_NAME} {plot_index}'}
            })

        return figures