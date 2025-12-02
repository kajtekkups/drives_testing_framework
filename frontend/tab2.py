import plotly.express as px
import pandas as pd
from dash import Input, Output, html, dcc, State

# Example plot
example_data = pd.DataFrame({
    "x": [1, 2, 3, 4],
    "y": [10, 15, 13, 17]
})
example_fig = px.line(example_data, x="x", y="y")
example_fig.update_layout(
    width=1100,   # width in pixels
    height=700   # height in pixels
)


def generate_tab2():
    return html.Div([
        html.H3("Example input", style={"textAlign": "center"}),

        # Flex container: plot on left, inputs on right
        html.Div([
            # Left side: plot
            html.Div([
                dcc.Graph(id='my-plot', figure=example_fig)
            ], style={"flex": "70%", "padding": "10px"}),

            # Right side: inputs and button
            html.Div([
                dcc.Input(
                    id='motor_velocity_input',
                    type='number',
                    placeholder='Enter motor velocity (0-3000 rpm)'
                ),
                html.Button("Submit", id="motor_velocity_button", n_clicks=0),
                html.Div(id="motor_velocity_output")
            ], style={"flex": "30%", "padding": "10px"})
        ], style={"display": "flex"})  # Flex container
    ])

def callback_tab2(app):
    @app.callback(
        Output("motor_velocity_output", "children"),
        Input("motor_velocity_button", "n_clicks"),
        State("motor_velocity_input", "value")
    )
    def update_output(n_clicks, input_value):
        if n_clicks > 0:
            # Store the value in a variable (here just returning for display)
            stored_value = input_value
            return f"You entered: {stored_value}"
        return "No input yet."