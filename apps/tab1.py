import dash_core_components as dcc
import dash_html_components as html
import dash_extensions as de

from apps.tasks.tab1.callback.update_filter import (
    update_likes_and_reactions_text,
    update_comments_text,
    update_footprint_text,
    update_posts_text,
    update_photos_text,
    update_areas_of_interest_text,
    generate_chart_footprint,
    update_left_panel_info,
    display_username_tab_1,
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
                        html.H6(className="title-header", id="username-tab-1"),
                        html.Br(),
                    ],
                ),
                html.Table(
                    className="table-profile",
                    children=[
                        html.Img(className="icon", src=app.get_asset_url("identity.png")),
                        html.H6("Pseudo"),
                        html.Tr(
                            className="row1",
                            children=[
                                html.Td(
                                    children=[
                                        html.P(
                                            className="td-info",
                                            id="pseudo",
                                        )
                                    ]
                                )
                            ],
                        ),
                        html.Img(className="icon", src=app.get_asset_url("www.png")),
                        html.H6("Internet birth date"),
                        html.Tr(
                            className="row2",
                            children=[
                                html.Td(
                                    children=[
                                        html.P(
                                            className="td-info",
                                            id="internet_birth_date",
                                        )
                                    ]
                                )
                            ],
                        ),
                        html.Img(className="icon", src=app.get_asset_url("ip.png")),
                        html.H6("Last IP address registered"),
                        html.Tr(
                            className="row3",
                            children=[
                                html.Td(
                                    children=[
                                        html.P(
                                            className="td-info",
                                            id="last_ip_address",
                                        )
                                    ]
                                )
                            ],
                        ),
                        html.Img(className="icon", src=app.get_asset_url("fingerprint.png")),
                        html.H6("Digital footprint size (MB)"),
                        html.Tr(
                            className="row4",
                            children=[
                                html.Td(
                                    children=[
                                        html.P(
                                            className="td-info",
                                            id="footprint",
                                        )
                                    ]
                                )
                            ],
                        ),
                        html.Img(className="icon", src=app.get_asset_url("email.png")),
                        html.H6("E-mail adresse(s)"),
                        html.Tr(
                            className="row5",
                            children=[
                                html.Td(
                                    children=[
                                        html.P(
                                            className="td-info",
                                            id="email",
                                        )
                                    ]
                                )
                            ],
                        ),
                        html.Img(className="icon", src=app.get_asset_url("phone.png")),
                        html.H6("Phone number(s)"),
                        html.Tr(
                            className="row6",
                            children=[
                                html.Td(
                                    children=[
                                        html.P(
                                            className="td-info",
                                            id="tel",
                                        )
                                    ]
                                )
                            ],
                        ),
                        html.Img(className="icon", src=app.get_asset_url("address.png")),
                        html.H6("Adresse(s)"),
                        html.Tr(
                            className="row7",
                            children=[
                                html.Td(
                                    children=[
                                        html.P(
                                            className="td-info",
                                            id="physical_address",
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
                                    # Load the app without any platform filter pre set
                                    value=["facebook", "google"],
                                    style={"width": "100%"},
                                )
                            ],
                        ),
                    ],
                ),
                html.Div(
                    # Div for kpi boxes
                    className="div-kpis",
                    children=[
                        html.Br(),
                        html.H6(className="title-kpi-chart", children="My activity"),
                        html.Div(
                            # Div for KPI row 1
                            className="div-kpis-row-1",
                            children=[
                                html.Div(
                                    [
                                        html.H6(id="likes_and_reactions_text"),
                                        html.P("Likes and reactions"),
                                        html.Img(src=app.get_asset_url("avastar_footprint_logo.png")),
                                    ],
                                    className="mini_container",
                                ),
                                html.Div(
                                    [
                                        html.H6(id="comments_text"),
                                        html.P("Comments"),
                                        html.Img(src=app.get_asset_url("avastar_footprint_logo.png")),
                                    ],
                                    id="comments",
                                    className="mini_container",
                                ),
                                html.Div(
                                    [
                                        html.H6(id="footprint_text"),
                                        html.P("MB of data"),
                                        html.Img(src=app.get_asset_url("avastar_footprint_logo.png")),
                                    ],
                                    className="mini_container",
                                ),
                            ],
                        ),
                        html.Br(),
                        html.Div(
                            # Div for KPI row 2
                            className="div-kpis-row-2",
                            children=[
                                html.Div(
                                    [
                                        html.H6(id="posts_text"),
                                        html.P("Posts"),
                                        html.Img(src=app.get_asset_url("avastar_footprint_logo.png")),
                                    ],
                                    id="posts",
                                    className="mini_container",
                                ),
                                html.Div(
                                    [
                                        html.H6(id="photos_text"),
                                        html.P("Photos and videos"),
                                        html.Img(src=app.get_asset_url("avastar_footprint_logo.png")),
                                    ],
                                    id="photos",
                                    className="mini_container",
                                ),
                                html.Div(
                                    [
                                        html.H6(id="areas_of_interest_text"),
                                        html.P("Followed pages"),
                                        html.Img(src=app.get_asset_url("avastar_footprint_logo.png")),
                                    ],
                                    id="areasOfInterest",
                                    className="mini_container",
                                ),
                            ],
                        ),
                    ],
                ),
                html.Br(),
                html.H6(className="title-pie-chart", children="My digital footprint"),
                html.Br(),
                # Pie Chart
                dcc.Graph(id="my_footprint"),
                html.Div(id="output-data-upload"),
            ],
        ),
    ],
)


# ---------- Callback
update_likes_and_reactions_text()
update_comments_text()
update_footprint_text()
update_posts_text()
update_photos_text()
update_areas_of_interest_text()
generate_chart_footprint()
update_left_panel_info()
display_username_tab_1()
