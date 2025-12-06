from dash import Input, Output, html, dcc

def generate_anomaly_detection():
    return html.Div([
                html.H3("anomaly_detection"),
                html.Div([
                    html.Div(id="anomaly_detection_example")                
                ]),
                # dcc.Interval(id='interval', interval=1000, n_intervals=0) #TODO: decide to use local or global interval
            ])

def callback_anomaly_detection(app):
    @app.callback(
        Output('anomaly_detection_example', 'children'),
        Input('interval', 'n_intervals')
    )
    def update_anomaly_detection(n_intervals):
        return 'anomaly_detection template'