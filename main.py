import db_connection as con
import GUI.main_window as win



def main():
    app = win.OracleApp()
    app.initialize_window()


if __name__ == "__main__":
    main()