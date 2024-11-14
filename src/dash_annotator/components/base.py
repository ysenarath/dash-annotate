"""
DashAnnotator component for text annotation in Dash applications.
"""

from dataclasses import dataclass
from dash_annotator.components import _ids


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
