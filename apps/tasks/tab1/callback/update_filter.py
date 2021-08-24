from app import app
from dash.dependencies import Input, Output, State

import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
import json


def update_likes_and_reactions_text():
    """
    Connect slct_platform and slct_year filters to likes and reactions KPI
        Parameters:
            fb-kpi-layer-1 (df) : dataframe containing relevant facebook information for the likes_and_reactions KPI
        Return:
            dff["count"].sum() (int) : the KPI to plot
    """

    @app.callback(
        Output("likes_and_reactions_text", "children"),
        [Input("slct_year", "value"), Input("slct_platform", "value")],
        [State("fb-kpi-layer-1", "data")],
    )
    def callback(slct_year, slct_platform, data_fb):
        # accumulate filtered platform dfs in a list
        small_dfs = []
        # check if facebook data exist
        if data_fb is not None:
            df_fb = pd.read_json(data_fb, orient="split")
            dff_fb = df_fb[df_fb["info"] == "likes and reactions"]
            small_dfs.append(dff_fb)
        if small_dfs:
            # Concatenate all platform dfs in a single one
            large_df = pd.concat(small_dfs, ignore_index=True)

            year = slct_year
            platform = []

            start = slct_year[0]
            end = slct_year[1]
            year = [*range(start, end + 1)]

            if isinstance(slct_platform, list) is False:
                platform.append(slct_platform)
            else:
                platform = slct_platform

            dff = large_df[(large_df.year.isin(year)) & (large_df.platform.isin(platform))]
            likes_and_reactions = dff["count"].sum()
        else:
            likes_and_reactions = 0
        return likes_and_reactions


def update_comments_text():
    """
    Connect slct_platform and slct_year filters to comments KPI
        Parameters:
            fb-kpi-layer-1 (df) : dataframe containing relevant facebook information for the comments KPI
        Return:
            dff["count"].sum() (int) : the KPI to plot
    """

    @app.callback(
        Output("comments_text", "children"),
        [Input("slct_year", "value"), Input("slct_platform", "value")],
        [State("fb-kpi-layer-1", "data")],
    )
    def callback(slct_year, slct_platform, data_fb):
        # accumulate filtered platform dfs in a list
        small_dfs = []
        # check if facebook data exist
        if data_fb is not None:
            df_fb = pd.read_json(data_fb, orient="split")
            dff_fb = df_fb[df_fb["info"] == "comments"]
            small_dfs.append(dff_fb)
        if small_dfs:
            # Concatenate all platform dfs in a single one
            large_df = pd.concat(small_dfs, ignore_index=True)

            year = slct_year
            platform = []

            start = slct_year[0]
            end = slct_year[1]
            year = [*range(start, end + 1)]

            if isinstance(slct_platform, list) is False:
                platform.append(slct_platform)
            else:
                platform = slct_platform

            dff = large_df[(large_df.year.isin(year)) & (large_df.platform.isin(platform))]
            comments = dff["count"].sum()
        else:
            comments = 0
        return comments


def update_footprint_text():
    """
    Connect slct_platform and slct_year filters to footprint KPI
        Parameters:
            fb-gen-info-1 (JSON) : dictionary with relevant facebook information for the footprint KPI
        Return:
            round(dff["size_mb"].sum(), 2) (float) : the KPI to plot
    """

    @app.callback(
        Output("footprint_text", "children"),
        [Input("slct_platform", "value")],
        [State("fb-gen-info-1", "data"), State("gg-gen-info", "data")],
    )
    def callback(slct_platform, data_fb, data_gg):
        # append footprint data to the lists below for the platforms with uploaded data
        platform_footprint = []
        count = []
        # check if facebook data exist
        if data_fb is not None:
            data_fb = json.loads(data_fb)
            if data_fb["size_footprint"] is not None:
                platform_footprint.append("facebook")
                count.append(data_fb["size_footprint"])
        # check if google data exist
        if data_gg is not None:
            data_gg = json.loads(data_gg)
            if data_gg["size_footprint"] is not None:
                platform_footprint.append("google")
                count.append(data_gg["size_footprint"])
        # list for slct_platform filter
        platform = []
        # if footprint data is available, build a filterable df to output relevant information
        if count:
            df_footprint = pd.DataFrame({"platform": platform_footprint, "size_mb": count})
            if isinstance(slct_platform, list) is False:
                platform.append(slct_platform)
            else:
                platform = slct_platform
            dff = df_footprint[(df_footprint.platform.isin(platform))]
            footprint = round(dff["size_mb"].sum(), 2)
        else:
            footprint = 0

        return footprint


