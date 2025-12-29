import sys
if sys.platform.startswith('win'):
    from windows_stubs.backend import backend_engine
elif sys.platform.startswith('linux'):
    from backend.backend import backend_engine
else:
    print("Unsupported OS")

import common.drive_parameters as param
from common.data_classes import ServerId

from dash import Dash, Input, Output, State, ALL, html, dcc
import dash
import random
import copy
import typing

# -------------------------
# Definicja parametrów (łatwo dodać nowe)
# -------------------------
# Każdy parametr: id (unikalny string), name (etykieta), section (grupa), default, unit, type ('num'|'text')
PARAMETERS = [
    # Sekcja 19 - Operation mode
    {"id": "19_current_mode", "name": "19.1 Aktual operation mode", "section": "19 - Operation mode", "default": "3", "unit": "", "type": "num", "opcua_id": param.ACTUAL_OPERATION_MODE},
    {"id": "19_ext_source_select", "name": "19.11 Źródło zewnętrzne", "section": "19 - Operation mode", "default": "0", "unit": "", "type": "num", "opcua_id": param.EXT1_EXT2_SELECTION },
    {"id": "19_local_lock", "name": "19.17 Blokada sterowania lokalnego", "section": "19 - Operation mode", "default": "0", "unit": "", "type": "num", "opcua_id": param.LOCAL_CONTROL_DISABLE },

    # Sekcja 20 - Start/Stop/Kierunek
    {"id": "20_we1_mode", "name": "20.1 We1: Start/Kierunek (tryb)", "section": "20 - Start/Stop/Kierunek", "default": "2", "unit": "", "type": "num", "opcua_id": param.EXT1_COMMANDS },
    {"id": "20_edge_or_level", "name": "20.2 Start: zbocze/poziom", "section": "20 - Start/Stop/Kierunek", "default": "1", "unit": "", "type": "num", "opcua_id": param.EXT1_START_TRIGGER_TYPE },
    {"id": "20_we1_value", "name": "20.3 Wartość dla We1", "section": "20 - Start/Stop/Kierunek", "default": "1", "unit": "", "type": "num", "opcua_id": param.EXT1_IN1_SOURCE },
    {"id": "20_stop_on_disable", "name": "20.11 Zatrzymanie przy wyłączeniu zezwolenia", "section": "20 - Start/Stop/Kierunek", "default": 0, "unit": "", "type": "num", "opcua_id": param.RUN_ENABLE_STOP_MODE },
    {"id": "20_enable_source", "name": "20.12 Źródło zezwolenia na bieg", "section": "20 - Start/Stop/Kierunek", "default": "1", "unit": "", "type": "num", "opcua_id": param.RUN_ENABLE_1_SOURCE },
    {"id": "20_allow_positive", "name": "20.23 Zezwolenie na dodatnią wartość zadaną", "section": "20 - Start/Stop/Kierunek", "default": "1", "unit": "", "type": "num", "opcua_id": param.POSITIVE_SPEED_ENABLE },
    {"id": "20_allow_negative", "name": "20.24 Zezwolenie na ujemną wartość zadaną", "section": "20 - Start/Stop/Kierunek", "default": "1", "unit": "", "type": "num", "opcua_id": param.NEGATIVE_SPEED_ENABLE },

    # Sekcja 21 - Start/Stop modes (DTC etc.)
    {"id": "21_start_mode", "name": "21.1 Tryb startu", "section": "21 - Start/Zatrzymanie", "default": "2", "unit": "", "type": "num", "opcua_id": param.START_MODE },
    {"id": "21_stop_mode", "name": "21.3 Tryb zatrzymania", "section": "21 - Start/Zatrzymanie", "default": "0", "unit": "", "type": "num", "opcua_id": param.STOP_MODE },
    {"id": "21_emergency_stop_mode", "name": "21.4 Tryb zatrzymania awaryjnego", "section": "21 - Start/Zatrzymanie", "default": "0", "unit": "", "type": "num", "opcua_id": param.EMERGENCY_STOP_MODE },
    {"id": "21_emergency_source", "name": "21.5 Źródło zatrzymania awaryjnego", "section": "21 - Start/Zatrzymanie", "default": "1", "unit": "", "type": "num", "opcua_id": param.EMERGENCY_STOP_SOURCE },
    {"id": "21_zero_speed_limit", "name": "21.6 Limit prędkości zerowej", "section": "21 - Start/Zatrzymanie", "default": 30.0, "unit": "rpm", "type": "num", "opcua_id": param.ZERO_SPEED_LIMIT },

    # Sekcja 22 - wartość zadana prędkości
    {"id": "22_speed_source", "name": "22.21 Funkcja stałej prędkości", "section": "22 - Wartość zadana prędkości", "default": "1", "unit": "", "type": "num", "opcua_id": param.CONSTANT_SPEED_FUNCTION },
    {"id": "22_const_speed_select", "name": "22.22 Wybór stałej prędkości (1-7)", "section": "22 - Wartość zadana prędkości", "default": "1", "unit": "", "type": "num", "opcua_id": param.CONSTANT_SPEED_SEL1},
    {"id": "22_critical_speed1", "name": "22.51 Prędkość krytyczna 1", "section": "22 - Wartość zadana prędkości", "default": 0, "unit": "rpm", "type": "num", "opcua_id": param.CRITICAL_SPEED_FUNCTION },
    {"id": "22_critical_speed2", "name": "22.52 Prędkość krytyczna 2", "section": "22 - Wartość zadana prędkości", "default": 0.0, "unit": "rpm", "type": "num", "opcua_id": param.CRITICAL_SPEED_1_LOW },
]

