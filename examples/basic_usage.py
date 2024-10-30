"""
Basic usage example of the DashAnnotator component.

This example demonstrates how to create a simple Dash application
with the DashAnnotator component for text annotation.

Run this script and navigate to http://localhost:8050 in your browser.
"""

import os
import dash
from dash import html
import dash_annotator
from dash_annotator import TextAnnotator, register_callbacks


def get_assets_folder():
    """Get the path to the assets folder."""
    return os.path.join(os.path.dirname(dash_annotator.__file__), "assets")


# Initialize the Dash app
app = dash.Dash(
    __name__,
    external_stylesheets=[],
    assets_folder=get_assets_folder(),
)

# Create the layout with the DashAnnotator component
app.layout = html.Div(
    [
        html.H1(
            "DashAnnotator Example", className="text-2xl font-bold mb-4 text-center"
        ),
        TextAnnotator(
            id="example-annotator",
            value="Try selecting some text in this area and click 'Add Annotation' to create annotations.",
            className="max-w-2xl mx-auto",
        ),
    ]
)

# Register the callbacks
register_callbacks(app)

if __name__ == "__main__":
    app.run_server(debug=True, port=8050)
