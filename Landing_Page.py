import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import dash_table
from dash.dependencies import Input, Output, State
import pandas as pd
import calendar
import cards as crd
import plotly.express as px
import plotly.graph_objs as go
import kanban_List as kb
app = dash.Dash()

navbar = dbc.NavbarSimple(
    children=[
        dbc.Button("Sidebar", outline=True, color="white", className="mr-1", id="btn_sidebar"),
        dbc.DropdownMenu(
            children=[
                dbc.DropdownMenuItem("More pages", header=True),
                dbc.DropdownMenuItem("Page 2", href="#"),
                dbc.DropdownMenuItem("Page 3", href="#"),
                dbc.DropdownMenuItem("Page 4", href="#"),
            ],
            nav=True,
            in_navbar=True,
            label="More",
        ),
    ],
    brand="Pila",
    brand_href="#",
    color="dark",
    dark=True,
    fluid=True,
)

# list for storing month dates
b = []
c = calendar.TextCalendar(calendar.MONDAY)
for i in c.itermonthdays(2021, 4):
    b.append(i)


def task_card(index_i):
    return dbc.Card(
        dbc.CardBody([
            html.H5(df['to_do_task'][index_i], className='card-title'),
            html.P(df['task_dates'][index_i]),
            dbc.Button("See More", id="click-task")
        ])
    )

def kanban_task_card(index_i, _value, _status,dfy):
    return dbc.Card(
        dbc.CardBody([
            html.H5(dfy['to_do_task'].iloc[index_i], className='card-title'),
        ])
    )



df = pd.read_excel('tasks1.xlsx')


def kanban_list(_value, _status):  # _value is(urgent,imp,normal) and _status is (to do,progress,done)
    _v=_value
    _s=_status
    dfx=pd.read_excel('tasks1.xlsx')
    dfx = dfx[dfx['_status'] == _status]
    dfx = dfx[dfx['_value'] == _value]
    print(len(dfx['to_do_task']))
    return dbc.ListGroup([
        html.Div(children=[
            kanban_task_card(i, _v, _s,dfx) for i in range(len(dfx['to_do_task']))
        ])
    ])





def employee_card(i_index):
    df2 = pd.read_excel("Employee_Book.xlsx")
    return dbc.Card([

        dbc.CardBody(children=[
            dbc.CardImg(src=app.get_asset_url(df2['img_loc'][i_index]), style={'display': 'block',
                                                                       'margin-left':'auto',
                                                                       'margin-right':'auto',
                                                                      'width': '100px',
                                                                      'height': '100px'}, top=True),
            html.H5(df2['employee_name'][i_index], className="card-text", style={"text-align": "center"}),
            html.Br(),
            html.P(df2['e_designation'][i_index], style={"text-align": "center"}),
            dbc.Button("View More"),
        ]

        ),
    ])


df3 = pd.read_excel("Employee_Book.xlsx")

employee_card_list = dbc.CardColumns(children=[
        employee_card(i) for i in range(len(df3['employee_name']))
    ])



card_list= dbc.ListGroup([
    dbc.ListGroupItem(children=[
        task_card(i) for i in range(len(df['to_do_task']))
    ])
])





# list for storing month dates


def divide_chunks(l, n):  # function to store date list into dataframe compatable list
    # looping till length l
    for i in range(0, len(l), n):
        yield l[i:i + n]


x = list(divide_chunks(b, 7))
df = pd.DataFrame(x, columns=['Monday', "Tuesday", "Wednesday", "Thursday", "Friday", "Saturdaty",
                              "Sunday"])  # month calendar
df[df.eq(0)] = ''

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

# the style arguments for the sidebar. We use position:fixed and a fixed width
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 62.5,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "height": "100%",
    "z-index": 1,
    "overflow-x": "hidden",
    "transition": "all 0.5s",
    "padding": "0.5rem 1rem",
    "background-color": "#f8f9fa",
}

SIDEBAR_HIDEN = {
    "position": "fixed",
    "top": 62.5,
    "left": "-16rem",
    "bottom": 0,
    "width": "16rem",
    "height": "100%",
    "z-index": 1,
    "overflow-x": "hidden",
    "transition": "all 0.5s",
    "padding": "0rem 0rem",
    "background-color": "#f8f9fa",
}

# the styles for the main content position it to the right of the sidebar and
# add some padding.
CONTENT_STYLE = {
    "transition": "margin-left .5s",
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}

