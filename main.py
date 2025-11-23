import dash

import threading
from backend.backend import backend_runner
from frontend.dash_layout import app_layout
from frontend.dash_callbacks import register_callbacks

app = dash.Dash(__name__, suppress_callback_exceptions=True)
app.layout = app_layout

# Register callbacks
register_callbacks(app)

if __name__ == '__main__':
    thread = threading.Thread(target=backend_runner.test_execution, daemon=True)
    thread.start()

    app.run(host="0.0.0.0", port=8050, debug=True)
