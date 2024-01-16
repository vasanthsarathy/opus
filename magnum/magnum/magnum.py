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
            "🐧 OPUS",text_align="justify", font_family="Courier New", font_size="3em"
        ),
        rx.text(
            "LLM-based Open World Natural Language Parser with Unrestricted Semantics",
            font_family="Courier New",
            font_size="1.5em",
        ),
        rx.text("version 0.1", as_="i", font_family="Courier New"),
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
    models = [
        "gpt-4-0613",
        "gpt-4-0314",
        "gpt-4",
        "gpt-3.5-turbo-16k",
        "gpt-3.5-turbo-16k-0613",
    ]
    return rx.vstack(
        rx.hstack(
            rx.button("Load", on_click=State.load, color_scheme="blue"),
            rx.input(
                placeholder='Type in your utterance or click "Load" to load an existing one',
                value=State.current_utterance,
                on_change=State.set_current_utterance,
            ),
            rx.button(
                "Parse",
                on_click=State.parse,
                is_loading=State.loading,
                color_scheme="green",
            ),
            rx.button("Clear", on_click=State.clear, color_scheme="gray"),
        ),
        rx.text('You only need to hit "Parse" for new utterances', font_size="1.1em"),
        rx.spacer(),
        # rx.hstack(
        #     rx.text("speaker: "),
        #     rx.input(placeholder="evan", default_value="evan", on_change=State.set_current_speaker),
        #     rx.text("listener: "),
        #     rx.input(placeholder="self", default_value="self",on_change=State.set_current_listener),
        # ),
        rx.hstack(
            rx.text("LLM: "),
            rx.select(
                models,
                value="gpt-3.5-turbo-16k-0613",
                placeholder="Select an LLM model",
                on_change=State.set_current_model,
            ),
        ),
        rx.divider(),
        rx.cond(State.show_edit, edit_area()),
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
            rx.tab_panel(
                rx.text(
                    State.current_trade_parse,
                    font_size="1.2em",
                    font_family="Courier New",
                )
            ),
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
            rx.vstack(
                rx.badge("Is this parse correct?", color_scheme="green"),
                rx.radio_group(
                    ["yes", "no"],
                    on_change=State.set_correct_str,
                    value=State.correct_str,
                ),
                    rx.input(placeholder="Your name", 
                             on_change=State.set_username),
                rx.box(
                    rx.cond(
                        State.is_wrong,
                        rx.vstack(
                            rx.text(
                                "Please provide a corrected parse along with your name"
                            ),
                            rx.editable(
                                rx.editable_preview(),
                                rx.editable_input(),
                                placeholder=State.current_trade_parse,
                                default_value=State.current_trade_parse,
                                on_change=State.set_current_trade_parse,
                                start_with_edit_view=True,
                                width="100%",
                            ),
                        ),
                    ),
                    width="100%",
                ),
                rx.button("Save", on_click=State.save),
                rx.cond(State.saved, rx.span("saved", color="green"))
            ),
        # header=rx.heading("🖋️ Verify the Parse", size="md"),
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
# app.compile()
