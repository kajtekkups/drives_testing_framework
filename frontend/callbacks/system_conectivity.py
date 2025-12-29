from dash import Input, Output, State, html, dcc, callback_context

SECTION_STYLE = {
    "border": "1px solid #e1e4e8",
    "borderRadius": "8px",
    "padding": "16px",
    "background": "#fff",
    "boxShadow": "0 1px 2px rgba(0,0,0,0.05)"
}

GRID_STYLE = {
    "display": "grid",
    "gridTemplateColumns": "1fr 1fr",
    "gap": "16px",
}


#TODO: connect it to real sensors, change name to external sensors, because drives are hadled seperatly
AVAILABLE_SENSORS = [
    {"id": "temp-1", "name": "Temp sensor 1"},
    {"id": "temp-2", "name": "Temp sensor 2"},
    {"id": "temp-3", "name": "Temp sensor 3"},
    {"id": "temp-4", "name": "Temp sensor 4"},
    {"id": "temp-5", "name": "Temp sensor 5"},
    {"id": "temp-6", "name": "Temp sensor 6"},
    {"id": "temp-7", "name": "Temp sensor 7"},

    {"id": "drive_1", "name": "Drive 1 sensors"},
    {"id": "drive_2", "name": "Drive 2 sensors"},
]


LABEL_STYLE = {"display": "block", "fontWeight": "600", "marginBottom": "6px"}
ROW_STYLE = {"marginBottom": "12px"}

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

def generate_system_conectivity(use_interval=False):
    """
    Four separate sections with read/write fields.
    Toggle `use_interval=True` to enable a global Interval component.
    """
    return html.Div(
        [
            html.H3("system_conectivity", style={"marginBottom": "16px"}),

            # Optional global interval

            html.Div(
                [
                    # SECTION 1: Overview
                    section(
                        "Sensors control panel",
                        [
                            html.Div(
                                [
                                    html.Label("Status", style=LABEL_STYLE),
                                    
                                    dcc.Checklist(
                                        id="sensor-checklist",
                                        options=[{"label": s["name"], "value": s["id"]} for s in AVAILABLE_SENSORS],
                                        value=[],
                                        inline=False
                                    )
                                ],
                                style=ROW_STYLE,
                            ),
                            html.Div(
                                [
                                    html.Label("Last Update (auto)", style=LABEL_STYLE),
                                    html.Div(id="overview-last-update", style={"color": "#586069"}),
                                ]
                            ),
                        ],
                        section_id="section-overview",
                    ),

                    # SECTION 2: Network
                    section(
                        "Network",
                        [
                            html.Div(
                                [
                                    html.Label("Drive 1 URL", style=LABEL_STYLE),
                                    html.Div("URL Example", id="url_1_output", style={"marginTop": "10px"}),                                    

                                    html.Div(id="drive_1_status", style={
                                        "padding": "10px",
                                        "border": "1px solid #ccc",
                                        "width": "200px",
                                        "background": "#f50909",
                                        "fontWeight": "bold"
                                    })
                              
                                ],
                                style=ROW_STYLE,
                            ),

                            html.Div(
                                [
                                    html.Label("Drive 2 URL", style=LABEL_STYLE),
                                    html.Div("URL Example", id="url_2_output", style={"marginTop": "10px"}),                                    

                                    html.Div(id="drive_2_status", style={
                                        "padding": "10px",
                                        "border": "1px solid #ccc",
                                        "width": "200px",
                                        "background": "#f50909",
                                        "fontWeight": "bold"
                                    })
                              
                                ],
                                style=ROW_STYLE,
                            ),

                            html.Div(
                                [
                                    html.Label("MQTT", style=LABEL_STYLE),
                                    html.Div("URL Example", id="MQTT_url_output", style={"marginTop": "10px"}),                                    

                                    html.Div(id="MQTT_status", style={
                                        "padding": "10px",
                                        "border": "1px solid #ccc",
                                        "width": "200px",
                                        "background": "#f50909",
                                        "fontWeight": "bold"
                                    })
                              
                                ],
                                style=ROW_STYLE,
                            ),

                            html.Div(id="net-result", style={"marginTop": "8px", "color": "#0366d6"}),
                        ],
                        section_id="section-network",
                    ),

                    # SECTION 3: Database
                    section(
                        "Database",
                        [
                            html.Div(
                                [
                                    html.Label("USB drive", style=LABEL_STYLE),
                                ],
                                style=ROW_STYLE,                            
                            ),
                            html.Div(id="db-summary", style={"marginTop": "8px"}),
                        ],
                        section_id="section-database",
                    ),

                    # SECTION 4: Services
                    section(
                        "Services",
                        [
                            html.Div(
                                [
                                    html.Label("Enabled Services", style=LABEL_STYLE),
                                    dcc.Checklist(
                                        id="svc-enabled",
                                        options=[
                                            {"label": "Auth", "value": "auth"},
                                            {"label": "API", "value": "api"},
                                            {"label": "Worker", "value": "worker"},
                                            {"label": "Scheduler", "value": "scheduler"},
                                        ],
                                        value=["auth", "api"],
                                        inline=True,
                                    ),
                                ],
                                style=ROW_STYLE,
                            ),
                            html.Div(
                                [
                                    html.Label("Notes", style=LABEL_STYLE),
                                    dcc.Textarea(
                                        id="svc-notes",
                                        placeholder="Operational notes, maintenance windows, throttling, etc.",
                                        style={"width": "100%", "height": "80px"},
                                    ),
                                ],
                                style=ROW_STYLE,
                            ),
                            html.Div(id="svc-output", style={"marginTop": "8px", "whiteSpace": "pre-wrap"}),
                        ],
                        section_id="section-services",
                    ),
                ],
                style=GRID_STYLE,
            ),

            # Keep your original placeholder if you still need it
            html.Div(id="system_conectivity_example", style={"marginTop": "16px", "color": "#6a737d"}),
        ],
        style={"display": "flex", "flexDirection": "column", "gap": "16px"}
    )

