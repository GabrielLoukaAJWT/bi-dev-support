import json
from tkinter import messagebox
import sys, os, getpass


import src.GUI.main_window as main_window
import constants as cta
import src.Services.prerun_set as prerun_set


def main():
    prerun_set.createFoldersIfNotExist(
        "local_DB",
        "logs",
        "settings"
    )    
    app = main_window.MainWindow()
    app.root.mainloop()

    print(f"RUNNING APP : {app}")
    print(f"USERNAME WINDOWS {getpass.getuser()}")


if __name__ == "__main__":
    main()