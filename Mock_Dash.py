import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import cards as crd
import dash_table
from dash.dependencies import Input, Output, State






app = dash.Dash(__name__)

colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}


app.layout = html.Div(style={'backgroundColor': colors['background']}, children=[
            html.H3("Calendar Dashboard", style={'textAlign': 'center'}),
            dbc.Row([dbc.Col(crd.card_maker("Total Tasks", "21", "warning"), width="auto"),
                     dbc.Col(crd.card_maker("Completed Tasks", "7", "success"), width="auto"),
                     dbc.Col(crd.card_maker("Pending/Upcomming Tasks", "14", "danger"), width="auto"),

                     ], justify="around"),

        ])

app.layout = html.Div(style={'backgroundColor': colors['background']}, children=[
    html.H3("Calendar Dashboard", style={'textAlign': 'center'}),
    dbc.Row([dbc.Col(crd.card_maker("Total Tasks", "21", "warning"), width="auto"),
             dbc.Col(crd.card_maker("Completed Tasks", "7", "success"), width="auto"),
             dbc.Col(crd.card_maker("Pending/Upcomming Tasks", "14", "danger"), width="auto"),



             ], justify="around"),

])




@app.callback(
    Output('output_div', 'children'),
    Input('data_table', 'active_cell'),
    State('data_table', 'data')
)
def getActiveCell(active_cell, data):
    if active_cell:
        col = active_cell['column_id']
        row = active_cell['row']
        cellData = data[row][col]
        return html.P(f'row: {row}, col: {col}, value: {cellData}')
    return html.P('Please Select a Date')


app.run_server()
