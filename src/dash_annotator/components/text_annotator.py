"""
Main TextAnnotator component that orchestrates text annotation functionality.
"""

from dash import (
    html,
    dcc,
    Input,
    Output,
    ClientsideFunction,
    clientside_callback,
)
import dash
from dataclasses import asdict
from typing import List, Optional
from dash_extensions import EventListener

from .annotate_button import AnnotateButton
from .annotations import Annotations
from ..models import Annotation


class TextAnnotator(html.Div):
    """
    A Dash component for interactive text annotation.

    This component allows users to select text and create annotations with notes.
    It provides a rich interface for managing annotations including adding,
    viewing, and removing them.

    Args:
        id: Unique identifier for the component instance
        value: Initial text content
        annotations: List of initial annotations
        className: Additional CSS classes for styling
    """

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
                        # Textarea for editing
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
                    className="relative border rounded-lg shadow-sm mb-4",
                ),
                # Controls
                html.Div(
                    [AnnotateButton(id=id)],
                    className="flex gap-4 mb-4",
                ),
                # Annotations list
                Annotations(id=id),
                # Instructions
                html.Div(
                    "Select text and click 'Add Annotation' to create an annotation.",
                    className="mt-2 text-sm text-gray-600",
                ),
            ],
            className=f"p-4 {className}",
        )

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


def register_text_annotator_callbacks(app: dash.Dash) -> None:
    """Register callbacks specific to the text annotator component."""

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

        # Create a list of all boundary points
        boundaries = []
        for ann in annotations_data:
            boundaries.append((ann["start"], "start", ann["id"]))
            boundaries.append((ann["end"], "end", ann["id"]))

        # Sort boundaries by position
        boundaries.sort(key=lambda x: (x[0], x[1] != "end"))

        # Build text parts with proper handling of overlapping annotations
        parts = []
        last_pos = 0
        active_annotations = set()

        for pos, boundary_type, ann_id in boundaries:
            if pos > last_pos:
                if not active_annotations:
                    parts.append(html.Span(text[last_pos:pos], id=f"text-{last_pos}"))
                else:
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

            if boundary_type == "start":
                active_annotations.add(ann_id)
            else:
                active_annotations.discard(ann_id)

            last_pos = pos

        if last_pos < len(text):
            parts.append(html.Span(text[last_pos:], id=f"text-{last_pos}"))

        return parts
