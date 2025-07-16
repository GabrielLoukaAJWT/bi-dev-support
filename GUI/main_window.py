import tkinter as tk
from tkinter import messagebox
import time

import Services.db_connection as cnx
import constants as cta
import GUI.query_view as qryview


class MainWindow:
    def __init__(self):
        self.oracleConnector = cnx.OracleConnector()
        self.root = tk.Tk()
        self.root.title("SQL analytics")
        self.root.geometry("800x550")
        
        self.setupMainUI()


    def setupMainUI(self):
        tk.Label(self.root, text="Enter Oracle DB Password:").pack(pady=(20, 5))

        self.password_entry = tk.Entry(self.root, show="*", width=30)
        self.password_entry.pack(pady=5)

        tk.Button(self.root, text="Connect", command=self.handleConnection).pack(pady=20)

        self.status_label = tk.Label(self.root, text="", font=("Arial", 10))
        self.status_label.pack(pady=10)


    def handleConnection(self):
        password = self.password_entry.get()
        isSuccessful, message = self.oracleConnector.connectToOracle(password)

        print(self.oracleConnector.connection)
        print(self.oracleConnector.cursor)
        self.showStatus(isSuccessful, message)

        if isSuccessful:
            self.root.update_idletasks()
            self.root.after(1000, self.clearRoot())
            self.initializeQueryViewPortConnection()


    def clearRoot(self):
        for widget in self.root.winfo_children():
            widget.destroy()


    def showStatus(self, success: bool, message: str):
        color = "green" if success else "red"
        self.status_label.config(text=message, fg=color)        


    def initializeMainView(self):
        self.root.mainloop()

    
    def initializeQueryViewPortConnection(self):
        self.queryView = qryview.QueryView(self.root, self.oracleConnector)