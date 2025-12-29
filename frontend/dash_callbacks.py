from frontend.callbacks.test_map_input_figures import generate_test_map_input_figures, callback_test_map_input_figures
from frontend.callbacks.test_control_panel import generate_test_control_panel, callback_test_control_panel
from frontend.callbacks.sensors_data import generate_sensors_data, callback_sensors_data
from frontend.callbacks.safty import generate_safty, callback_safty
from frontend.callbacks.anomaly_detection import generate_anomaly_detection, callback_anomaly_detection
from frontend.callbacks.load_drive_parameters import generate_load_drive_parameters, callback_load_drive_parameters
from frontend.callbacks.motor_drive_parameters import generate_motor_drive_parameters, callback_motor_drive_parameters
from frontend.callbacks.system_conectivity import generate_system_conectivity, callback_system_conectivity

from dash import Dash, Input, Output

def register_callbacks(app: Dash):

    ##############################################################
    # Render Tab Content
    ##############################################################
    @app.callback( # type: ignore
        Output("tab-content", "children"),
        Input("tabs", "value")
    )
    def render_tab(tab): # type: ignore
        if tab == "test_map_input_figures":
            return generate_test_map_input_figures()
        
        elif tab == "test_control_panel":
            return generate_test_control_panel()

        elif tab == "sensors_data":
            return generate_sensors_data()
        
        elif tab == "safty":
            return generate_safty()
    
        elif tab == "anomaly_detection":
            return generate_anomaly_detection()
        
        elif tab == "load_drive_parameters":
            return generate_load_drive_parameters()
        
        elif tab == "motor_drive_parameters":
            return generate_motor_drive_parameters()
        
        elif tab == "system_conectivity":
            return generate_system_conectivity()

    callback_test_map_input_figures(app)

    callback_test_control_panel(app)

    callback_sensors_data(app)

    callback_safty(app)

    callback_anomaly_detection(app)

    callback_load_drive_parameters(app)

    callback_motor_drive_parameters(app)

    callback_system_conectivity(app)

