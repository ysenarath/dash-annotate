# DashAnnotator

A Dash component for interactive text annotation. This component allows users to select text and create, manage, and visualize annotations with notes.

## Features

- Interactive text selection and annotation
- Visual highlighting of annotated text
- Support for overlapping annotations
- Add and remove annotations with notes
- Fully integrated with Dash callbacks
- Responsive and customizable design

## Installation

```bash
pip install dash-annotator
```

## Quick Start

```python
import dash
from dash import html
from dash_annotator import DashAnnotator, register_callbacks

# Initialize the Dash app
app = dash.Dash(__name__)

# Create the layout with DashAnnotator
app.layout = html.Div([
    DashAnnotator(
        id="my-annotator",
        value="Try selecting some text here to create annotations.",
        className="max-w-2xl mx-auto",
    )
])

# Register the callbacks
register_callbacks(app)

if __name__ == "__main__":
    app.run_server(debug=True)
```

## Usage

### Basic Component

The `DashAnnotator` component can be initialized with the following properties:

- `id` (str, required): Unique identifier for the component
- `value` (str, optional): Initial text content
- `annotations` (List[Annotation], optional): List of initial annotations
- `className` (str, optional): Additional CSS classes for styling

### Annotation Format

Annotations are represented using the `Annotation` dataclass with the following fields:

```python
@dataclass
class Annotation:
    id: str        # Unique identifier
    start: int     # Start position in text
    end: int       # End position in text
    text: str      # Annotated text content
    note: str      # Additional note/comment
```

### Example with Pre-existing Annotations

```python
from dash_annotator import DashAnnotator, Annotation

# Create initial annotations
annotations = [
    Annotation(
        id="1",
        start=0,
        end=5,
        text="Hello",
        note="Greeting annotation"
    )
]

# Use in layout
app.layout = html.Div([
    DashAnnotator(
        id="annotator-with-data",
        value="Hello World! This is an example.",
        annotations=annotations,
        className="max-w-2xl mx-auto",
    )
])
```

## Styling

The component uses Tailwind CSS classes by default but can be customized using the `className` prop. Make sure to include Tailwind CSS in your project for the default styling to work.

## Development

To run the example:

1. Clone the repository
2. Install dependencies: `pip install -e .`
3. Run the example: `python examples/basic_usage.py`
4. Open http://localhost:8050 in your browser

## License

MIT License

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
