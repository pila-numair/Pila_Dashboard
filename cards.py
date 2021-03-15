import dash_bootstrap_components as dbc
import dash_html_components as html
def card_maker(head,body,look):
    card = dbc.Card(
        [
            dbc.CardHeader(head),
            dbc.CardBody(
                [
                    html.H3(body, className="card-text"),
                ]
            ),
        ],
        style={"width": "10rem", "height": "10rem",},
        color=look,
        inverse=True,
    )
    return card