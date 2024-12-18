"""DashAnnotator component for text annotation in Dash applications."""

from dash import html, dcc, Input, Output, clientside_callback, callback, MATCH, ALL
from dataclasses import asdict
from typing import List, Optional

from dash_extensions import EventListener
from dash_annotator.components.base import BaseAnnotation, Annotation

DEFAULT_FONT = "-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen-Sans, Ubuntu, Cantarell, 'Helvetica Neue', sans-serif"


clientside_callback(
    """function(id) {
    const selection = window.getSelection();
    console.log(selection);
    if (selection.rangeCount > 0) {
        const range = selection.getRangeAt(0);
        const textarea = document.querySelector(`#${id}`);
        console.log(textarea);
        if (textarea && range.startContainer.parentElement.id === id) {
            return {
                start: textarea.selectionStart,
                end: textarea.selectionEnd
            };
        }
    }
    return null;
}""",
    Input(BaseAnnotation.ids.textarea(ALL), "id"),
    prevent_initial_call=False,
)

clientside_callback(
    """function(n_events, event) {
    event.forEach(e => {
        if ("srcElement.scrollTop" in e) {   
            return e["srcElement.scrollTop"];
        }
    });
}""",
    Output(BaseAnnotation.ids.visual_text(MATCH), "scrollTop"),
    Input(BaseAnnotation.ids.textarea_listener(MATCH), "n_events"),
    Input(BaseAnnotation.ids.textarea_listener(MATCH), "event"),
)


class TextAnnotator(html.Div, BaseAnnotation):
    """
    An All-in-One component for text annotation in Dash applications.
    """

    ids = BaseAnnotation.ids

    def __init__(
        self,
        id: str,
        value: str = "",
        annotations: Optional[List[Annotation]] = None,
        textarea_props: dict = None,
    ):
        if annotations is None:
            annotations = []
        if textarea_props is None:
            textarea_props = {}
        # Event listener configuration
        event_props = [
            "srcElement.selectionStart",
            "srcElement.selectionEnd",
            "srcElement.id",
        ]
        scroll_event_props = [
            *event_props,
            "srcElement.scrollTop",
            "srcElement.scrollLeft",
            "srcElement.scrollHeight",
            "srcElement.scrollWidth",
            "srcElement.clientHeight",
            "srcElement.clientWidth",
        ]
        events = [
            {"event": "select", "props": event_props},
            {"event": "mouseup", "props": event_props},
            {"event": "keyup", "props": event_props},
            {"event": "focusout", "props": event_props},
            {"event": "scroll", "props": scroll_event_props},
            {"event": "mousewheel", "props": scroll_event_props},
            {"event": "keydown", "props": scroll_event_props},
        ]
        # Initialize parent
        stores = [
            dcc.Store(
                id=self.ids.text_store(id),
                data=value,
            ),
            dcc.Store(
                id=self.ids.annotations_store(id),
                data=[asdict(ann) for ann in annotations],
            ),
            dcc.Store(
                id=self.ids.selection_store(id),
                data=None,
            ),
        ]
        super().__init__(
            [
                *stores,
                html.Div(
                    [
                        EventListener(  # Textarea with event listener
                            dcc.Textarea(
                                id=self.ids.textarea(id),
                                value=value,
                                placeholder="Type or paste text here to annotate...",
                                style={
                                    "position": "absolute",
                                    "top": "0",
                                    "left": "0",
                                    "width": "100%",
                                    "height": "100%",
                                    "padding": "0.5rem",
                                    "fontFamily": DEFAULT_FONT,
                                    "fontSize": "1rem",
                                    "lineHeight": "1rem",
                                    "border": "none",
                                    "resize": "none",
                                    "color": "transparent",
                                    "caretColor": "black",
                                    "background": "transparent",
                                    "whiteSpace": "pre-wrap",
                                    "overflowWrap": "break-word",
                                    "overflowY": "auto",
                                    "zIndex": "2",
                                    "boxSizing": "border-box",
                                },
                                persistence=True,
                                spellCheck=False,
                                **textarea_props,
                            ),
                            events=events,
                            id=self.ids.textarea_listener(id),
                        ),
                        # Visual text representation
                        html.Div(
                            id=self.ids.visual_text(id),
                            style={
                                "position": "absolute",
                                "top": "0",
                                "left": "0",
                                # "right": "0",
                                # "bottom": "0",
                                "width": "100%",
                                "height": "100%",
                                "padding": "0.5rem",
                                "fontSize": "1rem",
                                "lineHeight": "1rem",
                                "whiteSpace": "pre-wrap",
                                "pointerEvents": "none",
                                "fontFamily": DEFAULT_FONT,
                            },
                        ),
                    ],
                    style={
                        "position": "absolute",
                        "top": "0",
                        "left": "0",
                        "right": "0",
                        "bottom": "0",
                        "padding": "0.5rem",
                        "fontFamily": DEFAULT_FONT,
                        "fontSize": "1rem",
                        "lineHeight": "1rem",
                        "whiteSpace": "pre-wrap",
                        "overflowWrap": "break-word",
                        "wordWrap": "break-word",
                        "overflowY": "auto",
                        "zIndex": "1",
                        "boxSizing": "border-box",
                    },
                ),
            ],
            style={
                "position": "relative",
                "borderRadius": "0.5rem",
                "borderWidth": "1px",
                "boxShadow": "0 1px 2px 0 rgba(0, 0, 0, 0.05)",
                "minHeight": "3rem",
                # "width": "500px",
                # "height": "300px",
            },
            id=self.ids.main_container(id),
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
                            # className=f"border-b-2 border-blue-400 bg-blue-50",
                            style={
                                "opacity": min(0.2 + len(active_annotations) * 0.2, 1),
                                "borderBottomWidth": "2px",
                                "borderColor": "blue",
                                "backgroundColor": "blue",
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
