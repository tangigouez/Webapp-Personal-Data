from app import app
from dash.dependencies import Input, Output, State

import plotly.graph_objects as go
import pandas as pd
import dash_table
import json


def update_interest_table():
    """
    Connect slct_platform filter to ads areas of interest DataTable
        Parameters:
            fb-ads-interests (df) : dataframe with information for the facebook ads areas of interest
        Return:
            children (table) : the datatable to plot
    """

    @app.callback(
        Output("table", "children"),
        [Input("slct_platform", "value")],
        [State("fb-ads-interests", "data")],
    )
    def callback(slct_platform, data_fb):
        # accumulate filtered platform dfs in a list
        small_dfs = []
        # check if facebook data exists
        if data_fb is not None:
            df_fb = pd.read_json(data_fb, orient="split")
            small_dfs.append(df_fb)
        if small_dfs:
            # Concatenate all platform dfs in a single one
            large_df = pd.concat(small_dfs, ignore_index=True)
            platform = []

            if isinstance(slct_platform, list) is False:
                platform.append(slct_platform)
            else:
                platform = slct_platform

            dff = large_df[large_df.platform.isin(platform)]

            # Rename columns to get more explicit names on the webapp
            dff.columns = ["Platform", "Advertising interests"]
            # Change the order of columns to keep ads interest names on the left side
            dff = dff.reindex(columns=["Advertising interests", "Platform"])

        else:
            no_data = ["Aucune donnée"]

            dff = pd.DataFrame(
                {
                    "Advertising interests": no_data,
                    "Platform": no_data,
                }
            )
        children = dash_table.DataTable(
            data=dff.to_dict("rows"),
            columns=[{"id": c, "name": c} for c in dff.columns],
            style_cell_conditional=[{"if": {"column_id": c}, "textAlign": "left"} for c in dff.columns],
            style_as_list_view=True,
            page_size=10,
            style_header={"fontWeight": "bold"},
            style_cell={
                "backgroundColor": "rgba(0,0,0,0)",
                "color": "#404040",
                "font-family": "Lato",
            },
        )
        return children


def update_interactions_chart():
    """
    Connect slct_platform filter to interactions within the chart
        Parameters:
            fb-kpi-layer-2 (df) : dataframe with facebook information for the ads interactions
        Return:
            dff["count"].sum() (int) : the KPI to plot
    """

    @app.callback(
        Output("ads_interactions_text", "children"),
        [Input("slct_platform", "value")],
        [State("fb-kpi-layer-2", "data")],
    )
    def callback(slct_platform, data_fb):
        # accumulate filtered dfs in this list
        small_dfs = []
        # check if facebook data exist
        if data_fb is not None:
            df_fb = pd.read_json(data_fb, orient="split")
            dff_fb = df_fb[df_fb["info"] == "ads_interactions"]
            small_dfs.append(dff_fb)
        if small_dfs:
            # Concatenate all platform dfs in a single one
            large_df = pd.concat(small_dfs, ignore_index=True)
            platform = []

            if isinstance(slct_platform, list) is False:
                platform.append(slct_platform)
            else:
                platform = slct_platform

            dff = large_df[large_df.platform.isin(platform)]
            ads_interactions = dff["count"].sum()
        else:
            ads_interactions = 0
        return ads_interactions


def update_advertisers_chart():
    """
    Connect slct_platform filter to advertisers within the chart
        Parameters:
            fb-kpi-layer-2 (df) : dataframe with facebook information for the advertisers
        Return:
            dff["count"].sum() (int) : the KPI to plot
    """

    @app.callback(
        Output("num_advertisers_text", "children"),
        [Input("slct_platform", "value")],
        [State("fb-kpi-layer-2", "data")],
    )
    def callback(slct_platform, data_fb):
        # accumulate filtered dfs in this list
        small_dfs = []
        # check if facebook data exist
        if data_fb is not None:
            df_fb = pd.read_json(data_fb, orient="split")
            dff_fb = df_fb[df_fb["info"] == "advertisers"]
            small_dfs.append(dff_fb)
        if small_dfs:
            # Concatenate all platform dfs in a single one
            large_df = pd.concat(small_dfs, ignore_index=True)
            platform = []

            if isinstance(slct_platform, list) is False:
                platform.append(slct_platform)
            else:
                platform = slct_platform

            dff = large_df[large_df.platform.isin(platform)]
            advertisers = dff["count"].sum()
        else:
            advertisers = 0
        return advertisers


