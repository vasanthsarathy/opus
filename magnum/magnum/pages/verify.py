"""The verify page."""
from magnum.templates import template

import reflex as rx

class FormState(rx.State):

    form_data: dict = {}

    def handle_submit(self, form_data: dict):
        "Handle the form submit."
        self.form_data = form_data


"""
logical flow 

- >> user clicks on verify
- select random utterance that  is minimally validated
- display utterance
- >> user runs OPUS on it 
- display parse 
- display checkboxes for verification and if necessary 
- >> user clicks submit button

functions to write: load form, 
"""

@template(route="/verify", title="Verify Parse")
def verify() -> rx.Component:
    """The Verify page.
    
    Returns:
        The UI for the Verify page
    """
    return rx.vstack(
    rx.form(
        rx.vstack(
            rx.input(
                placeholder="First Name",
                id="first_name",
            ),
            rx.input(
                placeholder="Last Name", id="last_name"
            ),
            rx.hstack(
                rx.checkbox("Checked", id="check"),
                rx.switch("Switched", id="switch"),
            ),
            rx.button("Submit", 
                       type_="submit", 
                       bg="#ecfdf5",
                       color="#047857",
                       border_radius="lg",
            ),
        ),
        on_submit=FormState.handle_submit,
    ),
    rx.divider(),
    rx.heading("Results"),
    rx.text(FormState.form_data.to_string()),
    width="100%",
)