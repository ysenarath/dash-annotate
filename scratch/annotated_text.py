# annotated_text.py
from dash import (
    html,
    dcc,
    Input,
    Output,
    State,
    ClientsideFunction,
    clientside_callback,
)
import dash
import json
from dataclasses import dataclass, asdict
from typing import List, Optional
import uuid
from dash_extensions import EventListener


@dataclass
class Annotation:
    id: str
    start: int
    end: int
    text: str
    note: str


class AnnotatedText(html.Div):
    """A Dash component for text editing with annotations."""

    def __init__(
        self,
        id: str,
        value: str = "",
        annotations: Optional[List[Annotation]] = None,
        className: str = "",
    ):
        if annotations is None:
            annotations = []
        text_store = dcc.Store(
            id={"type": "text-store", "id": id},
            data=value,
        )
        annotations_store = dcc.Store(
            id={"type": "annotations-store", "id": id},
            data=[asdict(ann) for ann in annotations],
        )
        selection_store = dcc.Store(
            id={"type": "selection-store", "id": id},
            data=None,
        )
        event_props = [
            "srcElement.selectionStart",
            "srcElement.selectionEnd",
            "srcElement.id",
        ]
        events = [
            {"event": "select", "props": event_props},
            {"event": "mouseup", "props": event_props},
            {"event": "keyup", "props": event_props},
            {"event": "focusout", "props": event_props},
        ]
        main_container = html.Div(
            [
                # Editor area
                html.Div(
                    [
                        # Textarea for editing - using only supported attributes
                        EventListener(
                            dcc.Textarea(
                                id={"type": "textarea", "id": id},
                                value=value,
                                placeholder="Type or paste text here to annotate...",
                                className="w-full h-48 p-3 text-lg bg-transparent resize-none absolute top-0 left-0 z-10",
                                style={
                                    "spellCheck": "false",
                                    # Add CSS properties that might help prevent autofill
                                    "backgroundColor": "transparent",
                                    "caretColor": "black",
                                },
                                persistence=True,
                                spellCheck=False,  # Using supported attribute
                            ),
                            events=events,
                            id={"type": "textarea-listener", "id": id},
                        ),
                        # Visual representation div
                        html.Div(
                            id={"type": "visual-text", "id": id},
                            className="w-full h-48 p-3 text-lg whitespace-pre-wrap pointer-events-none",
                        ),
                    ],
                    className="relative border rounded-lg shadow-sm mb-4",
                ),
                # Controls
                html.Div(
                    [
                        html.Button(
                            "Add Annotation",
                            id={"type": "add-button", "id": id},
                            className="px-4 py-2 rounded bg-gray-200 text-gray-500",
                        ),
                    ],
                    className="flex gap-4 mb-4",
                ),
                # Annotations list
                html.Div(
                    id={"type": "annotations-list", "id": id},
                    className="space-y-2",
                ),
                # Instructions
                html.Div(
                    "Select text and click 'Add Annotation' to create an annotation.",
                    className="mt-2 text-sm text-gray-600",
                ),
            ],
            className=f"p-4 {className}",
        )
        # Call parent constructor with all children
        super().__init__(
            [
                # Hidden stores for state management
                text_store,
                annotations_store,
                selection_store,
                # Main editor container
                main_container,
            ]
        )
        # Add custom JavaScript for selection handling
        clientside_callback(
            ClientsideFunction(
                namespace="clientside", function_name="handleTextSelection"
            ),
            # Output({"type": "selection-store", "id": id}, "data"),
            Input({"type": "textarea", "id": id}, "id"),
            prevent_initial_call=False,
        )


def register_callbacks(app):
    """Register all callbacks for the AnnotatedText component."""

    @app.callback(
        Output({"type": "text-store", "id": dash.MATCH}, "data"),
        Input({"type": "textarea", "id": dash.MATCH}, "value"),
    )
    def update_text_store(value):
        """Update the text store when textarea changes."""
        return value

    @app.callback(
        Output({"type": "selection-store", "id": dash.MATCH}, "data"),
        Input({"type": "textarea-listener", "id": dash.MATCH}, "n_events"),
        Input({"type": "textarea-listener", "id": dash.MATCH}, "event"),
    )
    def update_selection_store(n_events, event):
        """Update the selection store when selection changes."""
        # if not dash.callback_context.triggered:
        #     return None
        # n_blur_prop = dash.callback_context.triggered[0]["prop_id"]
        # if n_blur_prop.endswith(".n_clicks"):
        #     return None
        if event:
            start = event["srcElement.selectionStart"]
            end = event["srcElement.selectionEnd"]
            if start != end:
                return {"start": start, "end": end}
        return None

    @app.callback(
        Output({"type": "visual-text", "id": dash.MATCH}, "children"),
        Input({"type": "text-store", "id": dash.MATCH}, "data"),
        Input({"type": "annotations-store", "id": dash.MATCH}, "data"),
    )
    def update_visual_text(text, annotations_data):
        """Update the visual representation of text with annotations."""
        if not text:
            return ""
        if not annotations_data:
            annotations_data = []
        # Sort annotations by start position
        sorted_annotations = sorted(annotations_data, key=lambda x: x["start"])
        # Build text parts with annotations
        parts = []
        last_index = 0
        for annotation in sorted_annotations:
            # Add text before annotation
            if annotation["start"] > last_index:
                parts.append(
                    html.Span(
                        text[last_index : annotation["start"]], id=f"text-{last_index}"
                    )
                )
            # Add annotated text
            parts.append(
                html.Span(
                    text[annotation["start"] : annotation["end"]],
                    className="border-b-2 border-blue-400 bg-blue-50",
                    id=f"annotation-{annotation['id']}",
                )
            )
            last_index = annotation["end"]
        # Add remaining text
        if last_index < len(text):
            parts.append(html.Span(text[last_index:], id=f"text-{last_index}"))
        return parts

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