def update_interests_chart():
    """
    Connect slct_platform filter to areas of interests within the chart
        Parameters:
            fb-ads-interests (df) : dataframe with information for the facebook ads areas of interest
        Return:
            len(dff) (int) : the KPI to plot
    """

    @app.callback(
        Output("num_ads_interests", "children"),
        [Input("slct_platform", "value")],
        [State("fb-ads-interests", "data")],
    )
    def callback(slct_platform, data_fb):
        # accumulate filtered dfs in this list
        small_dfs = []
        # check if facebook data exist
        if data_fb is not None:
            df_fb = pd.read_json(data_fb, orient="split")
            small_dfs.append(df_fb)
        if small_dfs:
            # Concatenate all platform dfs in a single one
            large_df = pd.concat(small_dfs, ignore_index=True)
            platform = []

            if isinstance(slct_platform, list) is False:
                platform.append(slct_platform)
            else:
                platform = slct_platform

            dff = large_df[large_df.platform.isin(platform)]
            ads_interests = len(dff)
        else:
            ads_interests = 0
        return ads_interests


def update_behaviour_data_pct():
    """
    Create behavioural chart
        Parameters:
            fb-behavioural-data (df) : dataframe with information about the user behaviour
        Return:
            fig (int) : Bar chart
    """

    @app.callback(
        Output("my_behaviour_pct", "figure"),
        [Input("slct_year", "value"), Input("slct_platform", "value")],
        [State("fb-behavioural-data", "data"), State("gg-behavioural-data", "data")],
    )
    def callback(slct_year, slct_platform, data_fb, data_gg):
        # accumulate filtered dfs in this list
        small_dfs = []

        # format filters
        year = slct_year
        platform = []

        start = slct_year[0]
        end = slct_year[1]
        year = [*range(start, end + 1)]

        if isinstance(slct_platform, list) is False:
            platform.append(slct_platform)
        else:
            platform = slct_platform

        # check if facebook data exists
        if data_fb is not None:
            df_fb = pd.read_json(data_fb, orient="split")
            dff_fb = df_fb[(df_fb.year.isin(year)) & (df_fb.platform.isin(platform))]
            small_dfs.append(dff_fb)
        # check if google data exists
        if data_gg is not None:
            df_gg = pd.read_json(data_gg, orient="split")
            dff_gg = df_gg[(df_gg.year.isin(year)) & (df_gg.platform.isin(platform))]
            small_dfs.append(dff_gg)
        if small_dfs:
            # store the names of platforms selected for the chart x axis
            platforms = slct_platform
            # Concatenate all platform dfs in a single one
            large_df = pd.concat(small_dfs, ignore_index=True)

            dff = large_df[large_df["year"].isin(year)]
            dff = dff.drop("year", 1)

            # get aggregates by platform and source
            data = dff.groupby(["platform", "source"]).sum().reset_index()
            # build list of values per category of data (one list = count of values for this category for each platform)
            localisation = []
            for element in platforms:
                if element in list(data[data["source"] == "localisation"]["platform"]):
                    localisation.append(
                        data[(data["source"] == "localisation") & (data["platform"] == element)]["count"].iloc[0]
                    )
                else:
                    localisation.append(0)

            connexion = []
            for element in platforms:
                if element in list(data[data["source"] == "connexion"]["platform"]):
                    connexion.append(
                        data[(data["source"] == "connexion") & (data["platform"] == element)]["count"].iloc[0]
                    )
                else:
                    connexion.append(0)

            historique = []
            for element in platforms:
                if element in list(data[data["source"] == "historique"]["platform"]):
                    historique.append(
                        data[(data["source"] == "historique") & (data["platform"] == element)]["count"].iloc[0]
                    )
                else:
                    historique.append(0)

            produit = []
            for element in platforms:
                if element in list(data[data["source"] == "produit"]["platform"]):
                    produit.append(data[(data["source"] == "produit") & (data["platform"] == element)]["count"].iloc[0])
                else:
                    produit.append(0)

            transaction = []
            for element in platforms:
                if element in list(data[data["source"] == "transaction"]["platform"]):
                    transaction.append(
                        data[(data["source"] == "transaction") & (data["platform"] == element)]["count"].iloc[0]
                    )
                else:
                    transaction.append(0)

            # build list of list with all categories
            listoflist = []
            listoflist.append(localisation)
            listoflist.append(connexion)
            listoflist.append(historique)
            listoflist.append(produit)
            listoflist.append(transaction)

            # sum all elements as vectors to get total of values per platform
            sumindex = [sum(elts) for elts in zip(*listoflist)]

            # get % of total for each category
            pct_localisation = [(i / j) if j != 0 else 0 for i, j in zip(localisation, sumindex)]
            pct_connexion = [(i / j) if j != 0 else 0 for i, j in zip(connexion, sumindex)]
            pct_historique = [(i / j) if j != 0 else 0 for i, j in zip(historique, sumindex)]
            pct_produit = [(i / j) if j != 0 else 0 for i, j in zip(produit, sumindex)]
            pct_transaction = [(i / j) if j != 0 else 0 for i, j in zip(transaction, sumindex)]

            # build chart
            x = platforms
            fig = go.Figure(
                go.Bar(
                    x=x,
                    y=pct_connexion,
                    name="login history",
                    text=connexion,
                    hovertemplate="%{y} of recorded data by %{x} about you is "
                    "about your login history with a total of %{text} logins",
                    width=0.2,
                )
            )
            fig.add_trace(
                go.Bar(
                    x=x,
                    y=pct_historique,
                    name="search history",
                    text=historique,
                    hovertemplate="%{y} of recorded data by %{x} about you is "
                    "about your search history with a total of %{text} searches",
                    width=0.2,
                )
            )
            fig.add_trace(
                go.Bar(
                    x=x,
                    y=pct_localisation,
                    name="localisation",
                    text=localisation,
                    hovertemplate="%{y} of recorded data by %{x} about you is "
                    "localisation data with a total of %{text} GPS coordinates",
                    width=0.2,
                )
            )
            fig.add_trace(
                go.Bar(
                    x=x,
                    y=pct_produit,
                    name="product",
                    text=produit,
                    hovertemplate="%{y} of recorded data by %{x} about you is "
                    "product usage data with a total of %{text} actions recorded",
                    width=0.2,
                )
            )
            fig.add_trace(
                go.Bar(
                    x=x,
                    y=pct_transaction,
                    name="transaction",
                    text=transaction,
                    hovertemplate="%{y} of recorded data by %{x} about you is "
                    "transaction data with a total of %{text} payments",
                    width=0.2,
                )
            )

            fig.update_layout(
                barmode="stack",
                xaxis={"categoryorder": "total descending"},
                yaxis_tickformat="%",
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                margin=dict(t=0),
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            )
            fig.update_traces(texttemplate="%{y}", textposition="inside")

            return fig


