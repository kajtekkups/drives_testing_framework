from dash import html, dcc

app_layout  = html.Div([
    dcc.Tabs(id="tabs", value="test_control_panel", children=[
        dcc.Tab(label="System conectivity", value="system_conectivity"),
        dcc.Tab(label="Motor drive parameters", value="motor_drive_parameters"),
        dcc.Tab(label="Load drive parameters", value="load_drive_parameters"),
        dcc.Tab(label="Test map input figures", value="test_map_input_figures"),
        dcc.Tab(label="Test control panel", value="test_control_panel"),
        dcc.Tab(label="Sensors data", value="sensors_data"),
        dcc.Tab(label="Anomaly detection", value="anomaly_detection"),        
        dcc.Tab(label="Safty", value="safty"),
    ]),
    html.Div(id="tab-content"),
    dcc.Interval(id='interval', interval=1000, n_intervals=0)
])