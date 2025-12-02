from dash import html, dcc

app_layout  = html.Div([
    dcc.Tabs(id="tabs", value="tab1", children=[
        dcc.Tab(label="Tab 1", value="tab1"),
        dcc.Tab(label="Tab 2 (Plots 1–4)", value="tab2"),
        dcc.Tab(label="Tab 3 (Plots 5–8)", value="tab3"),
    ]),
    html.Div(id="tab-content"),
    dcc.Interval(id='interval', interval=100, n_intervals=0)
])