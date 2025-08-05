import GUI.main_window
import GUI

import Services.database as db

import sys, os, getpass


def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)


def main():
    if resource_path("assets\images\favicon.ico"):
        app = GUI.main_window.MainWindow()
    print(f"RUNNING APP : {app}")
    print(f"USERNAME WINDOWS {getpass.getuser()}")


if __name__ == "__main__":
    main()