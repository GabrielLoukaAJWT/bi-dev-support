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


def main():
    if checkIfAllFilesExist():
        app = main_window.MainWindow()
    
        print(f"RUNNING APP : {app}")
        print(f"USERNAME WINDOWS {getpass.getuser()}")


if __name__ == "__main__":
    main()