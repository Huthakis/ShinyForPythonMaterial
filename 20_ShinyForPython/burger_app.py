from shiny import App, render, ui

app_ui = ui.page_fluid(
    ui.panel_title("Burger Ordering System"),
    ui.input_radio_buttons("meat", "Meat Option",
                            {                            
                                "beef": "Beef",
                                "chicken": "Chicken",
                                "vegetarian": "Black Bean Patty"
                            }, selected=None),
    ui.input_checkbox_group("topping", "Topping Options",
                            {
                                "cheese": "Cheese",
                                "lettuce": "Lettuce",
                                "mayonnaise": "Mayonnaise",
                                "mustard": "Mustard",
                                "onion": "Onion"
                            }, selected=None),
    ui.output_text_verbatim("order")
)

 
def server(input, output, session):
    @render.text
    def order():
        return f"Your burger will have {input.meat()} \nwith {", ".join(input.topping())}"


app = App(app_ui, server)
