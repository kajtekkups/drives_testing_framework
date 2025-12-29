import sys
if sys.platform.startswith('win'):
    from windows_stubs.backend import backend_engine
elif sys.platform.startswith('linux'):
    from backend.backend import backend_engine
else:
    print("Unsupported OS")

from common.data_classes import SERVERS

from dash import Input, Output, State, html, dcc, callback_context

import time
from datetime import datetime
from dash import Output, Input, MATCH, ctx
import random


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



# (Optional) Minimal style defaults — remove if you already define these elsewhere
CARD_STYLE = {
    "border": "1px solid #e5e7eb",
    "borderRadius": "12px",
    "padding": "16px",
    "background": "#ffffff",
    "boxShadow": "0 1px 2px rgba(0,0,0,0.06)",
    "display": "flex",
    "flexDirection": "column",
    "gap": "10px",
    "minWidth": "260px",
}
ROW_STYLE = {"display": "flex", "alignItems": "center", "gap": "8px"}
LABEL_MUTED = {"color": "#6b7280", "fontSize": "12px", "textTransform": "uppercase", "letterSpacing": "0.06em"}

def server_card(server_id: str, name: str, url: str, kind: str):
    """
    A modern 'card' with:
    - Big server name
    - Prominent IP 'chip'
    - URL in muted text
    - Status badge (color + icon)
    - Last update time
    """
    return html.Div(
        [
            # Header row: Name + Kind badge
            html.Div(
                [
                    html.Div(name, className="h5-title"),
                    html.Span(kind, className="badge kind-badge"),
                ],
                style={"display": "flex", "alignItems": "center", "justifyContent": "space-between"},
            ),

            # URL row – muted
            html.Div(
                [
                    html.Span("Endpoint", style=LABEL_MUTED),
                    html.Span(id={"type": "server-endpoint", "id": server_id},                        
                              className="endpoint-code"),
                ],
                style=ROW_STYLE,
            ),

            # Status & last update
            html.Div(
                [
                    html.Span("Status", style=LABEL_MUTED),
                    html.Span(
                        id={"type": "server-status", "id": server_id},
                        className="status-badge status-unknown"
                    ),
                ],
                style={"display": "flex", "alignItems": "center", "gap": "12px"},
            ),
        ],
        style=CARD_STYLE,
        id={"type": "server-card", "id": server_id}
    )


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
            html.H3(style={"marginBottom": "16px"}),

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
                                    html.Div(className="section-title"),
                                    html.Div(
                                        [server_card(s.id, s.name, s.url, s.kind) for s in SERVERS],
                                        style=GRID_STYLE,
                                        id="servers-grid",
                                    ),
                                ]
                            ),
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
                ],
                style=GRID_STYLE,
            ),
        ]
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


    @app.callback(
        Output({"type": "server-status", "id": MATCH}, "children"),
        Output({"type": "server-card", "id": MATCH}, "style"),
        Output({"type": "server-endpoint", "id": MATCH}, "children"),
        Input("interval", "n_intervals"),
        prevent_initial_call=False,
    )
    def update_server(match_n):
        # The pattern-matching id is available in dash.callback_context (ctx)
        # The `MATCH` id is resolved per component instance.
        pm = ctx.outputs_list[0]["id"]  # {'type': 'server-status', 'id': 'drive-1'} for example
        server_id = pm["id"]
        # change card color based on status
        base = CARD_STYLE.copy()

        server_instance = backend_engine.get_server(server_id)
        if server_instance is not None:
            endpoint_ip = server_instance.get_connection_status().ip
        else:
            endpoint_ip = ""
            txt = f"Offline"
            return txt, base, endpoint_ip
        
        
        if server_instance.client.get_connection_status().connected:
            print("connecterd")
            txt = f"Online"
            base["background"] = "#e0ffc3"
        else:
            print("disconected")
            txt = f"Offline"
            base["background"] = "#fcadad"

        return txt, base, endpoint_ip
