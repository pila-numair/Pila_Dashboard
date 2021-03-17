import dash
import dash_html_components as html
import dash_bootstrap_components as dbc
import pandas as pd


def task_card(index_i, _value, _status):
    sub_df = df[df['_status'] == _status]
    sub_df = sub_df[sub_df['_value'] == _value]
    return dbc.Card(
        dbc.CardBody([
            html.H5(sub_df['to_do_task'][index_i], className='card-title'),
        ])
    )


def employee_card(i_index):
    df2 = pd.read_excel("Employee_Book.xlsx")
    return dbc.Card(
        dbc.CardImg(src=df2['img_loc'][i_index], top=True),
        dbc.CardBody([
            html.H5(df2['employee_name'][i_index], className="card-text", style={"text-align": "center"}),
            html.Br(),
            html.P(df2['e_designation'][i_index], style={"text-align": "center"}),
        ]

        )
    )


df = pd.read_excel('tasks1.xlsx')


def kanban_list(_value, _status):  # _value is(urgent,imp,normal) and _status is (to do,progress,done)
    return dbc.ListGroup([
        dbc.ListGroupItem(children=[
            task_card(i, _value, _status) for i in range(len(df['to_do_task']))
        ])
    ])


def board():
    return html.Div(
        dbc.Row(children=[
            dbc.Col(html.H3('Kanban Board')),
            dbc.Col(html.H3('To Do')),
            dbc.Col(html.H3('In Progress')),
            dbc.Col(html.H3('Done')),
        ]),
        dbc.Row(children=[
            dbc.Col(html.H3("Urgent")),
            dbc.Col(kanban_list("urgent", "to do")),  # these 2 arguments has to be column name from tasks1.xlsx table
            dbc.Col(kanban_list("urgent", "in progress")),
            # these 2 arguments has to be column name from tasks1.xlsx table
            dbc.Col(kanban_list("urgent", "done"))  # these 2 arguments has to be column name from tasks1.xlsx table
        ]),
        dbc.Row(children=[
            dbc.Col(html.H3("Important")),
            dbc.Col(kanban_list("important", "to do")),
            # these 2 arguments has to be column name from tasks1.xlsx table
            dbc.Col(kanban_list("important", "in progress")),
            # these 2 arguments has to be column name from tasks1.xlsx table
            dbc.Col(kanban_list("important", "done"))  # these 2 arguments has to be column name from tasks1.xlsx table
        ]),
        dbc.Row(children=[
            dbc.Col(html.H3("Normal")),
            dbc.Col(kanban_list("normal", "in progress")),
            # these 2 arguments has to be column name from tasks1.xlsx table
            dbc.Col(kanban_list("normal", "to do")),  # these 2 arguments has to be column name from tasks1.xlsx table
            dbc.Col(kanban_list("normal", "done"))  # these 2 arguments has to be column name from tasks1.xlsx table
        ]),
    )
