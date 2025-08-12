import json
from tkinter import messagebox
import src.GUI.main_window as main_window
import constants as cta


import sys, os, getpass


def resource_path(relative_path) -> bool:
    if hasattr(sys, '_MEIPASS'):
        full = os.path.join(sys._MEIPASS, relative_path)
    else:
        full = os.path.join(os.path.abspath("."), relative_path)

    return os.path.exists(full)



def checkIfAllFilesExist() -> bool:
    allFilesExit = [
                resource_path(cta.ICON),
                resource_path(cta.LIB_DIR_AJWT),
                resource_path(cta.DIR_LOCAL_DB),
                resource_path(cta.DIR_LOGS),
                resource_path(cta.DIR_SETTINGS),
            ]
    
    return all(allFilesExit)


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
                json.dump({"data": []}, f)
                print("DB created.")

        except FileExistsError:
            print("File already exists.")
        
        try:
            with open(f"{logsPath}/queries.log", "x") as f:
                print("Logs created.")

        except FileExistsError:
            print("File already exists.")
        
        try:
            with open(f"{settingsPath}/settings.json", "x") as f:
                json.dump(
                    {
                        "staySignedIn": False, 
                        "areLogsShown": False, 
                        "credentials": {"username": "", "connectionString": ""}
                    }
                ,f)
                print("Settings created.")

        except FileExistsError:
            print("File already exists.")



def main():
    createFoldersIfNotExist()    
    app = main_window.MainWindow()

    print(f"RUNNING APP : {app}")
    print(f"USERNAME WINDOWS {getpass.getuser()}")


if __name__ == "__main__":
    main()