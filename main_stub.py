import dash

import threading
from windows_stubs.backend import backend_engine
from frontend.dash_layout import app_layout
from frontend.dash_callbacks import register_callbacks

app = dash.Dash(__name__, suppress_callback_exceptions=True)
app.layout = app_layout

# Register callbacks
register_callbacks(app)

if __name__ == '__main__':
    thread = threading.Thread(target=backend_engine.test_execution, daemon=True)
    thread.start()

    app.run(debug=True, port=8051)
