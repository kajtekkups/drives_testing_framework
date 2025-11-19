import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import random

import threading
from windows_stubs.backend import test_runner
from frontend.dash_layout import app_layout
from frontend.dash_callbacks import register_callbacks

app = dash.Dash(__name__, suppress_callback_exceptions=True)
app.layout = app_layout

# Register callbacks
register_callbacks(app)

if __name__ == '__main__':
    thread = threading.Thread(target=test_runner.run_test_loop, daemon=True)
    thread.start()

    app.run(debug=True)
