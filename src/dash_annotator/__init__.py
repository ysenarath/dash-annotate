"""
DashAnnotator component for text annotation in Dash applications.
"""

from .components.text_annotator import TextAnnotator, register_text_annotator_callbacks
from .components.annotate_button import register_annotate_button_callbacks
from .components.annotations import register_annotations_callbacks
from .models import Annotation


def register_callbacks(app):
    """
    Register all callbacks for the DashAnnotator component.

    This function sets up all the necessary callbacks for the component to function,
    including text updates, selection handling, and annotation management.

    Args:
        app: The Dash application instance to register callbacks with
    """
    register_text_annotator_callbacks(app)
    register_annotate_button_callbacks(app)
    register_annotations_callbacks(app)


__all__ = ["TextAnnotator", "Annotation", "register_callbacks"]
