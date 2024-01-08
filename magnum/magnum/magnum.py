"""Welcome to Reflex! This file outlines the steps to create a basic app."""
from rxconfig import config

import reflex as rx

docs_url = "https://reflex.dev/docs/getting-started/introduction"
filename = f"{config.app_name}/{config.app_name}.py"


class ParseState(rx.State):
    """The app state."""

    pass


def header() -> rx.Component:
    return rx.box(
        rx.spacer(),
        rx.text("🐧 OPUS", text_align="justify", font_family="Courier New", font_size="3em"),
        rx.text("Open World Natural Language Parser with Unrestricted Semantics", font_family="Courier New"),
        rx.spacer(),
        rx.html("<br>"),
        rx.divider(),
        align_items="left",
        padding_left="2em",
        padding_right="2em",
        padding_top="2em",
        padding_below="2em"
    )

def input_area() -> rx.Component:
    return rx.box(
            rx.hstack(
                rx.input(),
                rx.button("Parse")
            ),
            align_items="left",
        padding_left="2em",

    )

def output_area() -> rx.Component:
    return rx.tabs(
    rx.tab_list(
        rx.tab("Trade Semantics"),
        rx.tab("Surface Meaning Representation (SMR)"),
    ),
    rx.tab_panels(
        rx.tab_panel(rx.text("Text from tab 1.")),
        rx.tab_panel(rx.checkbox("Text from tab 2.")),
    ),
    bg="white",
    color="black",
    shadow="lg",
    padding_right="2em"
)

def edit_area() -> rx.Component:
    return rx.card(
    rx.text("Body of the Card Component"),
    header=rx.heading("🖋️ Magnum Opus", size="lg"),
    footer=rx.heading("Footer", size="sm"),
    padding_left="2em",
        padding_right="2em",
)


def index() -> rx.Component:
    return rx.grid(
        rx.grid_item(header(), row_span=1, col_span=4, bg="white"),
        rx.grid_item(input_area(), row_span=2, col_span=2, bg="white"),
        rx.grid_item(output_area(), row_span=1, col_span=2, bg="white", padding_left="2em",
        padding_right="2em"),
        rx.grid_item(edit_area(), row_span=4, col_span=4, bg="white", padding_left="2em",
        padding_right="2em"),
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