import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import dash_table
from dash.dependencies import Input, Output, State
import pandas as pd
import numpy as np
import calendar

# def create_date_table2(start='2000-01-01', end='2050-12-31'):


# list for storing month dates
b = []
c = calendar.TextCalendar(calendar.MONDAY)
for i in c.itermonthdays(2021, 4):
    b.append(i)


# list for storing month dates


def divide_chunks(l, n):  # function to store date list into dataframe compatable list
    # looping till length l
    for i in range(0, len(l), n):
        yield l[i:i + n]


x = list(divide_chunks(b, 7))
df = pd.DataFrame(x, columns=['Monday', "Tuesday", "Wednesday", "Thursday", "Friday", "Saturdaty",
                              "Sunday"])  # month calendar
df[df.eq(0)] = ''




app = dash.Dash(__name__)

colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}

card_calendar = dbc.Card(
    [
        dbc.CardBody([
            dash_table.DataTable(
                id='data_table',
                columns=[{"name": i, "id": i} for i in df.columns],
                data=df.to_dict('records')
            )
        ]),
    ], color="warning",
)

calendar_layout = html.Div([
    html.H3("Calendar Dashboard", style={'textAlign': 'center'}),
    dbc.Row([dbc.Col(card_calendar, width=5),

             html.Div([

                 html.Br(),
                 html.Label(['Choose Month'], style={'font-weight': 'bold', "text-align": "center"}),
                 dcc.Dropdown(id='cuisine_one',
                              options=[{'label': x, 'value': x} for x in ['January', 'February', 'March']],
                              value='January',
                              multi=False,
                              disabled=False,
                              clearable=True,
                              searchable=True,
                              placeholder='Choose Month.',
                              className='form-dropdown',
                              style={'width': "90%"},
                              persistence='string',
                              persistence_type='memory'),

                 dcc.Dropdown(id='cuisine_two',
                              options=[{'label': x, 'value': x} for x in [2021, 2022, 2023, 2024]],
                              value='2021',
                              multi=False,
                              clearable=False,
                              persistence='string',
                              persistence_type='session'),

             ], className='three columns'),

             dbc.Col(html.Div(id='output_div'), width=3),

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
