from shiny import App, render, ui

app_ui = ui.page_fluid(
    ui.panel_title("Artle Shiny!"),
    ui.input_numeric("g", "Guess", 0),
    ui.output_text_verbatim("txt"),
)


def server(input, output, session):
    @render.text
    def txt():
        return f"Your guess was {input.g()}"


app = App(app_ui, server)
