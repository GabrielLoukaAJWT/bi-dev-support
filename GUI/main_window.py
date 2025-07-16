import tkinter as tk
from tkinter import messagebox

import Services.db_connection as cnx
import constants as cta


class OracleApp:
    def __init__(self):
        self.oracleConnector = cnx.OracleConnector()
        self.root = tk.Tk()
        self.root.title("Oracle DB Connector")
        self.root.geometry("500x300")
        
        self.setupMainUI()


    def setupMainUI(self):
        tk.Label(self.root, text="Enter Oracle DB Password:").pack(pady=(20, 5))

        self.password_entry = tk.Entry(self.root, show="*", width=30)
        self.password_entry.pack(pady=5)

        tk.Button(self.root, text="Connect & Fetch", command=self.handleConnexion).pack(pady=20)

        self.status_label = tk.Label(self.root, text="", font=("Arial", 10))
        self.status_label.pack(pady=10)


    def handleConnexion(self):
        password = self.password_entry.get()
        isSuccessful, message = self.oracleConnector.connectToOracle(password)
        self.showStatus(isSuccessful, message)


    def showStatus(self, success: bool, message: str):
        color = "green" if success else "red"
        self.status_label.config(text=message, fg=color)


    def initializeWindow(self):
        self.root.mainloop()