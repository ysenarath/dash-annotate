"""AnnotateButton component for adding annotations."""

from dash import html, Input, Output, State, callback, MATCH
import dash
import json
import uuid

from dash_annotator.components.base import BaseAnnotation

__all__ = [
    "AnnotateButton",
]


class AnnotateButton(html.Button, BaseAnnotation):
    """AnnotateButton component for adding annotations."""

    ids = BaseAnnotation.ids

    def __init__(self, for_: str, label: str = "Add Annotation", **kwargs):
        if "className" not in kwargs:
            kwargs["className"] = ""
        kwargs["className"] = "px-4 py-2 rounded bg-gray-200 text-gray-500"
        super().__init__(
            children=label,
            id=self.ids.add_button(for_),
            **kwargs,
        )

    @callback(
        Output(ids.add_button(MATCH), "className"),
        Input(ids.selection_store(MATCH), "data"),
        Input(ids.textarea(MATCH), "n_blur"),
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

    @callback(
        Output(ids.annotations_store(MATCH), "data"),
        Input(ids.add_button(MATCH), "n_clicks"),
        Input(
            ids.remove_annotation(MATCH, dash.ALL),
            "n_clicks",
        ),
        State(ids.text_store(MATCH), "data"),
        State(ids.selection_store(MATCH), "data"),
        State(ids.annotations_store(MATCH), "data"),
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

        if "add-button" in trigger and selection_data:
            new_annotation = {
                "id": str(uuid.uuid4()),
                "start": selection_data["start"],
                "end": selection_data["end"],
                "text": text[selection_data["start"] : selection_data["end"]],
                "note": "Sample annotation note",
            }
            return annotations_data + [new_annotation]

        if "remove-annotation" in trigger:
            annotation_id = json.loads(trigger.split(".")[0])["index"]
            return [ann for ann in annotations_data if ann["id"] != annotation_id]

        return dash.no_update
