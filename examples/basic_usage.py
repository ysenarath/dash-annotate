"""
Basic usage example of the DashAnnotator component.

This example demonstrates how to create a simple Dash application
with the DashAnnotator component for text annotation.

Run this script and navigate to http://localhost:8050 in your browser.
"""

import time
import dash
from dash import html
from dash_annotator import TextAnnotator, AnnotateButton, AnnotationList


# Initialize the Dash app
app = dash.Dash(
    __name__,
    external_stylesheets=[],
)

# Create the layout with the DashAnnotator component
app.layout = html.Div(
    [
        TextAnnotator(id="example-annotator"),
        AnnotateButton(for_="example-annotator"),
        AnnotationList(for_="example-annotator"),
    ],
    className="w-100 p-3",
)

if __name__ == "__main__":
    try:
        app.run_server(debug=True, port=8050)
    except KeyboardInterrupt:
        print("Application stopped by user")
    except Exception as e:
        print(e)
        time.sleep(5)
