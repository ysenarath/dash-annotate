"""
AnnotateButton component for adding annotations.
"""

from dash import html, Input, Output, dash


class AnnotateButton(html.Button):
    """
    Button component for adding annotations.

    Args:
        id: Unique identifier for the parent TextAnnotator instance
    """

    def __init__(self, id: str):
        super().__init__(
            "Add Annotation",
            id={"type": "add-button", "id": id},
            className="px-4 py-2 rounded bg-gray-200 text-gray-500",
        )


def register_annotate_button_callbacks(app: dash.Dash) -> None:
    """Register callbacks specific to the annotate button component."""

    @app.callback(
        Output({"type": "add-button", "id": dash.MATCH}, "className"),
        Input({"type": "selection-store", "id": dash.MATCH}, "data"),
        Input({"type": "textarea", "id": dash.MATCH}, "n_blur"),
    )
    def update_button_state(selection_data, n_blur):
        """Update the Add Annotation button state based on text selection."""
        if not dash.callback_context.triggered:
            return None
        n_blur_prop = dash.callback_context.triggered[0]["prop_id"]
        has_lost_focus = n_blur_prop.endswith(".n_blur")
        base_class = "px-4 py-2 rounded "
        return base_class + (
            "bg-blue-500 text-white hover:bg-blue-600"
            if selection_data and not has_lost_focus
            else "bg-gray-200 text-gray-500 cursor-not-allowed"
        )