# -------------------------
# Helpers
# -------------------------
def build_defaults_dict():
    """Zwraca słownik defaults {param_id: default_value} na podstawie PARAMETERS."""
    return {p["id"]: p["default"] for p in PARAMETERS}

def read_from_motor() -> dict:  #TODO: use get_values from opcua client library to read all the nodes at once
    values = {} 
    for p in PARAMETERS:
        parameter_id = p["id"]
        opcua_id = p["opcua_id"]

        motor_instance = backend_engine.get_server(ServerId.motor_drive)
        values[parameter_id] =  motor_instance.read_parameter(opcua_id)
    return values

def group_params_by_section(params: typing.List[dict]) -> dict:
    out = {}
    for p in params:
        out.setdefault(p["section"], []).append(p)
    return out

# -------------------------
# Layout generator
# -------------------------
def generate_motor_drive_parameters():
    """
    Zwraca layout panelu nadzorującego silnik.
    Zawiera:
     - dcc.Interval do odświeżania
     - dcc.Store do przechowywania defaultów
     - wygenerowane pola parametrów (etykieta, aktualna wartość, pole zmiany default)
    """
    defaults = build_defaults_dict()
    sections = group_params_by_section(PARAMETERS)

    sections_children = []
    for section_name, params in sections.items():
        rows = []
        for p in params:
            pid = p["id"]
            # id pattern dla inputów (ułatwia przyszłe callbacki)
            default_input_id = {"type": "default-input", "index": pid}
            current_value_id = {"type": "current-value", "index": pid}
            row = html.Div(
                style={
                    "display": "flex",
                    "alignItems": "center",
                    "gap": "8px",
                    "padding": "6px",
                    "borderBottom": "1px solid #eee"
                },
                children=[
                    html.Div(p["name"], style={"minWidth": "260px", "fontWeight": "600"}),
                    # aktualna wartość - to pole będzie aktualizowane w callback'ach
                    html.Div(id=current_value_id, children=str(p["default"]), style={
                        "minWidth": "160px",
                        "padding": "6px",
                        "borderRadius": "6px",
                        "border": "1px solid #ddd",
                        "textAlign": "left"
                    }),
                    html.Div([
                        html.Label("Default:"),
                        # edytowalne pole dla wartości domyślnej
                        dcc.Input(
                            id=default_input_id,
                            type="text",
                            value=str(defaults[pid]),
                            debounce=True,
                            style={"width": "160px"}
                        )
                    ]),
                    html.Div(p.get("unit", ""), style={"minWidth": "40px", "textAlign": "left"})
                ]
            )
            rows.append(row)
        section_card = html.Div([
            html.H4(section_name, style={"marginTop": "12px"}),
            html.Div(rows, style={"border": "1px solid #ddd", "borderRadius": "6px", "padding": "6px", "background": "#fafafa"})
        ], style={"marginBottom": "16px"})
        sections_children.append(section_card)

    container = html.Div([
        html.H3("Panel nadzoru silnika"),
        # Store przechowuje aktualne wartości domyślne jako słownik {param_id: value}
        dcc.Store(id="defaults-store", data=defaults),
        html.Div(id="parameters-container", children=sections_children)
    ])
    return container