def update_behaviour_data_qtity():
    """
    Create behavioural chart
        Parameters:
            fb-behavioural-data (df) : dataframe with information about the user behaviour
        Return:
            fig (int) : Bar chart
    """

    @app.callback(
        Output("my_behaviour_qtity", "figure"),
        [Input("slct_year", "value"), Input("slct_platform", "value")],
        [State("fb-behavioural-data", "data"), State("gg-behavioural-data", "data")],
    )
    def callback(slct_year, slct_platform, data_fb, data_gg):
        # accumulate filtered dfs in this list
        small_dfs = []

        # format filters
        year = slct_year
        platform = []

        start = slct_year[0]
        end = slct_year[1]
        year = [*range(start, end + 1)]

        if isinstance(slct_platform, list) is False:
            platform.append(slct_platform)
        else:
            platform = slct_platform

        # check if facebook data exists
        if data_fb is not None:
            df_fb = pd.read_json(data_fb, orient="split")
            dff_fb = df_fb[(df_fb.year.isin(year)) & (df_fb.platform.isin(platform))]
            small_dfs.append(dff_fb)
        # check if google data exists
        if data_gg is not None:
            df_gg = pd.read_json(data_gg, orient="split")
            dff_gg = df_gg[(df_gg.year.isin(year)) & (df_gg.platform.isin(platform))]
            small_dfs.append(dff_gg)
        if small_dfs:
            # Concatenate all platform dfs in a single one
            large_df = pd.concat(small_dfs, ignore_index=True)

            data = large_df.groupby(["platform"])["count"].sum().reset_index()
            fig = go.Figure(
                go.Bar(
                    x=list(data["platform"]),
                    y=list(data["count"]),
                    width=0.2,
                    marker={"color": ("#636EFA", "#00CC96")},
                ),
            )
            fig.update_layout(
                xaxis={"categoryorder": "total descending"},
                margin=dict(t=0),
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
            )
            fig.update_traces(
                texttemplate="%{y:.2s}",
                textposition="outside",
                hovertemplate="%{x} has recorded a total of %{y:.2s} data about "
                "your behaviour and actions ON and OFF the platform",
            )

            return fig


