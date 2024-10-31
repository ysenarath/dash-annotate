"""
Basic usage example of the DashAnnotator component.

This example demonstrates how to create a simple Dash application
with the DashAnnotator component for text annotation.

Run this script and navigate to http://localhost:8050 in your browser.
"""

import os
import time
import dash
from dash import html
import dash_annotator
from dash_annotator import (
    TextAnnotator,
    register_callbacks,
    AnnotateButton,
    AnnotationsList,
)


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
        TextAnnotator(id="example-annotator", className="h-100"),
        AnnotateButton(for_="example-annotator"),
        AnnotationsList(for_="example-annotator"),
    ],
    className="w-100 p-3",
)

# Register the callbacks
register_callbacks(app)

if __name__ == "__main__":
    while True:
        try:
            app.run_server(debug=True, port=8050)
        except Exception as e:
            print(e)
            time.sleep(5)
