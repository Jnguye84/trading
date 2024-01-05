from shiny import App, ui

# Part 1: ui ----
app_ui = ui.page_fluid(
    ui.input_text(text_id, 'Ticker'),

    #outputs
    ui.output_plot('Reddit Sentiment Analysis'),


)

# Part 2: server ----
def server(input, output, session):
    @render.text_id

# Combine into a shiny app.
# Note that the variable must be "app".
app = App(app_ui, server)