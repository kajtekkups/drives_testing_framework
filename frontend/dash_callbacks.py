import sys

if sys.platform.startswith('win'):
    from windows_stubs.backend import backend_engine
elif sys.platform.startswith('linux'):
    from backend.backend import backend_engine
else:
    print("Unsupported OS")

from frontend.tab1 import generate_tab1, callback_tab1
from frontend.tab2 import generate_tab2, callback_tab2
from frontend.tab3 import generate_tab3, callback_tab3

from dash import Input, Output, State

def register_callbacks(app):

    ##############################################################
    # Render Tab Content
    ##############################################################
    @app.callback(
        Output("tab-content", "children"),
        Input("tabs", "value")
    )
    def render_tab(tab):
        if tab == "tab1":
            return generate_tab1()
        
        elif tab == "tab2":
            return generate_tab2()

        elif tab == "tab3":
            return generate_tab3()
    

    ##############################################################
    # ➤ Update input graph
    ##############################################################
    callback_tab1(app)

    ##############################################################
    # ➤ velocity control input
    ##############################################################  
    callback_tab2(app)

    ##############################################################
    # ➤ Update Plots 1–4
    ##############################################################
    callback_tab3(app)