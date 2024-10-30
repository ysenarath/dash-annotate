# app.py
import os
import dash
from dash import html
import dash_bootstrap_components as dbc
from annotated_text import AnnotatedText, register_callbacks


def get_assets_folder():
    """Get the path to the assets folder."""
    return os.path.join(os.path.dirname(__file__), "assets")


# Initialize the Dash app with Tailwind CSS
app = dash.Dash(
    __name__,
    external_stylesheets=[],
    assets_folder=get_assets_folder(),
)

# Create the layout
app.layout = html.Div(
    [
        AnnotatedText(
            id="my-annotated-text",
            value="",  # Start with empty textarea
            className="max-w-2xl mx-auto",
        )
    ]
)

# Register the callbacks
register_callbacks(app)

if __name__ == "__main__":
    app.run_server(debug=True, port=8050)  # Using port 8052 instead