def update_posts_text():
    """
    Connect slct_platform and slct_year filters to posts KPI
        Parameters:
            fb-kpi-layer-1 (df) : dataframe containing relevant facebook information for the posts KPI
        Return:
            dff["count"].sum() (int) : the KPI to plot
    """

    @app.callback(
        Output("posts_text", "children"),
        [Input("slct_year", "value"), Input("slct_platform", "value")],
        [State("fb-kpi-layer-1", "data")],
    )
    def callback(slct_year, slct_platform, data_fb):
        # accumulate filtered platform dfs in a list
        small_dfs = []
        # check if facebook data exist
        if data_fb is not None:
            df_fb = pd.read_json(data_fb, orient="split")
            dff_fb = df_fb[df_fb["info"] == "posts"]
            small_dfs.append(dff_fb)
        if small_dfs:
            # Concatenate all platform dfs in a single one
            large_df = pd.concat(small_dfs, ignore_index=True)

            year = slct_year
            platform = []

            start = slct_year[0]
            end = slct_year[1]
            year = [*range(start, end + 1)]

            if isinstance(slct_platform, list) is False:
                platform.append(slct_platform)
            else:
                platform = slct_platform

            dff = large_df[(large_df.year.isin(year)) & (large_df.platform.isin(platform))]
            posts = dff["count"].sum()
        else:
            posts = 0
        return posts


def update_photos_text():
    """
    Connect slct_platform and slct_year filters to photos KPI
        Parameters:
            fb-kpi-layer-1 (df) : dataframe containing relevant facebook information for the photos KPI
        Return:
            dff["count"].sum() (int) : the KPI to plot
    """

    @app.callback(
        Output("photos_text", "children"),
        [Input("slct_year", "value"), Input("slct_platform", "value")],
        [State("fb-kpi-layer-1", "data")],
    )
    def callback(slct_year, slct_platform, data_fb):
        # accumulate filtered platform dfs in a list
        small_dfs = []
        # check if facebook data exist
        if data_fb is not None:
            df_fb = pd.read_json(data_fb, orient="split")
            dff_fb = df_fb[df_fb["info"] == "photos"]
            small_dfs.append(dff_fb)
        if small_dfs:
            # Concatenate all platform dfs in a single one
            large_df = pd.concat(small_dfs, ignore_index=True)

            year = slct_year
            platform = []

            start = slct_year[0]
            end = slct_year[1]
            year = [*range(start, end + 1)]

            if isinstance(slct_platform, list) is False:
                platform.append(slct_platform)
            else:
                platform = slct_platform

            dff = large_df[(large_df.year.isin(year)) & (large_df.platform.isin(platform))]
            photos = dff["count"].sum()
        else:
            photos = 0
        return photos


def update_areas_of_interest_text():
    """
    Connect slct_platform and slct_year filters to the areas of interest KPI
        Parameters:
            fb-gen-info-1 (JSON) : dictionary with relevant facebook information for the areas of interest KPI
        Return:
            num_areas_of_interest (int) : the KPI to plot
    """

    @app.callback(
        Output("areas_of_interest_text", "children"),
        [Input("slct_platform", "value")],
        [State("fb-gen-info-1", "data")],
    )
    def callback(slct_platform, data_fb):
        # check if facebook data exist
        if data_fb is not None:
            data_fb = json.loads(data_fb)
            # KPI relevant only for facebook platform
            if data_fb["areas_of_interest"] is not None and "facebook" in slct_platform:
                num_areas_of_interest = data_fb["areas_of_interest"]
            else:
                num_areas_of_interest = 0
        else:
            num_areas_of_interest = 0

        return num_areas_of_interest


