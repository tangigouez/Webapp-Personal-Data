import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc

from app import app
from apps import tab1, tab2, datauploader
from utils import GA

server = app.server
app.index_string = GA

# Create Navigation Bar appearing at the top of the Tabs
navbar = dbc.Navbar(
    [
        html.A(
            # Use row and col to control vertical and horizontal alignment of Avastar logo
            dbc.Row(
                [
                    dbc.Col(
                        html.Img(
                            src="/assets/logo-avastar-grey-background.png",
                            height="45px",
                        ),
                        width={"offset": 5},
                    ),
                ],
                align="center",
                no_gutters=True,
            ),
            href="/accueil",
        ),
        dbc.Nav(
            # right align navigation items on the menu with ml-auto className
            [
                dbc.NavItem(
                    dbc.NavLink(
                        "Accueil",
                        href="/accueil",
                        style={
                            "background-color": "#0D67FE",
                            "color": "#fff",
                            "padding": "7px",
                            "border-radius": "5px",
                        },
                    ),
                    style={"margin-right": "10px"},
                ),
                dbc.NavItem(
                    dbc.NavLink(
                        "Mon activité",
                        href="/mon-activite",
                        style={
                            "background-color": "#0D67FE",
                            "color": "#fff",
                            "padding": "7px",
                            "border-radius": "5px",
                        },
                    ),
                    style={"margin-right": "10px"},
                ),
                dbc.NavItem(
                    dbc.NavLink(
                        "Mon comportement",
                        href="/mon-comportement",
                        style={
                            "background-color": "#0D67FE",
                            "color": "#fff",
                            "padding": "7px",
                            "border-radius": "5px",
                        },
                    ),
                    style={"margin-right": "50px"},
                ),
            ],
            className="ml-auto",
            navbar=True,
            pills=True,
            fill=True,
            style={"font-family": "Lato", "color": "white"},
        ),
    ],
    color="#ECEBF4",
    light=True,
)

# embedding the navigation bar
app.layout = html.Div(
    [
        dcc.Location(id="url", refresh=False),
        navbar,
        html.Div(id="page-content"),
        dcc.Store(id="fb-gen-info-1", storage_type="session"),
        dcc.Store(id="fb-gen-info-2", storage_type="session"),
        dcc.Store(id="fb-kpi-layer-1", storage_type="session"),
        dcc.Store(id="fb-kpi-layer-2", storage_type="session"),
        dcc.Store(id="fb-ads-interests", storage_type="session"),
        dcc.Store(id="fb-behavioural-data", storage_type="session"),
        dcc.Store(id="gg-gen-info", storage_type="session"),
        dcc.Store(id="gg-behavioural-data", storage_type="session"),
    ]
)


# Callback to change Tab based on the item selected in the DropDown Menu
@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def display_page(pathname):
    if pathname == "/mon-activite":
        return tab1.layout
    elif pathname == "/mon-comportement":
        return tab2.layout
    elif pathname == "/accueil":
        return datauploader.layout
    else:
        return datauploader.layout


if __name__ == "__main__":
    app.run_server(debug=True, port=8051)
