import sys, os, getpass
import json

import constants as cta


def createFoldersIfNotExist() -> None:
    foldersCreatedSuccess = False

    dbPath = "local_DB"
    logsPath = "logs"
    settingsPath = "settings"

    try:
        os.makedirs(dbPath, exist_ok=True)
        os.makedirs(logsPath, exist_ok=True)
        os.makedirs(settingsPath, exist_ok=True)

        foldersCreatedSuccess = True

    finally:
        pass

    if foldersCreatedSuccess:
        try:
            with open(f"{dbPath}/queries.json", "x") as f:
                json.dump({"data": []}, f, indent=4)
                print("DB created.")

        except FileExistsError:
            print("DB already exists.")
        
        try:
            with open(f"{logsPath}/queries.log", "x") as f:
                print("Logs created.")

        except FileExistsError:
            print("Logs file already exists.")


        try:
            with open(f"{settingsPath}/general.json", "x") as f:
                json.dump(
                    {
                        "areLogsShown": False,
                        "isDarkMode" : False
                    },
                    f, 
                    indent=4
                )
                print("General settings created.")

        except FileExistsError:
            print("General settings file already exists.")

        
        try:
            with open(f"{settingsPath}/account.json", "x") as f:
                json.dump(
                    {
                        "staySignedIn": False, 
                        "credentials": {"username": "", "connectionString": ""}
                    },
                    f, 
                    indent=4
                )
                print("Account settings created.")

        except FileExistsError:
            print("Account settings file already exists.")
        
        
        try:
            with open(f"{settingsPath}/set_queries.json", "x") as f:
                json.dump(
                    {
                        
                    },
                    f, 
                    indent=4
                )
                print("Queries settings file created.")

        except FileExistsError:
            print("Queries settings file already exists.")
        
        
        try:
            with open(f"{settingsPath}/analytics.json", "x") as f:
                json.dump(
                    {
                        
                    },
                    f, 
                    indent=4
                )
                print("Analytics settings file created.")

        except FileExistsError:
            print("Analytics settings file already exists.")


        