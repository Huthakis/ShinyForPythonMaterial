#%% Package Imports
from shiny import App, reactive, render, ui
from pathlib import Path
import pandas as pd
import numpy as np
import plotnine as gg

#%% Data Preparation
lang = pd.read_csv(Path(__file__).parent /
'MostPopularProgrammingLanguages.csv')
lang['datetime'] = pd.to_datetime(lang['Date'])
lang.drop(axis=1, columns=['Date'], inplace=True)

lang_long = lang.melt(id_vars='datetime',
                      value_name='popularity',
                      var_name='language').reset_index(drop=True)

date_range_start = np.min(lang_long['datetime'])
date_range_end = np.max(lang_long['datetime'])

lang_names = lang_long['language'].unique()
lang_names_dict = {l:l for l in lang_names}

#%% UI Setup
app_ui = ui.page_fluid(
    ui.panel_title('Most Popular Languages'),
    ui.layout_sidebar(
        ui.sidebar(
            ui.input_selectize(id='language',
                           label='Langauges',
                           choices=lang_names_dict,
                           selected='Python',
                           multiple=True),
            ui.input_date_range(id="daterange",
                            label="Date range",
                            start=date_range_start,
                            end=date_range_end))),
        ui.output_plot('time_plot')
)


#%% Server Setup
def server(input, output, session):
    @reactive.Calc
    def lang_filt():
        selected_start = pd.to_datetime(input.daterange()[0])
        selected_end = pd.to_datetime(input.daterange()[1])
        lang_filt = lang_long.loc[(lang_long['language'].isin(list(input.language()))) & 
                                  (lang_long['datetime'] >= selected_start) &
                                  (lang_long['datetime'] <= selected_end)
                                  ].reset_index(drop=True)
        return lang_filt

    @render.plot
    def time_plot():
        g = gg.ggplot(lang_filt()) + gg.aes(x = 'datetime', y = 'popularity', color = 'language') + gg.geom_line() + gg.theme(axis_text_x=gg.element_text(rotation=90, ha='center')) + gg.labs(title='Language Popularity Over Time', color='Langauge', x='Date', y='Popularity (%)')
        return g

#%% App
app = App(app_ui, server)
