from dash import Input, Output, html, dcc

def generate_load_drive_parameters():
    return html.Div([
                html.H3("load_drive_params"),
                html.Div([
                    html.Div(id="load_drive_params_example")                
                ]),
                # dcc.Interval(id='interval', interval=1000, n_intervals=0) #TODO: decide to use local or global interval
            ])

def callback_load_drive_parameters(app):
    @app.callback(
        Output('load_drive_params_example', 'children'),
        Input('interval', 'n_intervals')
    )
    def update_load_drive_params(n_intervals):
        return 'load_drive_params template'