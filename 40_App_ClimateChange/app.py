#%% Imports
from shiny import App, reactive, render, ui
from shinywidgets import output_widget, register_widget, reactive_read
from pathlib import Path
from start.plot_funs import plot_country, plot_world
from asyncio import sleep
import pandas as pd
import ipyleaflet as L
import plotnine as gg


#%% Data Prep
app_dir = Path(__file__).parent

# Load file
temps = pd.read_csv(app_dir / 'start/temperatures.csv')
#print(temp.head())

# Setup dropdown
countries = temps['Country'].unique().tolist()

# Setup slider
years = temps['Year'].unique()
year_min = years.min()
year_max = years.max()

#%% UI
# CSS
font_style = 'font-weight: 100'

app_ui = ui.page_fluid(
    ui.h2('Climate Change', style=font_style),
    ui.row(
        ui.column(6, ui.input_select(id='country',
                                     label='Choose a Country',
                                     choices=countries)),
        ui.column(6, ui.row(
            ui.column(6, ui.input_slider(id='year',
                                     label='Choose a Year',
                                     min=year_min,
                                     max=year_max,
                                     value=year_min,
                                     animate=False)),
            ui.column(6, ui.output_ui('col_map'))
            ))
    ),
    ui.row(
        ui.column(6, ui.output_plot('years_graph')),
        ui.column(6, output_widget('map'))
    ),
    ui.br(),
    ui.row(
        ui.column(6, ui.h5('Imprint', style=font_style)),
        ui.column(6, ui.p('Learn how to develop this app',
                          style=font_style))
    ),
    ui.row(
        ui.column(6,
        ui.row(
            ui.column(2, ui.img(src='developer.png', width='32px'),
                      style='text-align: center;'),
            ui.column(10, ui.p('My Name', style=font_style))
        ),
        ui.row(
            ui.column(2, ui.img(src='address2.png', width='32px'),
                      style='text-align: center;'),
            ui.column(10, ui.p('My Street', style=font_style)),
        ),
        ui.row(
            ui.column(2, ),
            ui.column(10, ui.p('My City', style=font_style))
        ),
        ui.row(
            ui.column(2, ),
            ui.column(10, ui.p('My Country', style=font_style))
        ),
        ui.row(
            ui.column(2, ui.img(src='mail2.png', width='32px'),
                      style='text-align: center;'),),
            ui.column(10, ui.a(ui.p('My Email'), href='My Email', 
                               style=font_style))
        ),
        ui.column(6, ui.a(ui.img(src='course_logo_300x169.png'),
                          href='https://www.google.com'),
                          style='text-align: center;')
    ), style='background-color: #fff'
)

#%% Server
def server(input, output, session):
    # Initialise map
    map = L.Map(center=(0, 0), zoom=1)
    # Add distance scale
    map.add_control(L.leaflet.ScaleControl(position='bottomleft'))
    # Link map with ui object
    register_widget('map', map)
    # Link year change to map change
    @reactive.Effect
    def _():
        layer = plot_world(temp=temps, year=input.year())
        map.add_layer(layer)

    # Temperature plot
    @output
    @render.plot
    async def years_graph():
        with ui.Progress(min=1, max=15) as p:
            p.set(message='Calculation in progress',
                  detail='Please wait ...')
            for i in range(1, 15):
                p.set(i, message='Computing')
                await sleep(0.1)
        g = plot_country(temp=temps,
                         country=input.country(),
                         year=input.year())
        return g
    
    # Colour map
    @output
    @render.ui
    def col_map():
        img = ui.img(src='colormap.png')
        return img

#%% App
app = App(app_ui, server, static_assets=app_dir / "start/www")
 