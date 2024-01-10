"""Welcome to Reflex! This file outlines the steps to create a basic app."""
from rxconfig import config
import asyncio
import reflex as rx
from magnum.state import State

docs_url = "https://reflex.dev/docs/getting-started/introduction"
filename = f"{config.app_name}/{config.app_name}.py"


def header() -> rx.Component:
    return rx.box(
        rx.spacer(),
        rx.heading(
            "🐧 OPUS", text_align="justify", font_family="Courier New", font_size="3em"),
        rx.text(
            "LLM-based Open World Natural Language Parser with Unrestricted Semantics",
            font_family="Courier New",font_size="1.5em"
        ),
        rx.text("version 0.1", as_="i",font_family="Courier New"),
        rx.spacer(),
        rx.html("<br>"),
        rx.divider(),
        align_items="left",
        padding_left="2em",
        padding_right="2em",
        padding_top="2em",
        padding_below="2em",
    )


def input_area() -> rx.Component:
    models = ["gpt-4-0613", "gpt-4-0314", "gpt-4","gpt-3.5-turbo-16k","gpt-3.5-turbo-16k-0613"]
    return rx.vstack(
        rx.hstack(
            rx.button("Load", on_click=State.load),
            rx.input(
                value=State.current_utterance, on_change=State.set_current_utterance
            ),
            rx.button("Parse", on_click=State.parse, is_loading=State.loading),
        ),
        rx.spacer(),
        rx.hstack(
            rx.text("speaker: "),
            rx.input(value="evan", 
                     on_change=State.set_current_speaker),
            rx.text("listener: "),
            rx.input(value="self", 
                     on_change=State.set_current_listener),        
        ),
        rx.hstack(
            rx.text("model: "),
            rx.select(models, 
                      value="gpt-3.5-turbo-16k-0613",
                      placeholder="Select a model",
                      on_change=State.set_current_model)
            ),
        rx.divider(),
        edit_area(),
        align_items="left",
        padding_left="2em",
    )


def output_area() -> rx.Component:
    return rx.tabs(
        rx.tab_list(
            rx.tab("TRADE Semantics"),
            rx.tab("Surface Meaning Representation (SMR)"),
        ),
        rx.tab_panels(
            rx.tab_panel(rx.text(State.current_trade_parse, font_size="1.2em", font_family="Courier New")),
            rx.tab_panel(
                rx.code_block(State.pretty_smr, language="json", font_size="0.7em")
            ),
        ),
        bg="white",
        color="black",
        shadow="lg",
        padding_right="2em",
    )


def edit_area() -> rx.Component:
    return rx.card(
        rx.text(
            rx.vstack(
                rx.input(placeholder="User"),
                rx.input(value=State.current_trade_parse),
                rx.button("Submit"),
            )
        ),
        header=rx.heading("🖋️ Verify the Parse", size="md"),
        padding_left="2em",
        padding_right="2em",
    )


def index() -> rx.Component:
    return rx.grid(
        rx.grid_item(header(), row_span=1, col_span=4, bg="white"),
        rx.grid_item(input_area(), row_span=1, col_span=2, bg="white"),
        rx.grid_item(
            output_area(),
            row_span=1,
            col_span=2,
            bg="white",
            padding_left="2em",
            padding_right="2em",
        ),
        template_rows="repeat(7, 1fr)",
        template_columns="repeat(4, 1fr)",
        h="200px",
        width="100%",
        gap=4,
    )


# Add state and page to the app.
app = rx.App()
app.add_page(index)
#app.compile()
