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

LABEL_STYLE = {"display": "block", "fontWeight": "600", "marginBottom": "6px"}
ROW_STYLE = {"marginBottom": "12px"}

NOT_CONNECTED_STYLE ={
                    "marginTop": "8px",
                    "display": "inline-block",
                    "padding": "6px 12px",
                    "borderRadius": "12px",
                    "fontWeight": "600",
                    "fontSize": "14px",
                    "color": "#721c24",
                    "backgroundColor": "#f8d7da",
                    "border": "1px solid #f5c6cb",
                    "textAlign": "center",
                }

CONNECTED_STYLE = {
                    "marginTop": "8px",
                    "display": "inline-block",
                    "padding": "6px 12px",
                    "borderRadius": "12px",
                    "fontWeight": "600",
                    "fontSize": "14px",
                    "color": "#155724",
                    "backgroundColor": "#d4edda",
                    "border": "1px solid #c3e6cb",
                    "textAlign": "center",
                }

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
                                    html.Div(
                                        id="sensor-status-panel",
                                        style={
                                            "marginTop": "8px",
                                            "display": "flex",
                                            "flexDirection": "column",
                                            "gap": "6px",
                                        },
                                    ),
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
                                    html.Div(
                                        id="usb-status"
                                    ),
                                ],
                                style=ROW_STYLE,
                            )
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
        Output("usb-status", "children"),
        Output("usb-status", "style"),
        Output("sensor-status-panel", "children"),
        Input("interval", "n_intervals"),
        prevent_initial_call=False,
    )
    def update_overview_last_update(n):
        # If interval is disabled (div fallback), this will still run once with n=None
        ticks = f"Updated: {n if n is not None else 0} ticks"

        #Sensor status:
        rows = []

        sensors_status = backend_engine.get_sensors_status()
        for sensor_name, sensor_status in sensors_status.items():

            if sensor_status:
                badge_style = CONNECTED_STYLE
            else:
                badge_style = NOT_CONNECTED_STYLE

            rows.append(
                html.Div(
                    [
                        html.Div(sensor_name, style={"flex": "1"}),
                        html.Div(
                            "OK" if sensor_status else "Offline",
                            style=badge_style,
                        ),
                    ],
                    style={
                        "display": "flex",
                        "alignItems": "center",
                        "justifyContent": "space-between",
                        "gap": "12px",
                    },
                )
            )

        #USB status:
        usb_connected = backend_engine.external_storage_status()
        if usb_connected:
            usb_status_info = "USB Connected"
            usb_status_style = CONNECTED_STYLE

        else:
            usb_status_info = "USB Not connected"
            usb_status_style = NOT_CONNECTED_STYLE

        return ticks, usb_status_info, usb_status_style, rows


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
            txt = f"Online"
            base["background"] = "#e0ffc3"
        else:
            txt = f"Offline"
            base["background"] = "#fcadad"

        return txt, base, endpoint_ip
