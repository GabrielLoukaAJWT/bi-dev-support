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
        self.root.geometry("1000x750")
        
        self.setupMainUI()


    def setupMainUI(self):
        main_frame = tk.Frame(self.root, padx=30, pady=30, bg="#f7f7f7")
        main_frame.pack(expand=True)

        title_label = tk.Label(main_frame, text="Oracle DB Login", font=("Arial", 16, "bold"), bg="#f7f7f7")
        title_label.pack(pady=(0, 20))

        tk.Label(main_frame, text="Enter Oracle DB Password:", font=("Arial", 12), bg="#f7f7f7").pack(pady=(0, 5))

        self.password_entry = tk.Entry(main_frame, show="*", font=("Arial", 12), width=30, relief="solid", bd=1)
        self.password_entry.pack(pady=5, ipady=4)

        connect_btn = tk.Button(main_frame, text="Connect", font=("Arial", 12, "bold"), bg="#4CAF50", fg="white",
                                activebackground="#45A049", padx=10, pady=5, command=self.handleConnection)
        connect_btn.pack(pady=20)

        self.status_label = tk.Label(main_frame, text="", font=("Arial", 10), fg="red", bg="#f7f7f7")
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