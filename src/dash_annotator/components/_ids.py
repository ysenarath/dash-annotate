def text_store(id):
    return {
        "component": "TextAnnotator",
        "subcomponent": "text-store",
        "id": id,
    }


def annotations_store(id):
    return {
        "component": "TextAnnotator",
        "subcomponent": "annotations-store",
        "id": id,
    }


def selection_store(id):
    return {
        "component": "TextAnnotator",
        "subcomponent": "selection-store",
        "id": id,
    }


def textarea(id):
    return {
        "component": "TextAnnotator",
        "subcomponent": "textarea",
        "id": id,
    }


def textarea_listener(id):
    return {
        "component": "TextAnnotator",
        "subcomponent": "textarea-listener",
        "id": id,
    }


def visual_text(id):
    return {
        "component": "TextAnnotator",
        "subcomponent": "visual-text",
        "id": id,
    }


def add_button(id):
    return {
        "component": "TextAnnotator",
        "subcomponent": "add-button",
        "id": id,
    }


def remove_annotation(id, index):
    return {
        "component": "TextAnnotator",
        "subcomponent": "remove-annotation",
        "id": id,
        "index": index,
    }


def annotations_list(id):
    return {
        "component": "TextAnnotator",
        "subcomponent": "annotations-list",
        "id": id,
    }


def main_container(id):
    return {
        "component": "TextAnnotator",
        "subcomponent": "main-container",
        "id": id,
    }
