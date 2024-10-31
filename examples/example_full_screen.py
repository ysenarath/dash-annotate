from dash import Dash, html

app = Dash(__name__)

# Define custom CSS
app.index_string = """
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
        <style>
            /* Remove all scrollbars and ensure full size */
            html, body {
                margin: 0;
                height: 100vh;
                width: 100vw;
                overflow: hidden;
            }
            #react-entry-point {
                height: 100vh;
                overflow: hidden;
            }
        </style>
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
"""

sidebar = html.Div(
    [
        html.H1("Sidebar"),
        html.P("This is the sidebar."),
    ],
    style={
        "flex": "0 0 200px",
        "background-color": "#f8f9fa",
        "className": "p-3",
    },
)

main_content = html.Div(
    [
        html.H1("Main content"),
        html.P("This is the main content."),
    ],
    style={
        "flex": "1",
        "className": "p-3",
    },
)

# Create the layout
app.layout = html.Div(
    [
        sidebar,
        main_content,
    ],
    style={
        "display": "flex",
        "flex-direction": "row",
        "height": "100vh",
        "width": "100vw",
        "margin": 0,
        "padding": 0,
    },
)

if __name__ == "__main__":
    app.run_server(debug=True)
