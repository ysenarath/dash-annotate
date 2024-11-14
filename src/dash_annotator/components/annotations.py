"""AnnotationsList component for displaying and managing annotations."""

from dash import html, callback, Output, Input, MATCH
import dash
from dash_annotator.components.base import BaseAnnotation

__all__ = [
    "AnnotationList",
]

ids = BaseAnnotation.ids


class AnnotationList(html.Div, BaseAnnotation):
    """Component for displaying and managing the list of annotations."""

    ids = BaseAnnotation.ids

    def __init__(self, for_: str, *args, **kwargs):
        """Initialize the component."""
        if "className" not in kwargs:
            kwargs["className"] = ""
        kwargs["className"] += "space-y-2 mt-4"
        self.for_id = for_
        super().__init__(id=self.ids.annotations_list(for_), *args, **kwargs)

    @callback(
        Output(ids.annotations_list(MATCH), "children"),
        Input(ids.annotations_store(MATCH), "data"),
    )
    def update_annotations_list(annotations_data):
        """Update the annotations list display."""
        if not annotations_data:
            return []
        # get input id
        annotator_id = dash.callback_context.triggered_id["id"]
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
                        id=ids.remove_annotation(annotator_id, ann["id"]),
                    ),
                ],
            )
            for ann in annotations_data
        ]
