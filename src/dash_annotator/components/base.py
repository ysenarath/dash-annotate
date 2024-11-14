"""
DashAnnotator component for text annotation in Dash applications.
"""

from dataclasses import dataclass

ID = "id"


class _ids:
    @staticmethod
    def text_store(id):
        return {
            "component": "TextAnnotator",
            "subcomponent": "text-store",
            ID: id,
        }

    @staticmethod
    def annotations_store(id):
        return {
            "component": "TextAnnotator",
            "subcomponent": "annotations-store",
            ID: id,
        }

    @staticmethod
    def selection_store(id):
        return {
            "component": "TextAnnotator",
            "subcomponent": "selection-store",
            ID: id,
        }

    @staticmethod
    def textarea(id):
        return {
            "component": "TextAnnotator",
            "subcomponent": "textarea",
            ID: id,
        }

    @staticmethod
    def textarea_listener(id):
        return {
            "component": "TextAnnotator",
            "subcomponent": "textarea-listener",
            ID: id,
        }

    @staticmethod
    def visual_text(id):
        return {
            "component": "TextAnnotator",
            "subcomponent": "visual-text",
            ID: id,
        }

    @staticmethod
    def add_button(id):
        return {
            "component": "TextAnnotator",
            "subcomponent": "add-button",
            ID: id,
        }

    @staticmethod
    def remove_annotation(id, ann_id):
        return {
            "component": "TextAnnotator",
            "subcomponent": "remove-annotation",
            ID: id,
            "ann_id": ann_id,
        }

    @staticmethod
    def annotations_list(id):
        return {
            "component": "TextAnnotator",
            "subcomponent": "annotations-list",
            ID: id,
        }

    @staticmethod
    def main_container(id):
        return {
            "component": "TextAnnotator",
            "subcomponent": "main-container",
            ID: id,
        }


@dataclass
class Annotation:
    """
    Data class for annotation objects.

    Parameters
    ----------
    id : str
        Unique identifier for the annotation.
    start : int
        Start index of the annotation.
    end : int
        End index of the annotation.
    text : str
        Text of the annotation.
    note : str
        Note for the annotation.
    """

    id: str
    start: int
    end: int
    text: str
    note: str


class BaseAnnotation:
    """Base class for annotation components."""

    ids = _ids
