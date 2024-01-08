"""Welcome to Reflex! This file outlines the steps to create a basic app."""
from rxconfig import config

import reflex as rx

docs_url = "https://reflex.dev/docs/getting-started/introduction"
filename = f"{config.app_name}/{config.app_name}.py"


class ParseState(rx.State):
    """The app state."""

    pass


def header() -> rx.Component:
    return rx.text("header")

def input_area() -> rx.Component:
    return rx.text("Input area")

def output_area() -> rx.Component:
    return rx.text("Output area")

def edit_area() -> rx.Component:
    return rx.text("Edit area")


def index() -> rx.Component:
    return rx.grid(
        rx.grid_item(header(), row_span=1, col_span=4, bg="lightblue"),
        rx.grid_item(input_area(), row_span=2, col_span=2, bg="lightgreen"),
        rx.grid_item(output_area(), row_span=1, col_span=2, bg="lightgreen"),
        rx.grid_item(edit_area(), row_span=4, col_span=4, bg="orange"),
        template_rows="repeat(7, 1fr)",
        template_columns="repeat(4, 1fr)",
        h="200px",
        width="100%",
        gap=4,
    )

# Add state and page to the app.
app = rx.App()
app.add_page(index)
app.compile()


"""
rx.grid(
    rx.grid_item(row_span=2, col_span=1, bg="lightblue"),
    rx.grid_item(col_span=2, bg="lightgreen"),
    rx.grid_item(col_span=1, bg="yellow"),
    rx.grid_item(col_span=3, bg="orange"),
    template_rows="repeat(2, 1fr)",
    template_columns="repeat(4, 1fr)",
    h="200px",
    width="100%",
    gap=4,
)
"""