import base64
from datetime import datetime
import io
import json
from zipfile import ZipFile
import pandas as pd
import time
import os


from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from app import app


def parse_google_files():
    """
    Parse the ZIP file uploaded in the dcc.upload component dedicated to Google
        Parameters:
            contents (str) :  content of the ZIP file encoded in base 64
            filename (str) : name of the ZIP file uploaded
            last_modified (ts) : timestamp at which the folder had been uploaded
        Return:
            general_info (JSON) : user general attributes stored plotted in left panels of tab1
            behavioural_data_store (JSON) : used to plot behavioural chart on tab2
    """

    @app.callback(
        [
            Output("gg-gen-info", "data"),
            Output("gg-behavioural-data", "data"),
        ],
        [Input("upload-data-google", "contents")],
        [
            State("upload-data-google", "filename"),
            State("upload-data-google", "last_modified"),
        ],
    )
    def update_output_google(list_of_contents, list_of_names, list_of_dates):
        # check if a file has been uploaded, if not prevent the callback to be fired
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

                # you can do what you wanna do with the zip object here

                # Identify files existing in uploaded folder directory
                file_list = []
                for zinfo in zf.filelist:
                    file_list.append(zinfo.filename)
                # Get the size of the folder uploaded in MB
                filesize = float(sum([zinfo.file_size for zinfo in zf.filelist])) / 1000000

                # As the folder is potentially heavy, set a time sleep to let the function ingest files before reading
                time.sleep(5)

                # check if the Google folder names are in EN or FR
                if (
                    (os.path.join(filename + "/Profile", "Profile.json") in file_list)
                    or (os.path.join(filename + "/Home App", "HomeHistory.json") in file_list)
                    or (os.path.join(filename + "/Location History", "Location History.json") in file_list)
                    or (os.path.join(filename + "/Location History", "Location History.json") in file_list)
                    or (os.path.join(filename + "/Saved", "Favourite places.csv") in file_list)
                ):
                    # Create dictionary with all the possible EN filepaths in the uploaded google folder directory
                    gg_directory = {
                        "profile_information": os.path.join("/Profile", "Profile.json"),
                        "autofill": os.path.join("/Chrome", "Autofill.json"),
                        "youtube_subscriptions": os.path.join(
                            "/YouTube and YouTube┬áMusic", "subscriptions", "subscriptions.json"
                        ),
                        "play_store_library": os.path.join("/Google Play Store", "Library.json"),
                        "play_store_installs": os.path.join("/Google Play Store", "Installs.json"),
                        "google_home": os.path.join("/Home App", "HomeHistory.json"),
                        "addresses_to_visit": os.path.join("/Saved", "Want to go.csv"),  # issue with filepath
                        "addresses_favourite": os.path.join("/Saved", "Favourite places.csv"),
                        "addresses_sellers": os.path.join("/Saved", "Adresses vendeurs.csv"),
                        "localisation_history": os.path.join("/Location History", "Location History.json"),
                        "browser_history": os.path.join("/Chrome", "BrowserHistory.json"),
                    }
                else:
                    # Create dictionary with all the possible FR filepaths in the uploaded google folder directory
                    gg_directory = {
                        "profile_information": os.path.join("/Profil", "Profil.json"),
                        "autofill": os.path.join("/Chrome", "Autofill.json"),
                        "play_store_library": os.path.join("/Google Play┬áStore", "Library.json"),
                        "play_store_installs": os.path.join("/Google Play┬áStore", "Installs.json"),
                        "google_home": os.path.join("/Application Google┬áHome", "HomeHistory.json"),
                        "addresses_to_visit": os.path.join("/Enregistré", "A╠Ç visiter.csv"),  # issue with filepath
                        "addresses_favourite": os.path.join("/Enregistre╠ü", "Adresses favorites.csv"),
                        "addresses_sellers": os.path.join("/Enregistre╠ü", "Adresses vendeurs.csv"),
                        "localisation_history": os.path.join(
                            "/Historique des positions", "Historique des positions.json"
                        ),
                        "google_pay": os.path.join(
                            "/Google┬áPay",
                            "Envois et demandes d_argent",
                            "Envois et demandes d_argent.csv",
                        ),
                        "browser_history": os.path.join("/Chrome", "BrowserHistory.json"),
                    }

                gg_file_used = 0
                # OUTPUT #1
                # Read the relevant files
                if (filename + gg_directory["profile_information"]) in file_list:
                    gg_file_used = gg_file_used + 1
                    profile_information = json.load(zf.open(filename + gg_directory["profile_information"]))
                    pseudo = profile_information["name"]["formattedName"]
                    mail = profile_information["emails"][0]["value"]
                else:
                    pseudo = None
                    mail = None
                if (filename + gg_directory["autofill"]) in file_list:
                    gg_file_used = gg_file_used + 1
                    autofill = json.load(zf.open(filename + gg_directory["autofill"]))
                    phone_numbers = []
                    if len(autofill["Autofill Profile"]) > 0:
                        for element in autofill["Autofill Profile"]:
                            if element["phone_home_whole_number"][0]:
                                phone_numbers.append(element["phone_home_whole_number"][0])
                        phone_numbers = set(phone_numbers)
                        tel = ", ".join([str(elem) for elem in phone_numbers])
                    else:
                        tel = None
                    addresses = []
                    if len(autofill["Autofill Profile"]) > 0:
                        for element in autofill["Autofill Profile"]:
                            if element["address_home_street_address"]:
                                addresses.append(element["address_home_street_address"])
                        addresses = set(addresses)
                        physical_address = ", ".join([str(elem) for elem in addresses])
                    else:
                        physical_address = None
                else:
                    tel = None
                    physical_address = None

                general_info = {
                    "pseudo": pseudo,
                    "size_footprint": filesize,
                    "physical_address": physical_address,
                    "e-mail": mail,
                    "phone_number": tel,
                }

                # convert dict to JSON
                general_info_store = json.dumps(general_info, indent=4)

                # OUTPUT #2
                # Initialize lists to store data
                platform_behavioural = []
                source_behavioural = []
                year_behavioural = []
                count_behavioural = []

                # Read the relevant files
                # Product behavioural data
                if (filename + gg_directory["play_store_library"]) in file_list:
                    gg_file_used = gg_file_used + 1
                    play_store_library_r = json.load(zf.open(filename + gg_directory["play_store_library"]))
                    if len(play_store_library_r) > 0:
                        for element in play_store_library_r:
                            platform_behavioural.append("google")
                            source_behavioural.append("produit")
                            year_behavioural.append(element["libraryDoc"]["acquisitionTime"][:4])
                            count_behavioural.append(1)

                # Localisation behavioural data
                if (filename + gg_directory["addresses_favourite"]) in file_list:
                    gg_file_used = gg_file_used + 1
                    favourite_addresses_r = pd.read_csv(zf.open(filename + gg_directory["addresses_favourite"]))
                    if gg_directory["addresses_favourite"] == os.path.join("/Enregistre╠ü", "Adresses favorites.csv"):
                        if len(favourite_addresses_r["Titre"]) > 0:
                            for element in favourite_addresses_r["Titre"]:
                                platform_behavioural.append("google")
                                source_behavioural.append("localisation")
                                year_behavioural.append(
                                    2021
                                )  # set 2021 as default date as we don't have dates for each event
                                count_behavioural.append(1)
                    else:
                        if len(favourite_addresses_r["Title"]) > 0:
                            for element in favourite_addresses_r["Title"]:
                                platform_behavioural.append("google")
                                source_behavioural.append("localisation")
                                year_behavioural.append(
                                    2021
                                )  # set 2021 as default date as we don't have dates for each event
                                count_behavioural.append(1)
                if (filename + gg_directory["addresses_sellers"]) in file_list:
                    gg_file_used = gg_file_used + 1
                    sellers_addresses_r = pd.read_csv(zf.open(filename + gg_directory["addresses_sellers"]))
                    if gg_directory["addresses_favourite"] == os.path.join("/Enregistre╠ü", "Adresses favorites.csv"):
                        if len(sellers_addresses_r["Titre"]) > 0:
                            for element in sellers_addresses_r["Titre"]:
                                platform_behavioural.append("google")
                                source_behavioural.append("localisation")
                                year_behavioural.append(
                                    2021
                                )  # set 2021 as default date as we don't have dates for each event
                                count_behavioural.append(1)
                    else:
                        if len(sellers_addresses_r["Title"]) > 0:
                            for element in sellers_addresses_r["Title"]:
                                platform_behavioural.append("google")
                                source_behavioural.append("localisation")
                                year_behavioural.append(
                                    2021
                                )  # set 2021 as default date as we don't have dates for each event
                                count_behavioural.append(1)
                if (filename + gg_directory["localisation_history"]) in file_list:
                    gg_file_used = gg_file_used + 1
                    # set another time sleep as the file is potentially heavy
                    time.sleep(5)
                    localisation_r = json.load(zf.open(filename + gg_directory["localisation_history"]))
                    if len(localisation_r["locations"]) > 0:
                        for element in localisation_r["locations"]:
                            platform_behavioural.append("google")
                            source_behavioural.append("localisation")
                            year_behavioural.append(datetime.fromtimestamp(int(element["timestampMs"]) / 1000).year)
                            count_behavioural.append(1)

                # Search history behavioural data
                if (filename + gg_directory["browser_history"]) in file_list:
                    gg_file_used = gg_file_used + 1
                    # set another time sleep as the file is potentially heavy
                    time.sleep(5)
                    browser_history_r = json.load(zf.open(filename + gg_directory["browser_history"]))
                    if len(browser_history_r["Browser History"]) > 0:
                        for element in browser_history_r["Browser History"]:
                            platform_behavioural.append("google")
                            source_behavioural.append("historique")
                            year_behavioural.append(datetime.fromtimestamp(int(element["time_usec"]) / 1000000).year)
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

                print("Number of Google files used is " + str(gg_file_used) + " files")
                print(general_info)
                print(behavioural_data)

                return general_info_store, behavioural_data_store


def loading_state_gg():
    """
    Display success message once Google Files have uploaded and parsed
        Parameters:
            n_click (int) :  number of clicks on "Sélectionne ton fichier ZIP Google"
            gg-gen-info (dict) : content stored in one of the Google dcc.Store components
        Return:
            loading-output-google (str) : success message displayed once the Google files have been uploaded and parsed
    """


@app.callback(
    Output("loading-output-google", "children"),
    [Input("gg-gen-info", "data"), Input("click_gg", "n_clicks")],
)
def input_triggers_spinner_gg(gg_data, n_clicks):
    # detect if the url "séléctionne tes fichiers Facebook" has been clicked
    if n_clicks is not None:
        # time sleep to launch the spinner
        while gg_data is None:
            time.sleep(1)
        # display success message once at least one dcc store is not None
        success_text = "Le traitement de tes fichiers Google est terminé !"
        return success_text
