from dash import Input, Output, html, dcc

def generate_motor_drive_parameters():
    return html.Div([
                html.H3("motor_drive_params"),
                html.Div([
                    html.Div(id="motor_drive_params_example")                
                ]),
                # dcc.Interval(id='interval', interval=1000, n_intervals=0) #TODO: decide to use local or global interval
            ])

def callback_motor_drive_parameters(app):
    @app.callback(
        Output('motor_drive_params_example', 'children'),
        Input('interval', 'n_intervals')
    )
    def update_motor_drive_params(n_intervals):
        return 'motor_drive_params template'