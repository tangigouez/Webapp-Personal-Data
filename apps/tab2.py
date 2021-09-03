import dash_html_components as html
import dash_core_components as dcc
import dash_extensions as de

from apps.tasks.tab2.callback.update_filter import (
    update_interest_table,
    update_interactions_chart,
    update_advertisers_chart,
    update_interests_chart,
    update_behaviour_data_pct,
    update_behaviour_data_qtity,
    update_left_panel_info,
    display_username_tab_2,
)

from app import app

# ---------- Dash App layout
url = "https://assets2.lottiefiles.com/packages/lf20_n5icqxkw.json"
options = dict(
    loop=True,
    autoplay=True,
    rendererSettings=dict(preserveAspectRatio="xMidYMid slice"),
)

layout = html.Div(
    # Main Div
    className="main-div",
    children=[
        html.Div(
            # Left Panel Div
            className="div-left-panel",
            children=[
                html.Div(
                    # Div for Left Panel App Info (bio ; datatable ; button)
                    className="div-bio",
                    children=[
                        html.Br(),
                        # User profile picture
                        html.Div(de.Lottie(options=options, width="50%", height="50%", url=url)),
                        # html.Img(
                        #     className="identity_photo",
                        #     src=app.get_asset_url("id_photo.png"),
                        # ),
                        html.H6(className="title-header", id="username-tab-2"),
                        html.Br(),
                    ],
                ),
                html.Table(
                    className="table-profile",
                    children=[
                        html.Img(className="icon", src=app.get_asset_url("device.png")),
                        html.H6("Device(s) used"),
                        html.Tr(
                            className="row1",
                            children=[html.Td(children=[html.P(className="td-info", id="devices")])],
                        ),
                        html.Img(className="icon", src=app.get_asset_url("browser.png")),
                        html.H6("Browser(s) used"),
                        html.Tr(
                            className="row2",
                            children=[
                                html.Td(
                                    children=[
                                        html.P(
                                            className="td-info",
                                        )
                                    ]
                                )
                            ],
                        ),
                        html.Img(className="icon", src=app.get_asset_url("os.png")),
                        html.H6("Operating system(s) used"),
                        html.Tr(
                            className="row3",
                            children=[html.Td(children=[html.P(className="td-info", id="os")])],
                        ),
                        html.Img(className="icon", src=app.get_asset_url("languages.png")),
                        html.H6("Preferred language(s)"),
                        html.Tr(
                            className="row4",
                            children=[
                                html.Td(
                                    children=[
                                        html.P(
                                            className="td-info",
                                        )
                                    ]
                                )
                            ],
                        ),
                        html.Img(
                            className="icon",
                            src=app.get_asset_url("facial-recognition.png"),
                        ),
                        html.H6("Inferred life stage"),
                        html.Tr(
                            className="row5",
                            children=[
                                html.Td(
                                    children=[
                                        html.P(
                                            className="td-info",
                                            id="life_stage",
                                        )
                                    ]
                                )
                            ],
                        ),
                    ],
                ),
            ],
        ),
        html.Div(
            # Right panel Div
            className="div-right-panel",
            children=[
                html.Div(
                    # Div for filters
                    className="div-filters",
                    children=[
                        html.Div(
                            className="float-filter",
                            children=[
                                # Date filter
                                dcc.RangeSlider(
                                    id="slct_year",
                                    min=2005,
                                    max=2021,
                                    step=None,
                                    value=[
                                        2005,
                                        2021,
                                    ],
                                    marks={
                                        2005: {"label": "2005"},
                                        2007: {"label": "2007"},
                                        2009: {"label": "2009"},
                                        2011: {"label": "2011"},
                                        2013: {"label": "2013"},
                                        2015: {"label": "2015"},
                                        2017: {"label": "2017"},
                                        2019: {"label": "2019"},
                                        2021: {"label": "2021"},
                                    },
                                )
                            ],
                        ),
                        html.Div(
                            className="float-filter",
                            children=[
                                # Platform filter
                                dcc.Dropdown(
                                    id="slct_platform",
                                    options=[
                                        {"label": "Facebook", "value": "facebook"},
                                        {"label": "Google", "value": "google"},
                                    ],
                                    placeholder="Sélectionne la plateforme",
                                    multi=True,
                                    value=["facebook", "google"],
                                    style={"width": "100%"},
                                )
                            ],
                        ),
                    ],
                ),
                html.Br(),
                html.H6(className="title-pie-chart", children="My behavioural data"),
                # Pie Chart
                html.Br(),
                dcc.Tabs(
                    parent_className="custom-tabs",
                    className="custom-tabs-container",
                    children=[
                        dcc.Tab(
                            className="custom-tab",
                            selected_className="custom-tab--selected",
                            label="Quantity of behavioural data recorded",
                            children=[html.Br(), dcc.Graph(id="my_behaviour_qtity")],
                        ),
                        dcc.Tab(
                            className="custom-tab",
                            selected_className="custom-tab--selected",
                            label="Categories of behavioural data (%)",
                            children=[html.Br(), dcc.Graph(id="my_behaviour_pct")],
                        ),
                    ],
                ),
                html.H6(
                    className="title-pie-chart",
                    children="My advertising interests",
                ),
                html.Div(
                    # Div for KPI
                    className="div-kpis",
                    children=[
                        html.Div(
                            # Div for KPI row 1
                            className="div-kpis-row-1",
                            children=[
                                html.Div(
                                    [
                                        html.H6(id="ads_interactions_text"),
                                        html.P("Interactions with ads"),
                                        html.Img(src=app.get_asset_url("avastar_footprint_logo.png")),
                                    ],
                                    className="mini_container",
                                ),
                                html.Div(
                                    [
                                        html.H6(id="num_advertisers_text"),
                                        html.P("Advertisers hold information about me"),
                                        html.Img(src=app.get_asset_url("avastar_footprint_logo.png")),
                                    ],
                                    className="mini_container",
                                ),
                                html.Div(
                                    [
                                        html.H6(id="num_ads_interests"),
                                        html.P("Ads interests"),
                                        html.Img(src=app.get_asset_url("avastar_footprint_logo.png")),
                                    ],
                                    className="mini_container",
                                ),
                            ],
                        ),
                    ],
                ),
                html.Div(
                    # Div for DataTable
                    className="div-datatable",
                    id="table",
                ),
            ],
        ),
    ],
)


# ---------- Callback

update_interest_table()
update_interactions_chart()
update_advertisers_chart()
update_interests_chart()
update_behaviour_data_pct()
update_behaviour_data_qtity()
update_left_panel_info()
display_username_tab_2()
