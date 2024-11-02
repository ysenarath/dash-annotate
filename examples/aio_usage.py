"""
Example usage of the TextAnnotatorAIO component.

This example demonstrates how to use the All-in-One version of the
DashAnnotator component, which encapsulates all callbacks and layout
in a single, reusable component.

Run this script and navigate to http://localhost:8050 in your browser.
"""

import os
import time
import dash
from dash import html
import dash_annotator
from dash_annotator import TextAnnotator


def get_assets_folder():
    """Get the path to the assets folder."""
    return os.path.join(os.path.dirname(dash_annotator.__file__), "assets")


# Initialize the Dash app
app = dash.Dash(
    __name__,
    external_stylesheets=[],
    assets_folder=get_assets_folder(),
)

# Create the layout with the TextAnnotatorAIO component
# Note: No need to register callbacks separately - they're included in the component
app.layout = html.Div(
    [
        html.H1("Text Annotation Example (AIO Version)", className="mb-4"),
        html.P(
            """
            This example uses the All-in-One (AIO) version of the TextAnnotator component.
            The AIO version includes all necessary callbacks and subcomponents, making it
            easier to use and more maintainable.
            """,
            className="mb-4",
        ),
        # The AIO component includes the text area, annotation button, and annotations list
        TextAnnotator(
            aio_id="example-annotator",
            value="Try selecting some text here and click 'Add Annotation' to create an annotation.",
            className="w-100",
            # Optional: Customize textarea properties
            # textarea_props={
            #     "placeholder": "Enter or paste your text here...",
            #     "style": {"minHeight": "200px"},
            # },
            # Optional: Customize button properties
            button_props={
                "style": {"marginTop": "10px"},
            },
        ),
    ],
    className="container mx-auto p-4 max-w-3xl",
)


if __name__ == "__main__":
    while True:
        try:
            app.run_server(debug=True, port=8050)
        except Exception as e:
            print(e)
            time.sleep(5)
