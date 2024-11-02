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
    callback,
    MATCH,
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
    """
    An All-in-One component for text annotation in Dash applications.
    """

    class ids:
        @staticmethod
        def text_store(aio_id):
            return {
                "component": "TextAnnotator",
                "subcomponent": "text-store",
                "aio_id": aio_id,
            }

        @staticmethod
        def annotations_store(aio_id):
            return {
                "component": "TextAnnotator",
                "subcomponent": "annotations-store",
                "aio_id": aio_id,
            }

        @staticmethod
        def selection_store(aio_id):
            return {
                "component": "TextAnnotator",
                "subcomponent": "selection-store",
                "aio_id": aio_id,
            }

        @staticmethod
        def textarea(aio_id):
            return {
                "component": "TextAnnotator",
                "subcomponent": "textarea",
                "aio_id": aio_id,
            }

        @staticmethod
        def textarea_listener(aio_id):
            return {
                "component": "TextAnnotator",
                "subcomponent": "textarea-listener",
                "aio_id": aio_id,
            }

        @staticmethod
        def visual_text(aio_id):
            return {
                "component": "TextAnnotator",
                "subcomponent": "visual-text",
                "aio_id": aio_id,
            }

        @staticmethod
        def add_button(aio_id):
            return {
                "component": "TextAnnotator",
                "subcomponent": "add-button",
                "aio_id": aio_id,
            }

        @staticmethod
        def remove_annotation(aio_id, index):
            return {
                "component": "TextAnnotator",
                "subcomponent": "remove-annotation",
                "aio_id": aio_id,
                "index": index,
            }

        @staticmethod
        def annotations_list(aio_id):
            return {
                "component": "TextAnnotator",
                "subcomponent": "annotations-list",
                "aio_id": aio_id,
            }

    def __init__(
        self,
        aio_id: str,
        value: str = "",
        annotations: Optional[List[Annotation]] = None,
        className: str = "",
        textarea_props: dict = None,
        button_props: dict = None,
    ):
        """
        Initialize TextAnnotator component.

        Args:
            aio_id: Unique identifier for this component instance
            value: Initial text value
            annotations: Initial list of annotations
            className: CSS class for the main container
            textarea_props: Additional props for the textarea
            button_props: Additional props for the add button
        """
        if annotations is None:
            annotations = []
        if textarea_props is None:
            textarea_props = {}
        if button_props is None:
            button_props = {}

        # Stores
        text_store = dcc.Store(
            id=self.ids.text_store(aio_id),
            data=value,
        )
        annotations_store = dcc.Store(
            id=self.ids.annotations_store(aio_id),
            data=[asdict(ann) for ann in annotations],
        )
        selection_store = dcc.Store(
            id=self.ids.selection_store(aio_id),
            data=None,
        )

        # Event listener configuration
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

        # Main container
        main_container = html.Div(
            [
                html.Div(
                    [
                        # Textarea with event listener
                        EventListener(
                            dcc.Textarea(
                                id=self.ids.textarea(aio_id),
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
                                **textarea_props,
                            ),
                            events=events,
                            id=self.ids.textarea_listener(aio_id),
                        ),
                        # Visual text representation
                        html.Div(
                            id=self.ids.visual_text(aio_id),
                            className="w-full h-48 p-3 text-lg whitespace-pre-wrap pointer-events-none",
                        ),
                    ],
                    className="relative border rounded-lg shadow-sm mb-4 w-100",
                ),
                # Annotation controls
                html.Div(
                    [
                        html.Button(
                            "Add Annotation",
                            id=self.ids.add_button(aio_id),
                            className="px-4 py-2 rounded bg-gray-200 text-gray-500",
                            **button_props,
                        ),
                        html.Div(
                            id=self.ids.annotations_list(aio_id),
                            className="space-y-2 mt-4",
                        ),
                    ]
                ),
            ],
            className=className,
        )

        # Initialize parent
        super().__init__(
            [
                text_store,
                annotations_store,
                selection_store,
                main_container,
            ]
        )

        # Add clientside callback for selection handling
        clientside_callback(
            ClientsideFunction(
                namespace="clientside", function_name="handleTextSelection"
            ),
            Input(self.ids.textarea(aio_id), "id"),
            prevent_initial_call=False,
        )

    @callback(
        Output(ids.text_store(MATCH), "data"),
        Input(ids.textarea(MATCH), "value"),
    )
    def update_text_store(value):
        """Update the text store when textarea changes."""
        return value

    @callback(
        Output(ids.selection_store(MATCH), "data"),
        Input(ids.textarea_listener(MATCH), "n_events"),
        Input(ids.textarea_listener(MATCH), "event"),
    )
    def update_selection_store(n_events, event):
        """Update the selection store when selection changes."""
        if event:
            start = event["srcElement.selectionStart"]
            end = event["srcElement.selectionEnd"]
            if start != end:
                return {"start": start, "end": end}
        return None

    @callback(
        Output(ids.visual_text(MATCH), "children"),
        Input(ids.text_store(MATCH), "data"),
        Input(ids.annotations_store(MATCH), "data"),
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
            {
                "component": "TextAnnotator",
                "subcomponent": "remove-annotation",
                "aio_id": MATCH,
                "index": dash.ALL,
            },
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

    @callback(
        Output(ids.annotations_list(MATCH), "children"),
        Input(ids.annotations_store(MATCH), "data"),
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
                        id=TextAnnotator.ids.remove_annotation(MATCH, ann["id"]),
                        className="text-red-500 hover:text-red-700",
                    ),
                ],
                className="flex items-start gap-2 p-2 bg-gray-50 rounded",
            )
            for ann in annotations_data
        ]
