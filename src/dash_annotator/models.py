"""
Data models for the dash-annotator package.
"""

from dataclasses import dataclass


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