def generate_chart_footprint():
    """
    Connect slct_platform filter to the footprint pie chart
        Parameters:
            fb-gen-info-1 (JSON) : dictionary with relevant facebook information for the footprint pie chart
        Return:
            fig (chart) : the pie chart to plot
    """

    @app.callback(
        Output("my_footprint", "figure"),
        [Input("slct_platform", "value")],
        [State("fb-gen-info-1", "data"), State("gg-gen-info", "data")],
    )
    def callback(slct_platform, data_fb, data_gg):
        # append footprint data to the lists below for the platforms with uploaded data
        platform_footprint = []
        count = []
        # check if facebook data exist
        if data_fb is not None:
            data_fb = json.loads(data_fb)
            if data_fb["size_footprint"] is not None:
                platform_footprint.append("facebook")
                count.append(data_fb["size_footprint"])

        # check if google data exist
        if data_gg is not None:
            data_gg = json.loads(data_gg)
            if data_gg["size_footprint"] is not None:
                platform_footprint.append("google")
                count.append(data_gg["size_footprint"])

        dff = pd.DataFrame({"platform": platform_footprint, "size_mb": count})
        dff = dff.sort_values("platform")
        labels = list(dff[dff.platform.isin(slct_platform)]["platform"])
        values = list(dff[dff.platform.isin(slct_platform)]["size_mb"])

        # Use `hole` to create a donut-like pie chart
        fig = go.Figure(
            data=[
                go.Pie(
                    labels=labels,
                    values=values,
                    hole=0.4,
                    marker=dict(
                        colors=["#636EFA", "#00CC96"],
                    ),
                )
            ]
        )
        fig.update_layout(
            annotations=[
                dict(
                    text=str(round(dff[dff.platform.isin(slct_platform)]["size_mb"].sum(), 2)) + " MB",
                    x=0.50,
                    y=0.5,
                    font_size=20,
                    showarrow=False,
                )
            ],
            paper_bgcolor="rgba(0,0,0,0)",
            margin=dict(t=0),
            legend=dict(orientation="v", yanchor="top", y=1.0, xanchor="center", x=1),
        )
        return fig


