import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

from apps.tasks.datauploader.parse_facebook_files import parse_facebook_files, loading_state_fb
from apps.tasks.datauploader.parse_google_files import parse_google_files, loading_state_gg

from app import app

# ---------- Dash App layout
layout = html.Div(
    # Data uploader UI components
    className="main-div",
    children=[
        # Title of the page
        html.Div(
            className="main-title",
            children=[html.H2("Discover what the internet knows about you")],
        ),
        # Introductory text of the page
        html.Div(
            className="main-text",
            children=[
                dcc.Markdown(
                    """
                    When you retrieve your personal data from the apps you use, you receive dozens of files with raw data stored in **different formats** (csv, JSON, HTML, etc.).
                    If you are not technical, it is difficult to get the big picture on who you are on the internet and make decisions about what personal data you would like to delete or modify. 
                    
                    That is why we have created a Webapp that allows you to **visualise your digital identity** in a simple way from all the data you have downloaded.
                    
                    This dashboard should help you **make decisions** to better manage your online privacy and personalise your advertising interests with a few clicks. 
                """
                ),
            ],
        ),
        # Row with the boxes detailing the 3 steps to be ready using the webapp
        html.Div(
            className="steps-boxes",
            children=[
                html.Div(
                    # Box dedicated to downloading data
                    className="float-box-step-1",
                    children=[
                        html.H4("Step 1 - Download your personal data"),
                        html.P("Follow our tutorials to get your data."),
                        dbc.CardDeck(
                            [
                                # Facebook Card
                                dbc.Card(
                                    [
                                        dbc.CardImg(
                                            src=app.get_asset_url("facebook-logo.png"),
                                            top=True,
                                        ),
                                        html.Br(),
                                        html.P("Reception ~ 5 minutes"),
                                        dbc.CardBody(
                                            [
                                                # html.Br(),
                                                dbc.Button(
                                                    "Download",
                                                    color="success",
                                                    href="https://avastar.notion.site/How-to-get-your-Data-f35b51c5690d4f1889c87e0fd0b970d8",
                                                    external_link=True,
                                                    target="_blank",
                                                    style={
                                                        "text-transform": "uppercase",
                                                        "letter-spacing": "1px",
                                                        "line-height": "30px",
                                                    },
                                                    className="box-button",
                                                ),
                                            ]
                                        ),
                                    ],
                                    style={
                                        "max-width": "18rem",
                                        "background-color": "#F5F4FA",
                                        "borderRadius": "10px",
                                        "margin": "0 auto",
                                    },
                                ),
                                # Google Card
                                dbc.Card(
                                    [
                                        dbc.CardImg(
                                            src=app.get_asset_url("google-logo.png"),
                                            top=True,
                                        ),
                                        html.Br(),
                                        html.P("Reception ~ 3 minutes"),
                                        dbc.CardBody(
                                            [
                                                # html.Br(),
                                                dbc.Button(
                                                    "Download",
                                                    color="success",
                                                    href="https://avastar.notion.site/How-to-get-your-Data-f35b51c5690d4f1889c87e0fd0b970d8",
                                                    target="_blank",
                                                    external_link=True,
                                                    style={
                                                        "text-transform": "uppercase",
                                                        "letter-spacing": "1px",
                                                        "line-height": "30px",
                                                    },
                                                    className="box-button",
                                                ),
                                            ]
                                        ),
                                    ],
                                    style={
                                        "max-width": "18rem",
                                        "background-color": "#F5F4FA",
                                        "borderRadius": "10px",
                                        "margin": "0 auto",
                                    },
                                ),
                            ],
                            style={"margin": "0 auto"},
                        ),
                    ],
                ),
                # Box dedicated to uploading data
                html.Div(
                    className="float-box-step-2",
                    children=[
                        html.H4("Step 2 - Upload your files"),
                        html.P("It may take a few seconds to upload your data."),
                        # Facebook Data Uploader
                        dcc.Upload(
                            id="upload-data-facebook",
                            children=html.Div([html.A(id="click_fb", children="Select your Facebook ZIP file")]),
                            style={
                                "lineHeight": "25px",
                                "borderWidth": "1px",
                                "borderStyle": "dashed",
                                "borderRadius": "5px",
                                "padding-top": "10px",
                                "padding-bottom": "10px",
                                "textAlign": "center",
                                "margin": "0 auto",
                                "width": "80%",
                                "fontFamily": "Lato",
                                "align-items": "center",
                            },
                            # Allow multiple files to be uploaded
                            multiple=True,
                            max_size=150000000,
                        ),
                        html.Br(),
                        # Google data uploader
                        dcc.Upload(
                            id="upload-data-google",
                            children=html.Div([html.A(id="click_gg", children="Select your Google ZIP file")]),
                            style={
                                "lineHeight": "25px",
                                "borderWidth": "1px",
                                "borderStyle": "dashed",
                                "borderRadius": "5px",
                                "padding-top": "10px",
                                "padding-bottom": "10px",
                                "textAlign": "center",
                                "margin": "0 auto",
                                "width": "80%",
                                "fontFamily": "Lato",
                            },
                            # Allow multiple files to be uploaded
                            multiple=True,
                            max_size=150000000,
                        ),
                        html.Br(),
                        dcc.Loading(id="loading-output-facebook"),
                        dcc.Loading(id="loading-output-google"),
                    ],
                ),
                # Box dedicated to access the Dashboard
                html.Div(
                    className="float-box-step-3",
                    children=[
                        html.H4("Step 3 - Take action"),
                        html.P(
                            "Take back control of your privacy and your identity on the internet.",
                            className="card-text",
                        ),
                        html.Br(),
                        dbc.Button(
                            "Access the dashboard",
                            color="success",
                            href="/mon-activite",
                            external_link=False,
                            style={
                                "text-transform": "uppercase",
                                "letter-spacing": "1px",
                                "line-height": "30px",
                            },
                            className="box-button",
                        ),
                    ],
                ),
            ],
        ),
        html.Br(),
        # Alert box to display link towards solution page
        dbc.Alert(
            [
                html.H4("You have encountered a problem to upload your personal data files?"),
                html.Div(
                    [
                        "We certainly have a solution for you! Go to ",
                        html.A(
                            "this link",
                            href="https://avastar.notion.site/Webapp-Help-Center-09c5e3892814493da33a8bde112bc775",
                            target="_blank",
                            style={"color": "#004085", "text-decoration": "none"},
                            className="alert-link",
                        ),
                        " to get more details on how it can be solved.",
                    ]
                ),
            ],
            className="alert-heading",
        ),
        # Feedback box
        html.Div(
            className="feedback-box",
            children=[
                dbc.Jumbotron(
                    [
                        html.H4(" Who are we?"),
                        dcc.Markdown(
                            """
                        The project has been developed by [Tangi Gouez](https://www.linkedin.com/in/tangi-gouez/) and [Nicolas Pfeffer](https://www.linkedin.com/in/nicolas-pfeffer/). We are both Data Analysts in Tech companies in Paris 
                        and passionate about solving complex problems through data analysis. We decided to co-found this project to develop the tools and educational 
                        content we wish we had had when we first started online.
                        
                        **Reach out to us if you think you can help us make this open-source project more scalable and secure.** 
                        """
                        ),
                        html.Br(),
                        dbc.Button(
                            "Get in touch",
                            href="https://avastar.notion.site/avastar/Avastar-Open-Source-Project-730dbef6c24040d69b4f3a17960979ae",
                            style={
                                "text-transform": "uppercase",
                                "letter-spacing": "1px",
                                "line-height": "30px",
                            },
                            target="_blank",
                            color="success",
                            className="box-button",
                        ),
                    ]
                ),
            ],
        ),
        html.Br(),
        # Disclaimer
        html.Div(
            className="disclaimer-text",
            children=[
                dcc.Markdown(
                    """
                    **Disclaimer** 
                    
                    It is important to know that the files you upload to the webapp are passing through a server. The webapp is deployed on Heroku and relies on a system whose file storage is ephemeral.
                    Indeed, on Heroku the dynos automatically restart every 24 hours. The memory is rebooted every 24h which cause all the files uploaded to the webapp to be deleted. Because we had limited resources to build this project, we do not 
                    pretend to guarantee an infrastructure that ensures an absolutely secure environment for our users.
                    We therefore decline all responsibility for any problem in the sharing of your data on our webapp.
                """
                ),
            ],
        ),
        html.Br(),
        # Footer
        html.Footer(
            className="footer",
            children=[
                html.A(
                    "Our vision",
                    href="https://avastar.notion.site/Our-Mission-a52207c78d2e405c95da934ee19a6a5a",
                    target="_blank",
                ),
                html.A(
                    "You want to contribute ?",
                    href="https://avastar.notion.site/Technical-Challenges-0d8dcc660a1e436a9109b3e588c997d2",
                    target="_blank",
                    style={"margin-left": "100px"},
                ),
                html.A(
                    "Open source code",
                    href="https://github.com/tangigouez/Webapp-Personal-Data",
                    target="_blank",
                    style={"margin-left": "100px"},
                ),
            ],
        ),
    ],
)

# ---------- Callbacks
parse_facebook_files()
loading_state_fb()
parse_google_files()
loading_state_gg()
