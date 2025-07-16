import Services.db_connection as con
import GUI.main_window as win



def main():
    app = win.OracleApp()
    app.initializeWindow()

if __name__ == "__main__":
    main()