def update_left_panel_info():
    """
    Connect slct_platform filter to the footprint pie chart
        Parameters:
            fb-gen-info-2 (JSON) : dictionary with relevant facebook general information for tab2 left panel
        Return:
            os (str) :
            devices (datetime) :
            life_stage (str) :
    """

    @app.callback(
        [
            Output("os", "children"),
            Output("devices", "children"),
            Output("life_stage", "children"),
        ],
        [Input("slct_platform", "value")],
        [State("fb-gen-info-2", "data")],
    )
    def callback(slct_platform, data_fb):
        platform = []
        category = []
        information = []
        # check if facebook data exists
        if data_fb is not None:
            data_fb = json.loads(data_fb)
            if data_fb["devices"] is not None:
                platform.append("facebook")
                category.append("devices")
                information.append(data_fb["devices"])
            if data_fb["operating_system"] is not None:
                platform.append("facebook")
                category.append("operating_system")
                information.append(data_fb["operating_system"])
            if data_fb["life_stage"] is not None:
                platform.append("facebook")
                category.append("life_stage")
                information.append(data_fb["life_stage"])
        if information:
            # if there is data available, aggregate the lists in a single df
            df = pd.DataFrame({"platform": platform, "category": category, "information": information})
            dff = df[df.platform.isin(slct_platform)]
            if "operating_system" in list(dff.category):
                df_os = dff[dff["category"] == "operating_system"]
                os = ", ".join([str(elem) for elem in df_os["information"]])
            else:
                os = ""
            if "devices" in list(dff.category):
                df_devices = dff[dff["category"] == "devices"]
                devices = ", ".join([str(elem) for elem in df_devices["information"]])
            else:
                devices = ""
            if "life_stage" in list(dff.category):
                df_life_stage = dff[dff["category"] == "life_stage"]
                life_stage = ", ".join([str(elem) for elem in df_life_stage["information"]])
            else:
                life_stage = ""
        else:
            os = ""
            devices = ""
            life_stage = ""

        return os, devices, life_stage


def display_username_tab_2():
    """
    Select the most relevant username to display on tab2 left panel
        Parameters:
            fb-gen-info-1 (JSON) : dictionary with relevant facebook information for the left panel
            gg-gen-info (JSON) : dictionary with relevant google information for the left panel
        Return:
            username (value) : the first name and last name to display
    """

    @app.callback(
        Output("username-tab-2", "children"),
        [Input("fb-gen-info-1", "data"), Input("gg-gen-info", "data")],
        [State("fb-gen-info-1", "data"), State("gg-gen-info", "data")],
    )
    def callback(fb_ts, gg_ts, data_fb, data_gg):
        pseudos = []
        if data_fb is not None:
            data_fb = json.loads(data_fb)
            if data_fb["pseudo"] is not None:
                pseudos.append(data_fb["pseudo"])
        if data_gg is not None:
            data_gg = json.loads(data_gg)
            if data_gg["pseudo"] is not None:
                pseudos.append(data_gg["pseudo"])
        if len(pseudos) == 2:
            name_display = pseudos[1]
        elif len(pseudos) == 1:
            name_display = pseudos[0]
        else:
            name_display = "Anonymous"
        return name_display