def callback_system_conectivity(app):
    # Overview last update (ticks with global interval if present)
    @app.callback(
        Output("overview-last-update", "children"),
        Input("interval", "n_intervals"),
        prevent_initial_call=False,
    )
    def update_overview_last_update(n):
        # If interval is disabled (div fallback), this will still run once with n=None
        return f"Updated: {n if n is not None else 0} ticks"

    # Network test action
    @app.callback(
        Output("net-result", "children"),
        Input("btn-test-net", "n_clicks"),
        State("Drive_1_id", "value"),
        State("net-port", "value"),
        prevent_initial_call=True,
    )
    def run_network_test(n_clicks, endpoint, port):
        if not endpoint or not port:
            return "Please provide both endpoint and port."
        # Dummy result – replace with your real check
        ok = str(endpoint).startswith("http") and 1 <= int(port) <= 65535
        return "Connectivity OK ✅" if ok else "Connectivity failed ❌"

    # Database summary
    @app.callback(
        Output("db-summary", "children"),
        Input("db-host", "value"),
        Input("db-name", "value"),
        Input("db-mode", "value"),
    )
    def show_db_summary(host, name, mode):
        if not host and not name:
            return "Waiting for database details…"
        mode_label = "Read-Only" if mode == "ro" else "Read/Write"
        return f"DB: {host or '-'} / {name or '-'} | Mode: {mode_label}"

    # Services echo
    @app.callback(
        Output("svc-output", "children"),
        Input("svc-enabled", "value"),
        Input("svc-notes", "value"),
    )
    def show_services(enabled, notes):
        enabled = enabled or []
        notes = notes or ""
        return f"Enabled: {', '.join(enabled) if enabled else 'None'}\nNotes: {notes}"

    # Keep your original example output, wired to the (optional) interval
    @app.callback(
        Output('system_conectivity_example', 'children'),
        Input('interval', 'n_intervals')
    )
    def update_system_conectivity(n_intervals):
        return 'system_conectivity template'
