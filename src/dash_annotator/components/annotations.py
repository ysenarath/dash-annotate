"""
Annotations component for displaying and managing annotations.
"""

from dash import html, Input, Output, State, dash
import json
import uuid


class Annotations(html.Div):
    """
    Component for displaying and managing annotations.

    Args:
        id: Unique identifier for the parent TextAnnotator instance
    """

    def __init__(self, id: str):
        super().__init__(
            id={"type": "annotations-list", "id": id},
            className="space-y-2",
        )


def register_annotations_callbacks(app: dash.Dash) -> None:
    """Register callbacks specific to the annotations component."""

    @app.callback(
        Output({"type": "annotations-store", "id": dash.MATCH}, "data"),
        Input({"type": "add-button", "id": dash.MATCH}, "n_clicks"),
        Input({"type": "remove-annotation", "index": dash.ALL}, "n_clicks"),
        State({"type": "text-store", "id": dash.MATCH}, "data"),
        State({"type": "selection-store", "id": dash.MATCH}, "data"),
        State({"type": "annotations-store", "id": dash.MATCH}, "data"),
        prevent_initial_call=True,
    )
    def manage_annotations(
        add_clicks, remove_clicks, text, selection_data, annotations_data
    ):
        """Handle adding and removing annotations."""
        ctx = dash.callback_context
        if not ctx.triggered:
            return dash.no_update
        trigger = ctx.triggered[0]["prop_id"]
        if not annotations_data:
            annotations_data = []

        # Handle adding new annotation
        if "add-button" in trigger and selection_data:
            new_annotation = {
                "id": str(uuid.uuid4()),
                "start": selection_data["start"],
                "end": selection_data["end"],
                "text": text[selection_data["start"] : selection_data["end"]],
                "note": "Sample annotation note",
            }
            return annotations_data + [new_annotation]

        # Handle removing annotation
        if "remove-annotation" in trigger:
            annotation_id = json.loads(trigger.split(".")[0])["index"]
            return [ann for ann in annotations_data if ann["id"] != annotation_id]

        return dash.no_update

    @app.callback(
        Output({"type": "annotations-list", "id": dash.MATCH}, "children"),
        Input({"type": "annotations-store", "id": dash.MATCH}, "data"),
    )
    def update_annotations_list(annotations_data):
        """Update the annotations list display."""
        if not annotations_data:
            return []
        return [
            html.Div(
                [
                    html.Div(
                        [
                            html.Div(f'"{ann["text"]}"', className="font-medium"),
                            html.Div(ann["note"], className="text-sm text-gray-600"),
                        ],
                        className="flex-1",
                    ),
                    html.Button(
                        "Remove",
                        id={"type": "remove-annotation", "index": ann["id"]},
                        className="text-red-500 hover:text-red-700",
                    ),
                ],
                className="flex items-start gap-2 p-2 bg-gray-50 rounded",
            )
            for ann in annotations_data
        ]