# -------------------------
# Callback'y
# -------------------------
def callback_motor_drive_parameters(app: Dash):
    # 1) Aktualizacja pól aktualnych wartości co tick intervalu.
    @app.callback(
        # Outputs: dla każdego parametru uaktualnimy div z id={'type':'current-value','index': pid}
        Output({'type': 'current-value', 'index': ALL}, 'children'),
        Output({'type': 'current-value', 'index': ALL}, 'style'),
        Input('interval', 'n_intervals'),
        State('defaults-store', 'data')
    )
    def update_current_values(n_intervals, defaults_store):
        """
        Ten callback:
         - pobiera aktualne (symulowane) wartości z silnika
         - porównuje z wartościami domyślnymi w defaults_store
         - zwraca listę children i style dla każdego pola current-value
        Ważne: zastąp simulate_read_from_motor() prawdziwym odczytem z urządzenia.
        """
        # Tu zamień na rzeczywisty odczyt z silnika:
        current_values = read_from_motor()

        children_list = []
        styles_list = []
        # zachowaj kolejność zgodną z PARAMETERS
        for p in PARAMETERS:
            pid = p["id"]
            val = current_values.get(pid, None)
            # sformatuj wartości numeryczne ładnie
            if p["type"] == "num" and isinstance(val, (int, float)):
                child = str(val)
            else:
                child = str(val)
            children_list.append(child)

            # porównanie z domyślną wartością
            default_raw = defaults_store.get(pid) if defaults_store else p["default"]
            # porównujemy jako stringy, żeby nie mieć problemów z typami
            different = (str(default_raw) != str(val))
            base_style = {
                "minWidth": "160px",
                "padding": "6px",
                "borderRadius": "6px",
                "border": "1px solid #ddd",
                "textAlign": "left",
                "transition": "background 0.15s ease"
            }
            if different:
                # jeśli różne, ustaw tło (np. jasnoczerwone) — możesz zmienić kolor
                base_style["backgroundColor"] = "#ffecec"
            else:
                base_style["backgroundColor"] = "white"
            styles_list.append(base_style)

        return children_list, styles_list

    # 2) Auto-zapisywanie zmian wartości domyślnych:
    # gdy którykolwiek input default-input zmieni wartość, aktualizujemy defaults-store
    @app.callback(
        Output('defaults-store', 'data'),
        Input({'type': 'default-input', 'index': ALL}, 'value'),
        State('defaults-store', 'data')
    )
    def update_defaults_store(all_values, current_store):
        """
        Zmiany w polach 'Default' zapisujemy do dcc.Store.
        all_values jest listą wartości w takiej samej kolejności jak PARAMETERS.
        """
        if current_store is None:
            current_store = {}
        new_store = copy.deepcopy(current_store)
        # Załóż, że kolejność all_values odpowiada kolejności PARAMETERS
        for i, p in enumerate(PARAMETERS):
            try:
                raw = all_values[i]
            except Exception:
                raw = p["default"]
            # próbujemy zachować typ numeryczny jeśli to parametr numeryczny
            if p["type"] == "num":
                # spróbuj sparsować na float/int, jeśli to możliwe
                try:
                    if raw is None or raw == "":
                        new_store[p["id"]] = p["default"]
                    else:
                        # jeżeli wprowadzone całkowite -> int, inaczej float
                        if isinstance(raw, (int, float)):
                            new_store[p["id"]] = raw
                        else:
                            s = str(raw).strip()
                            if s == "":
                                new_store[p["id"]] = p["default"]
                            elif "." in s:
                                new_store[p["id"]] = float(s)
                            else:
                                new_store[p["id"]] = int(s)
                except Exception:
                    # w razie błędu parsowania zostawiamy oryginalne domyślne
                    new_store[p["id"]] = p["default"]
            else:
                # dla tekstu zapisujemy string
                new_store[p["id"]] = raw
        return new_store

