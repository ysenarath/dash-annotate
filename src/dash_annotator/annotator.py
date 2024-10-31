"""
DashAnnotator component for text annotation in Dash applications.
"""

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
    """
    Represents a text annotation with position and content.

    Attributes:
        id: Unique identifier for the annotation
        start: Starting position in the text
        end: Ending position in the text
        text: The annotated text content
        note: Additional note or comment about the annotation
    """

    id: str
    start: int
    end: int
    text: str
    note: str


class TextAnnotator(html.Div):
    def __init__(
        self,
        id: str,
        value: str = "",
        annotations: Optional[List[Annotation]] = None,
        className: str = "",
    ):
        self.id_ = id
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
                                    "backgroundColor": "transparent",
                                    "caretColor": "black",
                                },
                                persistence=True,
                                spellCheck=False,
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
                    className="relative border rounded-lg shadow-sm mb-4 w-100",
                )
            ],
            className=className,
        )
        # Call parent constructor with all children
        super().__init__(
            [
                text_store,
                annotations_store,
                selection_store,
                main_container,
            ]
        )
        # Add custom JavaScript for selection handling
        clientside_callback(
            ClientsideFunction(
                namespace="clientside", function_name="handleTextSelection"
            ),
            Input({"type": "textarea", "id": id}, "id"),
            prevent_initial_call=False,
        )


class AnnotateButton(html.Button):
    def __init__(self, for_: str, label: str = "Add Annotation"):
        super().__init__(
            label,
            id={"type": "add-button", "id": for_},
            className="px-4 py-2 rounded bg-gray-200 text-gray-500",
        )


class AnnotationsList(html.Div):
    def __init__(self, for_: str):
        super().__init__(
            id={"type": "annotations-list", "id": for_},
            className="space-y-2",
        )


def register_callbacks(app: dash.Dash) -> None:
    """
    Register all callbacks for the DashAnnotator component.

    This function sets up all the necessary callbacks for the component to function,
    including text updates, selection handling, and annotation management.

    Args:
        app: The Dash application instance to register callbacks with
    """

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

        # Create a list of all boundary points (start and end positions)
        boundaries = []
        for ann in annotations_data:
            boundaries.append((ann["start"], "start", ann["id"]))
            boundaries.append((ann["end"], "end", ann["id"]))

        # Sort boundaries by position
        boundaries.sort(
            key=lambda x: (x[0], x[1] != "end")
        )  # Ensure "end" comes after "start" at same position

        # Build text parts with proper handling of overlapping annotations
        parts = []
        last_pos = 0
        active_annotations = set()

        for pos, boundary_type, ann_id in boundaries:
            # Add non-annotated text before this boundary if there is any
            if pos > last_pos:
                if not active_annotations:
                    # No active annotations - render as plain text
                    parts.append(html.Span(text[last_pos:pos], id=f"text-{last_pos}"))
                else:
                    # Text with active annotations
                    parts.append(
                        html.Span(
                            text[last_pos:pos],
                            className=f"border-b-2 border-blue-400 bg-blue-50",
                            style={
                                "opacity": min(0.2 + len(active_annotations) * 0.2, 1)
                            },
                            id=f"overlap-{'-'.join(sorted(active_annotations))}",
                        )
                    )

            # Update active annotations set
            if boundary_type == "start":
                active_annotations.add(ann_id)
            else:
                active_annotations.discard(ann_id)

            last_pos = pos

        # Add remaining text after last boundary
        if last_pos < len(text):
            parts.append(html.Span(text[last_pos:], id=f"text-{last_pos}"))

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
