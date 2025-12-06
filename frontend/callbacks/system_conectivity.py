from dash import Input, Output, html, dcc

def generate_system_conectivity():
    return html.Div([
                html.H3("system_conectivity"),
                html.Div([
                    html.Div(id="system_conectivity_example")                
                ]),
                # dcc.Interval(id='interval', interval=1000, n_intervals=0) #TODO: decide to use local or global interval
            ])

def callback_system_conectivity(app):
    @app.callback(
        Output('system_conectivity_example', 'children'),
        Input('interval', 'n_intervals')
    )
    def update_system_conectivity(n_intervals):
        return 'system_conectivity template'