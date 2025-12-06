from dash import Input, Output, html, dcc

def generate_safty():
    return html.Div([
                html.H3("safty"),
                html.Div([
                    html.Div(id="safty_example")                
                ]),
                # dcc.Interval(id='interval', interval=1000, n_intervals=0) #TODO: decide to use local or global interval
            ])

def callback_safty(app):
    @app.callback(
        Output('safty_example', 'children'),
        Input('interval', 'n_intervals')
    )
    def update_safty(n_intervals):
        return 'safty template'