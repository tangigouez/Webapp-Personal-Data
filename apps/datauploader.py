import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

from apps.tasks.datauploader.parse_facebook_files import (parse_facebook_files, loading_state_fb)
from apps.tasks.datauploader.parse_google_files import (parse_google_files, loading_state_gg)

from app import app

# ---------- Dash App layout
layout = html.Div(
    # Data uploader UI components
    className="main-div",
    children=[
        # Title of the page
        html.Div(
            className="main-title",
            children=[html.H2("Reprends le contrôle de ton identité digitale")],
        ),
        # Introductory text of the page
        html.Div(
            className="main-text",
            children=[
                dcc.Markdown(
                    """
                La confidentialité de nos utilisateurs est au cœur de notre produit. 
                **Nous ne voulons et ne pouvons pas voir les données** que tu déposes sur notre plateforme. 
                Le traitement et le stockage des données visualisées dans ton Dashboard se font localement dans ton navigateur.
                Dès que tu quittes ton navigateur, les informations visualisées sur Avastar disparaitront.
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
                        html.H4("Etape 1 - Télécharge tes données"),
                        html.P("Suis les instructions de nos tutoriels pour récupérer tes données."),
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
                                        html.P("Réception ~ 5 minutes"),
                                        dbc.CardBody(
                                            [
                                                # html.Br(),
                                                dbc.Button(
                                                    "Télécharger",
                                                    color="success",
                                                    href="https://www.avastar.fr/faq",
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
                                        html.P("Réception ~ 3 minutes"),
                                        dbc.CardBody(
                                            [
                                                # html.Br(),
                                                dbc.Button(
                                                    "Télécharger",
                                                    color="success",
                                                    href="https://www.avastar.fr/faq",
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
                        html.H4("Etape 2 - Dépose tes fichiers"),
                        html.P("Le téléchargement de tes données peut prendre quelques secondes."),
                        # Facebook Data Uploader
                        dcc.Upload(
                            id="upload-data-facebook",
                            children=html.Div([html.A(id="click_fb", children="Sélectionne ton fichier ZIP Facebook")]),
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
                            children=html.Div([html.A(id="click_gg", children="Sélectionne ton fichier ZIP Google")]),
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
                            max_size=150000000
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
                        html.H4("Etape 3 - Passe à l'action"),
                        html.P(
                            "Reprends le contrôle de ta vie privée et de ton image sur internet.",
                            className="card-text",
                        ),
                        html.Br(),
                        dbc.Button(
                            "Accéder au dashboard",
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
                html.H4("Tu rencontres un problème ?"),
                html.Div(
                    [
                        "Nous avons très certainement une solution pour toi ! Rends toi sur ",
                        html.A(
                            "ce lien",
                            href="https://www.avastar.fr/support",
                            target="_blank",
                            style={"color": "#004085", "text-decoration": "none"},
                            className="alert-link",
                        ),
                        " pour plus de détails sur la façon dont il peut être résolu.",
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
                        html.H4(" Nous aimerions avoir ton avis !"),
                        dcc.Markdown(
                            """
                        Dis nous comment tu aimerais **actionner ta carte d’identité digitale**. 
                        Grâce à ton aide nous pourrons  prioriser les fonctionnalités qui comptent le plus pour toi.
                        """
                        ),
                        dbc.Button(
                            "Par ici !",
                            href="https://docs.google.com/forms/d/e/1FAIpQLScogm301-tQgu5ysMUGBydAc_STn6Y36nLgavqBGmMunHWZQA/viewform?usp=pp_url",
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
        # Footer
        html.Footer(
            className="footer",
            children=[
                html.A("Notre vision", href="https://www.avastar.fr/manifesto", target="_blank"),
                html.A(
                    "Nous contacter",
                    href="mailto:contact@avastar.fr",
                    target="_blank",
                    style={"margin-left": "100px"},
                ),
                html.A(
                    "Nous soutenir",
                    href="https://www.buymeacoffee.com/avastar",
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