CONTENT_STYLE1 = {
    "transition": "margin-left .5s",
    "margin-left": "2rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}

sidebar = html.Div(
    [
        html.H5("Task Manager", className="display-5"),
        html.Hr(),
        html.P(
            "View your tasks accordingly", className="lead"
        ),
        dbc.Nav(
            [
                dbc.NavLink("Landing Page", href="/page-1", id="page-1-link"),
                dbc.NavLink("Kanban Board", href="/page-2", id="page-2-link"),
                dbc.NavLink("Page 3", href="/page-3", id="page-3-link"),
                dbc.NavLink("Employees", href="/page-4", id="page-4-link"),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    id="sidebar",
    style=SIDEBAR_STYLE,
)

content = html.Div(

    id="page-content",
    style=CONTENT_STYLE)

app.layout = html.Div(
    [
        dcc.Store(id='side_click'),
        dcc.Location(id="url"),
        navbar,
        sidebar,
        content,
    ],
)


@app.callback(
    [
        Output("sidebar", "style"),
        Output("page-content", "style"),
        Output("side_click", "data"),
    ],

    [Input("btn_sidebar", "n_clicks")],
    [
        State("side_click", "data"),
    ]
)
def toggle_sidebar(n, nclick):
    if n:
        if nclick == "SHOW":
            sidebar_style = SIDEBAR_HIDEN
            content_style = CONTENT_STYLE1
            cur_nclick = "HIDDEN"
        else:
            sidebar_style = SIDEBAR_STYLE
            content_style = CONTENT_STYLE
            cur_nclick = "SHOW"
    else:
        sidebar_style = SIDEBAR_STYLE
        content_style = CONTENT_STYLE
        cur_nclick = 'SHOW'

    return sidebar_style, content_style, cur_nclick


# this callback uses the current pathname to set the active state of the
# corresponding nav link to true, allowing users to tell see page they are on
@app.callback(
    [Output(f"page-{i}-link", "active") for i in range(1, 5)],
    [Input("url", "pathname")],
)
def toggle_active_links(pathname):
    if pathname == "/":
        # Treat page 1 as the homepage / index
        return True, False, False
    return [pathname == f"/page-{i}" for i in range(1, 5)]


@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def render_page_content(pathname):
    if pathname in ["/", "/page-1"]:

        colors = {
            'background': '#111111',
            'text': '#7FDBFF'
        }

        return html.Div([
            html.H1("Numair's Tasks", style={'textAlign': 'center'}),
            dbc.Row([
                dbc.Col([
                    html.H5("Task List"),
                    html.Div(card_list, style={'height': '750px', 'overflow': 'scroll'}),
                ],
                        width=3),
                dbc.Col([html.H5("Task Details"),
                         dbc.ListGroup([
                             dbc.ListGroupItem(html.H3("Your Task Name"),style={'textAlign': 'left'}),
                             dbc.ListGroupItem(html.H5("25-March-2021"),style={'textAlign': 'left'}),
                             dbc.ListGroupItem(html.P("Here Are the details of the selected task of employee.More details can be displayed here"),style={'textAlign': 'left'}),
                         ])
                         ],style={'textAlign': 'left'}, align="start",width=8),


                     #dbc.Col(html.Div(id='output_div'), width=3),      this line for uderstanding callback I/O


                     ], no_gutters=True),

        ])

    elif pathname == "/page-2":
        return html.Div([
            dbc.Row(children=[
                dbc.Col(html.H3('Kanban Board',style={"color":"red"})),
                dbc.Col(html.H3('To Do')),
                dbc.Col(html.H3('In Progress')),
                dbc.Col(html.H3('Done')),

            ]),
            dbc.Row(children=[
                dbc.Col(html.H3("Urgent")),
                dbc.Col(kanban_list("urgent", "to do")),
                # these 2 arguments has to be column name from tasks1.xlsx table
                dbc.Col(kanban_list("urgent", "in progress")),
                # these 2 arguments has to be column name from tasks1.xlsx table
                dbc.Col(kanban_list("urgent", "done"))  # these 2 arguments has to be column name from tasks1.xlsx table
            ],style={"color":"blue"}),
            dbc.Row(children=[
                dbc.Col(html.H3("Important")),
                dbc.Col(kanban_list("important", "to do")),
                # these 2 arguments has to be column name from tasks1.xlsx table
                dbc.Col(kanban_list("important", "in progress")),
                # these 2 arguments has to be column name from tasks1.xlsx table
                dbc.Col(kanban_list("important", "done"))
                # these 2 arguments has to be column name from tasks1.xlsx table
            ],style={"color":"green"}),
            dbc.Row(children=[
                dbc.Col(html.H3("Normal")),
                dbc.Col(kanban_list("normal", "in progress")),
                # these 2 arguments has to be column name from tasks1.xlsx table
                dbc.Col(kanban_list("normal", "to do")),
                # these 2 arguments has to be column name from tasks1.xlsx table
                dbc.Col(kanban_list("normal", "done"))  # these 2 arguments has to be column name from tasks1.xlsx table
            ],style={"color":"orange"}),
        ],style={"border-style":"solid","border":"1px solid black"})
    elif pathname == "/page-3":
        df = pd.DataFrame([
            dict(Task="Make List", Start='2021-01-01', Finish='2021-02-28', Completion_pct=100),
            dict(Task="Buy Products", Start='2021-03-05', Finish='2021-04-15', Completion_pct=55),
            dict(Task="Sell Products", Start='2021-02-20', Finish='2021-05-30', Completion_pct=25)
        ])

        fig = px.timeline(df, x_start="Start", x_end="Finish", y="Task", color="Completion_pct")
        fig.update_yaxes(autorange="reversed")

        df = pd.read_csv("progress_dates.csv")
        df['dates']= pd.to_datetime(df['dates'])
        fig2 = px.line(df, x='dates', y='percent', color='progress')
        fig3 = go.Figure(go.Indicator(
            mode="gauge+number",
            value=70,
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': " Completion Progress"}))
        return html.Div([html.H3('Ghatt chart'),dcc.Graph(figure=fig),html.H3('work flow'),
                        dbc.Row([
                            dbc.Col(dcc.Graph(id='example-graph-2',figure=fig2)),
                            dbc.Col(dcc.Graph(id='example-graph-3',figure=fig3))
                        ])
                        ,])
    elif pathname == "/page-4":
        return html.Div([html.H1("Employees", style={'text-align': 'center'}),
                         employee_card_list], style={'height': '750px', 'overflow': 'scroll'})
    # If the user tries to reach a different page, return a 404 message
    return dbc.Jumbotron(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ]
    )


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


if __name__ == "__main__":
    app.run_server()
