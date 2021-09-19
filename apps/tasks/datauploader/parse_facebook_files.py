import base64
from datetime import datetime
import io
import json
from zipfile import ZipFile
import pandas as pd
import time
import unicodedata


from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from app import app


def parse_facebook_files():
    """
    Parse the ZIP file uploaded in the dcc.upload component dedicated to Facebook
        Parameters:
            contents (str) :  content of the ZIP file encoded in base 64
            filename (str) : name of the ZIP file uploaded
            last_modified (ts) : timestamp at which the folder had been uploaded
        Return:
            general_info_1 (JSON) : user general attributes stored plotted in left panels of tab1
            general_info_2 (JSON) : user general attributes stored plotted in left panels of tab2
            kpi_layer_1_store (JSON) : used to plot KPIs on tab1
            kpi_layer_2_store (JSON) : used to plot KPIs on tab2
            ads_interests_store (JSON) : used to plot ads interests DataTable on tab2
            behavioural_data_store (JSON) : used to plot behavioural chart on tab2
    """

    @app.callback(
        [
            Output("fb-gen-info-1", "data"),
            Output("fb-gen-info-2", "data"),
            Output("fb-kpi-layer-1", "data"),
            Output("fb-kpi-layer-2", "data"),
            Output("fb-ads-interests", "data"),
            Output("fb-behavioural-data", "data"),
        ],
        [Input("upload-data-facebook", "contents")],
        [
            State("upload-data-facebook", "filename"),
            State("upload-data-facebook", "last_modified"),
        ],
    )
    def update_output_facebook(list_of_contents, list_of_names, list_of_dates):
        # check if a file has been uploaded, if not prevent the callback to be fired
        import os

        if list_of_dates is None:
            raise PreventUpdate
        else:
            for content, name, date in zip(list_of_contents, list_of_names, list_of_dates):
                # the content needs to be split. It contains the type and the real content
                content_type, content_string = content.split(",")
                # Decode the base64 string
                content_decoded = base64.b64decode(content_string)
                # Use BytesIO to handle the decoded content
                zip_str = io.BytesIO(content_decoded)
                ZipFile(zip_str, "r").printdir()
                # Get name of the file uploaded
                filename = name.split(".zip")[0]
                # Now you can use ZipFile to take the BytesIO output
                # ZipFile(zip_str, 'r').printdir() # To use in order to check the directory of the folder uploaded
                zf = ZipFile(zip_str, "r")
                if str(filename) != str(zf.namelist()[0].split("/")[0]):
                    filename = str(zf.namelist()[0].split("/")[0])

                # Identify files existing in the uploaded folder directory
                file_list = []
                for zinfo in zf.filelist:
                    file_list.append(zinfo.filename)

                # Get the size of the folder uploaded in MB
                filesize = float(sum([zinfo.file_size for zinfo in zf.filelist])) / 1000000

                # check if files are contained in a single folder which has the same name as the zip folder
                if str(name.split(".zip")[0]) == str(zf.namelist()[0].split("/")[0]):
                    # Create dictionary with all the possible filepath in the uploaded facebook folder directory
                    fb_directory = {
                        "profile_information": os.path.join(
                            filename, "profile_information", "profile_information.json"
                        ),
                        "account_activity": os.path.join(
                            filename, "security_and_login_information", "account_activity.json"
                        ),
                        "page_likes": os.path.join(filename, "pages", "pages_you've_liked.json"),
                        "mobile_devices": os.path.join(
                            filename, "security_and_login_information", "mobile_devices.json"
                        ),
                        "life_stage": os.path.join(filename, "other_logged_information", "friend_peer_group.json"),
                        "likes_and_reactions": os.path.join(
                            filename, "comments_and_reactions", "posts_and_comments.json"
                        ),
                        "posts": os.path.join(filename, "posts", "your_posts_1.json"),
                        "cover_photos": os.path.join(filename, "posts", "album", "0.json"),
                        "profile_photos": os.path.join(filename, "posts", "album", "1.json"),
                        "timeline_photos": os.path.join("posts", "album", "2.json"),
                        "comments": os.path.join(filename, "comments_and_reactions", "comments.json"),
                        "visited": os.path.join(filename, "your_interactions_on_facebook", "recently_visited.json"),
                        "viewed": os.path.join(filename, "your_interactions_on_facebook", "recently_viewed.json"),
                        "interactions_people": os.path.join(filename, "activity_messages", "people_and_friends.json"),
                        "interactions_events": os.path.join(filename, "activity_messages", "events_interactions.json"),
                        "logins_and_logouts": os.path.join(
                            filename, "security_and_login_information", "logins_and_logouts.json"
                        ),
                        "login_location": os.path.join(
                            filename, "security_and_login_information", "where_you're_logged_in.json"
                        ),
                        "used_ip": os.path.join(filename, "security_and_login_information", "ip_address_activity.json"),
                        "search_history": os.path.join(filename, "search", "your_search_history.json"),
                        "advertisers_interaction": os.path.join(
                            "ads_information", "advertisers_you've_interacted_with.json"
                        ),
                        "ad_contact_info": os.path.join(
                            filename,
                            "ads_information",
                            "advertisers_who_uploaded_a_contact_list_with_your_information.json",
                        ),
                        "ads_interests": os.path.join(filename, "other_logged_information", "ads_interests.json"),
                        "ads_topics": os.path.join(filename, "your_topics", "your_topics.json"),
                        "cookies": os.path.join(filename, "security_and_login_information", "browser_cookies.json"),
                    }
                else:
                    # Create dictionary with all the possible filepath in the uploaded facebook folder directory
                    fb_directory = {
                        "profile_information": os.path.join("profile_information", "profile_information.json"),
                        "account_activity": os.path.join("security_and_login_information", "account_activity.json"),
                        "page_likes": os.path.join("pages", "pages_you've_liked.json"),
                        "mobile_devices": os.path.join("security_and_login_information", "mobile_devices.json"),
                        "likes_and_reactions": os.path.join("comments_and_reactions", "posts_and_comments.json"),
                        "life_stage": os.path.join("other_logged_information", "friend_peer_group.json"),
                        "posts": os.path.join("posts", "your_posts_1.json"),
                        "cover_photos": os.path.join("posts", "album", "0.json"),
                        "profile_photos": os.path.join("posts", "album", "1.json"),
                        "timeline_photos": os.path.join("posts", "album", "2.json"),
                        "comments": os.path.join("comments_and_reactions", "comments.json"),
                        "visited": os.path.join("your_interactions_on_facebook", "recently_visited.json"),
                        "viewed": os.path.join("your_interactions_on_facebook", "recently_viewed.json"),
                        "interactions_people": os.path.join("activity_messages", "people_and_friends.json"),
                        "interactions_events": os.path.join("activity_messages", "events_interactions.json"),
                        "logins_and_logouts": os.path.join("security_and_login_information", "logins_and_logouts.json"),
                        "login_location": os.path.join("security_and_login_information", "where_you're_logged_in.json"),
                        "used_ip": os.path.join("security_and_login_information", "ip_address_activity.json"),
                        "search_history": os.path.join("search", "your_search_history.json"),
                        "advertisers_interaction": os.path.join(
                            "ads_information", "advertisers_you've_interacted_with.json"
                        ),
                        "ad_contact_info": os.path.join(
                            "ads_information",
                            "advertisers_who_uploaded_a_contact_list_with_your_information.json",
                        ),
                        "ads_interests": os.path.join("other_logged_information", "ads_interests.json"),
                        "ads_topics": os.path.join("your_topics", "your_topics.json"),
                        "cookies": os.path.join("security_and_login_information", "browser_cookies.json"),
                    }

                fb_file_used = 0
                # OUTPUT 1
                # Read the relevant files
                if (fb_directory["profile_information"]) in file_list:
                    fb_file_used = fb_file_used + 1
                    profile_information = json.load(zf.open(fb_directory["profile_information"]))
                    pseudo = profile_information["profile_v2"]["name"]["full_name"]
                    acr = profile_information["profile_v2"]["registration_timestamp"]
                    mail = profile_information["profile_v2"]["emails"]["emails"][0]
                    phone_number = profile_information["profile_v2"]["phone_numbers"]
                    if len(phone_number) > 0:
                        phone_number = profile_information["profile_v2"]["phone_numbers"][0]["phone_number"]
                    else:
                        phone_number = None
                else:
                    pseudo = None
                    acr = None
                    mail = None
                    phone_number = None

                if (fb_directory["account_activity"]) in file_list:
                    fb_file_used = fb_file_used + 1
                    login_information = json.load(zf.open(fb_directory["account_activity"]))
                    last_ip_ts = login_information["account_activity_v2"][0]["timestamp"]
                    last_ip = login_information["account_activity_v2"][0]["ip_address"]
                else:
                    last_ip = None
                    last_ip_ts = None

                if (fb_directory["page_likes"]) in file_list:
                    fb_file_used = fb_file_used + 1
                    pages = json.load(zf.open(fb_directory["page_likes"]))
                    areas_of_interest = len(pages["page_likes_v2"])
                else:
                    areas_of_interest = None

                if (fb_directory["mobile_devices"]) in file_list:
                    fb_file_used = fb_file_used + 1
                    device_information = json.load(zf.open(fb_directory["mobile_devices"]))
                    device = device_information["devices_v2"][0]["type"]
                    os = device_information["devices_v2"][0]["os"]
                else:
                    device = None
                    os = None

                if (fb_directory["life_stage"]) in file_list:
                    fb_file_used = fb_file_used + 1
                    life_stage = json.load(zf.open(fb_directory["life_stage"]))
                    life_stage_value = life_stage["friend_peer_group_v2"]
                else:
                    life_stage_value = None

                # Aggregate information in dictionaries
                general_info_1 = {
                    "pseudo": pseudo,
                    "account_creation_date": acr,
                    "last_ip_address": last_ip,
                    "last_ip_timestamp": last_ip_ts,
                    "size_footprint": filesize,
                    "e-mail": mail,
                    "tel": phone_number,
                    "areas_of_interest": areas_of_interest,
                }

                general_info_2 = {
                    "devices": device,
                    "operating_system": os,
                    "life_stage": life_stage_value,
                }

                # convert dict to JSON
                general_info_1_store = json.dumps(general_info_1, indent=4)
                general_info_2_store = json.dumps(general_info_2, indent=4)

                # OUTPUT 2
                # Initialize lists to store data
                platform_kpi_1 = []
                info_kpi_1 = []
                year_kpi_1 = []
                count_kpi_1 = []
                # Read the relevant files
                # Likes and reactions
                if (fb_directory["likes_and_reactions"]) in file_list:
                    fb_file_used = fb_file_used + 1
                    likes_and_reactions_r = json.load(zf.open(fb_directory["likes_and_reactions"]))
                    for element in likes_and_reactions_r["reactions_v2"]:
                        platform_kpi_1.append("facebook")
                        info_kpi_1.append("likes and reactions")
                        year_kpi_1.append(datetime.utcfromtimestamp(element["timestamp"]).year)
                        count_kpi_1.append(1)
                # Posts
                if (fb_directory["posts"]) in file_list:
                    fb_file_used = fb_file_used + 1
                    posts_r = json.load(zf.open(fb_directory["posts"]))
                    for element in posts_r:
                        platform_kpi_1.append("facebook")
                        info_kpi_1.append("posts")
                        year_kpi_1.append(datetime.utcfromtimestamp(element["timestamp"]).year)
                        count_kpi_1.append(1)
                # Photos
                if (fb_directory["cover_photos"]) in file_list:
                    fb_file_used = fb_file_used + 1
                    photos_0_r = json.load(zf.open(fb_directory["cover_photos"]))
                    for element in photos_0_r["photos"]:
                        platform_kpi_1.append("facebook")
                        info_kpi_1.append("photos")
                        year_kpi_1.append(datetime.utcfromtimestamp(element["creation_timestamp"]).year)
                        count_kpi_1.append(1)
                if (fb_directory["profile_photos"]) in file_list:
                    fb_file_used = fb_file_used + 1
                    photos_1_r = json.load(zf.open(fb_directory["profile_photos"]))
                    for element in photos_1_r["photos"]:
                        platform_kpi_1.append("facebook")
                        info_kpi_1.append("photos")
                        year_kpi_1.append(datetime.utcfromtimestamp(element["creation_timestamp"]).year)
                        count_kpi_1.append(1)
                if (fb_directory["timeline_photos"]) in file_list:
                    fb_file_used = fb_file_used + 1
                    photos_2_r = json.load(zf.open(fb_directory["timeline_photos"]))
                    for element in photos_2_r["photos"]:
                        platform_kpi_1.append("facebook")
                        info_kpi_1.append("photos")
                        year_kpi_1.append(datetime.utcfromtimestamp(element["creation_timestamp"]).year)
                        count_kpi_1.append(1)
                # Comments
                if (fb_directory["comments"]) in file_list:
                    fb_file_used = fb_file_used + 1
                    comments_r = json.load(zf.open(fb_directory["comments"]))
                    for element in comments_r["comments_v2"]:
                        platform_kpi_1.append("facebook")
                        info_kpi_1.append("comments")
                        year_kpi_1.append(datetime.utcfromtimestamp(element["timestamp"]).year)
                        count_kpi_1.append(1)
                # Aggregate lists of information in df
                df_kpi_layer_1 = pd.DataFrame(
                    {
                        "platform": platform_kpi_1,
                        "info": info_kpi_1,
                        "year": year_kpi_1,
                        "count": count_kpi_1,
                    }
                )
                kpi_layer_1 = df_kpi_layer_1.groupby(["platform", "info", "year"]).sum().reset_index()
                # convert df to JSON
                kpi_layer_1_store = kpi_layer_1.to_json(date_format="iso", orient="split")

                # OUTPUT 3
                # Initialize lists to store data
                platform_behavioural = []
                source_behavioural = []
                year_behavioural = []
                count_behavioural = []
                # Read the relevant files
                # Product behavioural data
                if (fb_directory["visited"]) in file_list:
                    fb_file_used = fb_file_used + 1
                    visited_r = json.load(zf.open(fb_directory["visited"]))
                    if len(visited_r["visited_things_v2"][0]["entries"]) > 0:
                        for i in range(0, len(visited_r["visited_things_v2"][0]["entries"])):
                            platform_behavioural.append("facebook")
                            source_behavioural.append("produit")
                            year_behavioural.append(
                                datetime.utcfromtimestamp(
                                    visited_r["visited_things_v2"][0]["entries"][i]["timestamp"]
                                ).year
                            )
                            count_behavioural.append(1)
                    if len(visited_r["visited_things_v2"][1]["entries"]) > 0:
                        for i in range(0, len(visited_r["visited_things_v2"][1]["entries"])):
                            platform_behavioural.append("facebook")
                            source_behavioural.append("produit")
                            year_behavioural.append(
                                datetime.utcfromtimestamp(
                                    visited_r["visited_things_v2"][1]["entries"][i]["timestamp"]
                                ).year
                            )
                            count_behavioural.append(1)
                    if len(visited_r["visited_things_v2"][2]["entries"]) > 0:
                        for i in range(0, len(visited_r["visited_things_v2"][2]["entries"])):
                            platform_behavioural.append("facebook")
                            source_behavioural.append("produit")
                            year_behavioural.append(
                                datetime.utcfromtimestamp(
                                    visited_r["visited_things_v2"][2]["entries"][i]["timestamp"]
                                ).year
                            )
                            count_behavioural.append(1)
                    # this filepath is a source of many errors depending on the user file structure
                    # if len(visited_r["visited_things_v2"][3]["entries"]) > 0:
                    #     for i in range(0, len(visited_r["visited_things_v2"][3]["entries"])):
                    #         platform_behavioural.append("facebook")
                    #         source_behavioural.append("produit")
                    #         year_behavioural.append(
                    #             datetime.utcfromtimestamp(
                    #                 visited_r["visited_things_v2"][3]["entries"][i]["timestamp"]
                    #             ).year
                    #         )
                    #         count_behavioural.append(1)

                    if (fb_directory["viewed"]) in file_list:
                        fb_file_used = fb_file_used + 1
                        viewed_r = json.load(zf.open(fb_directory["viewed"]))
                        if "entries" in viewed_r["recently_viewed"][0]["children"][0]:
                            if len(viewed_r["recently_viewed"][0]["children"][0]["entries"]) > 0:
                                for i in range(
                                    0,
                                    len(viewed_r["recently_viewed"][0]["children"][0]["entries"]),
                                ):
                                    platform_behavioural.append("facebook")
                                    source_behavioural.append("produit")
                                    year_behavioural.append(
                                        datetime.utcfromtimestamp(
                                            viewed_r["recently_viewed"][0]["children"][0]["entries"][i]["timestamp"]
                                        ).year
                                    )
                                    count_behavioural.append(1)
                        if "entries" in viewed_r["recently_viewed"][1]:
                            if len(viewed_r["recently_viewed"][1]["entries"]) > 0:
                                for i in range(0, len(viewed_r["recently_viewed"][1]["entries"])):
                                    platform_behavioural.append("facebook")
                                    source_behavioural.append("produit")
                                    year_behavioural.append(
                                        datetime.utcfromtimestamp(
                                            viewed_r["recently_viewed"][1]["entries"][i]["timestamp"]
                                        ).year
                                    )
                                    count_behavioural.append(1)
                        if "entries" in viewed_r["recently_viewed"][2]:
                            if len(viewed_r["recently_viewed"][2]["entries"]) > 0:
                                for i in range(0, len(viewed_r["recently_viewed"][2]["entries"])):
                                    platform_behavioural.append("facebook")
                                    source_behavioural.append("produit")
                                    year_behavioural.append(
                                        datetime.utcfromtimestamp(
                                            viewed_r["recently_viewed"][2]["entries"][i]["timestamp"]
                                        ).year
                                    )
                                    count_behavioural.append(1)
                if (fb_directory["interactions_people"]) in file_list:
                    fb_file_used = fb_file_used + 1
                    people_r = json.load(zf.open(fb_directory["interactions_people"]))
                    if len(people_r["people_interactions_v2"][0]["entries"]) > 0:
                        for i in range(0, len(people_r["people_interactions_v2"][0]["entries"])):
                            platform_behavioural.append("facebook")
                            source_behavioural.append("produit")
                            year_behavioural.append(
                                datetime.utcfromtimestamp(
                                    people_r["people_interactions_v2"][0]["entries"][i]["timestamp"]
                                ).year
                            )
                            count_behavioural.append(1)
                if (fb_directory["interactions_events"]) in file_list:
                    fb_file_used = fb_file_used + 1
                    events_r = json.load(zf.open(fb_directory["interactions_events"]))
                    if len(events_r["events_interactions_v2"][0]["entries"]) > 0:
                        for i in range(0, len(events_r["events_interactions_v2"][0]["entries"])):
                            platform_behavioural.append("facebook")
                            source_behavioural.append("produit")
                            year_behavioural.append(
                                datetime.utcfromtimestamp(
                                    events_r["events_interactions_v2"][0]["entries"][i]["timestamp"]
                                ).year
                            )
                            count_behavioural.append(1)
                # Localisation behavioural data
                if (fb_directory["account_activity"]) in file_list:
                    fb_file_used = fb_file_used + 1
                    account_activity_r = json.load(zf.open(fb_directory["account_activity"]))
                    for element in account_activity_r["account_activity_v2"]:
                        platform_behavioural.append("facebook")
                        source_behavioural.append("localisation")
                        year_behavioural.append(datetime.utcfromtimestamp(element["timestamp"]).year)
                        count_behavioural.append(1)
                if (fb_directory["logins_and_logouts"]) in file_list:
                    fb_file_used = fb_file_used + 1
                    logins_logout_r = json.load(zf.open(fb_directory["logins_and_logouts"]))
                    for element in logins_logout_r["account_accesses_v2"]:
                        platform_behavioural.append("facebook")
                        source_behavioural.append("localisation")
                        year_behavioural.append(datetime.utcfromtimestamp(element["timestamp"]).year)
                        count_behavioural.append(1)
                if (fb_directory["login_location"]) in file_list:
                    fb_file_used = fb_file_used + 1
                    logins_r = json.load(zf.open(fb_directory["login_location"]))
                    for element in logins_r["active_sessions_v2"]:
                        platform_behavioural.append("facebook")
                        source_behavioural.append("localisation")
                        year_behavioural.append(datetime.utcfromtimestamp(element["created_timestamp"]).year)
                        count_behavioural.append(1)
                if (fb_directory["used_ip"]) in file_list:
                    fb_file_used = fb_file_used + 1
                    used_ip_r = json.load(zf.open(fb_directory["used_ip"]))
                    for element in used_ip_r["used_ip_address_v2"]:
                        platform_behavioural.append("facebook")
                        source_behavioural.append("localisation")
                        year_behavioural.append(datetime.utcfromtimestamp(element["timestamp"]).year)
                        count_behavioural.append(1)
                if (fb_directory["account_activity"]) in file_list:
                    fb_file_used = fb_file_used + 1
                    account_activity_r = json.load(zf.open(fb_directory["account_activity"]))
                    for element in account_activity_r["account_activity_v2"]:
                        platform_behavioural.append("facebook")
                        source_behavioural.append("connexion")
                        year_behavioural.append(datetime.utcfromtimestamp(element["timestamp"]).year)
                        count_behavioural.append(1)
                if (fb_directory["logins_and_logouts"]) in file_list:
                    fb_file_used = fb_file_used + 1
                    logins_logout_r = json.load(zf.open(fb_directory["logins_and_logouts"]))
                    for element in logins_logout_r["account_accesses_v2"]:
                        platform_behavioural.append("facebook")
                        source_behavioural.append("connexion")
                        year_behavioural.append(datetime.utcfromtimestamp(element["timestamp"]).year)
                        count_behavioural.append(1)
                if (fb_directory["login_location"]) in file_list:
                    fb_file_used = fb_file_used + 1
                    logins_r = json.load(zf.open(fb_directory["login_location"]))
                    for element in logins_r["active_sessions_v2"]:
                        platform_behavioural.append("facebook")
                        source_behavioural.append("connexion")
                        year_behavioural.append(datetime.utcfromtimestamp(element["created_timestamp"]).year)
                        count_behavioural.append(1)
                # Transaction behavioural data
                # Search history behavioural data
                if (fb_directory["search_history"]) in file_list:
                    fb_file_used = fb_file_used + 1
                    search_r = json.load(zf.open(fb_directory["search_history"]))
                    for element in search_r["searches_v2"]:
                        platform_behavioural.append("facebook")
                        source_behavioural.append("historique")
                        year_behavioural.append(datetime.utcfromtimestamp(element["timestamp"]).year)
                        count_behavioural.append(1)
                # Aggregate lists of information in df
                df_behavioural_data = pd.DataFrame(
                    {
                        "platform": platform_behavioural,
                        "source": source_behavioural,
                        "year": year_behavioural,
                        "count": count_behavioural,
                    }
                )
                behavioural_data = df_behavioural_data.groupby(["platform", "source", "year"]).sum().reset_index()
                # convert df to JSON
                behavioural_data_store = behavioural_data.to_json(date_format="iso", orient="split")

                # OUTPUT 4
                # Initialize lists to store data
                platform_kpi_2 = []
                info_kpi_2 = []
                count_kpi_2 = []
                # Read the relevant files
                if (fb_directory["advertisers_interaction"]) in file_list:
                    fb_file_used = fb_file_used + 1
                    ads_interactions = json.load(zf.open(fb_directory["advertisers_interaction"]))
                    platform_kpi_2.append("facebook")
                    info_kpi_2.append("ads_interactions")
                    count_kpi_2.append(len(ads_interactions["history_v2"]))
                # this filepath is a source of many errors depending on the user file structure
                # if (fb_directory["viewed"]) in file_list:
                #     fb_file_used = fb_file_used + 1
                #     viewed_r = json.load(zf.open(fb_directory["viewed"]))
                #     platform_kpi_2.append("facebook")
                #     info_kpi_2.append("ads_interactions")
                #     if len(viewed_r["recently_viewed"]) >= 5:
                #         if "entries" in viewed_r["recently_viewed"][5]:
                #             count_kpi_2.append(len(viewed_r["recently_viewed"][5]["entries"]))
                #         else:
                #             count_kpi_2.append(0)
                #     else:
                #         count_kpi_2.append(0)
                if (fb_directory["ad_contact_info"]) in file_list:
                    fb_file_used = fb_file_used + 1
                    advertisers = json.load(zf.open(fb_directory["ad_contact_info"]))
                    platform_kpi_2.append("facebook")
                    info_kpi_2.append("advertisers")
                    count_kpi_2.append(len(advertisers["custom_audiences_v2"]))
                if (fb_directory["ads_interests"]) in file_list:
                    fb_file_used = fb_file_used + 1
                    ads_interests_1 = json.load(zf.open(fb_directory["ads_interests"]))
                    platform_kpi_2.append("facebook")
                    info_kpi_2.append("ads_interests")
                    count_kpi_2.append(len(ads_interests_1["topics_v2"]))
                if (fb_directory["ads_topics"]) in file_list:
                    fb_file_used = fb_file_used + 1
                    ads_interests_2 = json.load(zf.open(fb_directory["ads_topics"]))
                    platform_kpi_2.append("facebook")
                    info_kpi_2.append("ads_interests")
                    count_kpi_2.append(len(ads_interests_2["inferred_topics_v2"]))
                if (fb_directory["cookies"]) in file_list:
                    fb_file_used = fb_file_used + 1
                    cookies = json.load(zf.open(fb_directory["cookies"]))
                    platform_kpi_2.append("facebook")
                    info_kpi_2.append("cookies")
                    count_kpi_2.append(len(cookies["datr_stats_v2"]))
                # Aggregate lists of information in df
                df_kpi_layer_2 = pd.DataFrame(
                    {
                        "platform": platform_kpi_2,
                        "info": info_kpi_2,
                        "count": count_kpi_2,
                    }
                )
                kpi_layer_2 = df_kpi_layer_2.groupby(["platform", "info"]).sum().reset_index()
                # convert df to JSON
                kpi_layer_2_store = kpi_layer_2.to_json(date_format="iso", orient="split")

                # OUTPUT 5
                platform_ads_interests = []
                ads_interests = []
                # Read the relevant files
                if (fb_directory["ads_interests"]) in file_list:
                    fb_file_used = fb_file_used + 1
                    ads_interests_list_1 = json.load(zf.open(fb_directory["ads_interests"]))
                    for element in ads_interests_list_1["topics_v2"]:
                        platform_ads_interests.append("facebook")
                        ads_interests.append(element)
                if (fb_directory["ads_topics"]) in file_list:
                    fb_file_used = fb_file_used + 1
                    ads_interests_list_2 = json.load(zf.open(fb_directory["ads_topics"]))
                    for element in ads_interests_list_2["inferred_topics_v2"]:
                        platform_ads_interests.append("facebook")
                        ads_interests.append(element)
                # Aggregate lists of information in df
                df_ads_interests = pd.DataFrame({"platform": platform_ads_interests, "interest": ads_interests})
                # convert df to JSON
                ads_interests_store = df_ads_interests.to_json(date_format="iso", orient="split")

                print("Number of Facebook files used is " + str(fb_file_used) + " files")

                return (
                    general_info_1_store,
                    general_info_2_store,
                    kpi_layer_1_store,
                    kpi_layer_2_store,
                    ads_interests_store,
                    behavioural_data_store,
                )


def loading_state_fb():
    """
    Display success message once Google Files have uploaded and parsed
        Parameters:
            n_click (int) :  number of clicks on "Sélectionne ton fichier ZIP Facebook"
            fb-gen-info-1 (dict) : content stored in one of the Facebook dcc.Store components
        Return:
            loading-output-facebook (str) : success message displayed once the Facebook files have been uploaded and parsed
    """


@app.callback(
    Output("loading-output-facebook", "children"),
    [Input("fb-gen-info-1", "data"), Input("click_fb", "n_clicks")],
)
def input_triggers_spinner_fb(fb_data, n_clicks):
    # detect if the url "select your Facebook files" has been clicked
    if n_clicks is not None:
        # time sleep to launch the spinner
        while fb_data is None:
            time.sleep(1)
        # display success message once at least one dcc store is not None
        success_text = "The processing of your Facebook files is finished!"
        return success_text
