import GUI.main_window
import GUI

import Services.database as db


def main():
    app = GUI.main_window.MainWindow()
    app.initializeMainView()



if __name__ == "__main__":
    main()