def update_left_panel_info():
    """
    Connect slct_platform filter to the left panel infos
        Parameters:
            fb-gen-info-1 (JSON) : dictionary with relevant facebook general information for tab1 and tab2 left panels
        Return:
            pseudo (str) : name(s) used on the different platforms
            internet_birth_date (datetime) : oldest platform account creation date
            last_ip_address (str) : ip address associated to the most recent date
            email (str) : email address shared by the used on the internet
            tel (str) : phone number shared by the used on the internet
            physical_address (str) : physical address shared by the used on the internet
            footprint (int) : size (MB) of the files uploaded by the user
    """

    @app.callback(
        [
            Output("pseudo", "children"),
            Output("internet_birth_date", "children"),
            Output("last_ip_address", "children"),
            Output("email", "children"),
            Output("tel", "children"),
            Output("physical_address", "children"),
            Output("footprint", "children"),
        ],
        [Input("slct_platform", "value")],
        [State("fb-gen-info-1", "data"), State("gg-gen-info", "data")],
    )
    def callback(slct_platform, data_fb, data_gg):
        platform = []
        category = []
        information = []
        date = []
        if data_fb is not None:
            data_fb = json.loads(data_fb)
            if data_fb["pseudo"] is not None:
                platform.append("facebook")
                category.append("pseudo")
                information.append(data_fb["pseudo"])
                date.append("")
            if data_fb["account_creation_date"] is not None:
                platform.append("facebook")
                category.append("internet_birth_date")
                information.append("")
                date.append(data_fb["account_creation_date"])
            if data_fb["last_ip_address"] is not None:
                platform.append("facebook")
                category.append("last_ip_address")
                information.append(data_fb["last_ip_address"])
                date.append(data_fb["last_ip_timestamp"])
            if data_fb["size_footprint"] is not None:
                platform.append("facebook")
                category.append("footprint")
                information.append(data_fb["size_footprint"])
                date.append("")
            if data_fb["e-mail"] is not None:
                platform.append("facebook")
                category.append("email")
                information.append(data_fb["e-mail"])
                date.append("")
            if data_fb["tel"] is not None:
                platform.append("facebook")
                category.append("tel")
                information.append(data_fb["tel"])
                date.append("")
        if data_gg is not None:
            data_gg = json.loads(data_gg)
            if data_gg["pseudo"] is not None:
                platform.append("google")
                category.append("pseudo")
                information.append(data_gg["pseudo"])
                date.append("")
            if data_gg["e-mail"] is not None:
                platform.append("google")
                category.append("email")
                information.append(data_gg["e-mail"])
                date.append("")
            if data_gg["size_footprint"] is not None:
                platform.append("google")
                category.append("footprint")
                information.append(data_gg["size_footprint"])
                date.append("")
            if data_gg["phone_number"] is not None:
                platform.append("google")
                category.append("tel")
                information.append(data_gg["phone_number"])
                date.append("")
            if data_gg["physical_address"] is not None:
                platform.append("google")
                category.append("physical_address")
                information.append(data_gg["physical_address"])
                date.append("")
        if information:
            df = pd.DataFrame(
                {
                    "platform": platform,
                    "category": category,
                    "information": information,
                    "date": date,
                }
            )
            dff = df[df.platform.isin(slct_platform)]
            if "pseudo" in list(dff.category):
                df_pseudo = dff[dff["category"] == "pseudo"]
                pseudo = ", ".join([str(elem) for elem in df_pseudo["information"]])
                # if there are multiple pseudos, check if they are similar, if so keep only one
                data_split = pseudo.split(",")
                if len(data_split) > 1:
                    data_compare = pseudo.lower()
                    data_compare_split = data_compare.split(", ")
                    pseudo = list(set(data_compare_split))
                    pseudo = ", ".join([str(elem) for elem in pseudo])
                else:
                    pseudo = pseudo.lower()
            else:
                pseudo = ""
            if "email" in list(dff.category):
                df_email = dff[dff["category"] == "email"]
                email = ", ".join([str(elem) for elem in df_email["information"]])
                # if there are multiple e-mails, check if they are similar, if so keep only one
                data_split = email.lower().replace(" ", "").split(",")
                if len(data_split) > 1:
                    email = list(set(data_split))
                    email = ", ".join([str(elem) for elem in email])
            else:
                email = ""
            if "tel" in list(dff.category):
                df_tel = dff[dff["category"] == "tel"]
                tel = ", ".join([str(elem) for elem in df_tel["information"]])
                if tel == "[]":
                    tel = ""
                # if there are multiple phone numbers, check if they are similar, if so keep only one
                data_split = tel.split(",")
                if len(data_split) > 1:
                    data_compare = tel.replace("+33", "0").replace(" ", "").replace("(", "").replace(")", "")
                    data_compare_split = data_compare.split(",")
                    tel = list(set(data_compare_split))
                    tel = ", ".join([str(elem) for elem in tel])
                else:
                    tel = tel.replace("+33", "0").replace(" ", "").replace("(", "").replace(")", "")
            else:
                tel = ""
            if "physical_address" in list(dff.category):
                df_physical_address = dff[dff["category"] == "physical_address"]
                physical_address = ", ".join([str(elem) for elem in df_physical_address["information"]])
            else:
                physical_address = ""
            if "internet_birth_date" in list(dff.category):
                df_internet_birth_date = dff[dff["category"] == "internet_birth_date"]
                internet_birth_date = datetime.strftime(
                    datetime.utcfromtimestamp(min(df_internet_birth_date["date"])),
                    "%Y-%m-%d",
                )
            else:
                internet_birth_date = ""
            if "last_ip_address" in list(dff.category):
                df_ip = dff[dff["category"] == "last_ip_address"]
                min_date = max(df_ip["date"])
                last_ip_address = df_ip[df_ip["date"] == min_date]["information"].iloc[0]
            else:
                last_ip_address = ""
            if "footprint" in list(dff.category):
                df_footprint = df[df["category"] == "footprint"]
                footprint = round(df_footprint["information"].sum(), 2)
            else:
                footprint = ""
        else:
            pseudo = ""
            internet_birth_date = ""
            last_ip_address = ""
            email = ""
            tel = ""
            physical_address = ""
            footprint = ""

        return (
            pseudo,
            internet_birth_date,
            last_ip_address,
            email,
            tel,
            physical_address,
            footprint,
        )


def display_username_tab_1():
    """
    Select the most relevant username to display on tab1 left panel
        Parameters:
            fb-gen-info-1 (JSON) : dictionary with relevant facebook information for the left panel
            gg-gen-info (JSON) : dictionary with relevant google information for the left panel
        Return:
            username (value) : the first name and last name to display
    """

    @app.callback(
        Output("username-tab-1", "children"),
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
