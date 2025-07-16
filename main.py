import GUI.main_window
import GUI.query_view
import Services.db_connection as con
import GUI



def main():
    app = GUI.main_window.MainWindow()
    app.initializeMainView()


if __name__ == "__main__":
    main()