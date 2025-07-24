import GUI.main_window
import GUI

import Services.database as db


def main():
    app = GUI.main_window.MainWindow()
    print(f"RUNNING APP : {app}")


if __name__ == "__main__":
    main()