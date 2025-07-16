import tkinter as tk
from tkinter import messagebox

import db_connection as cnx
import constants as cta


class OracleApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Oracle DB Connector")
        self.root.geometry("500x300")
        
        self.setup_ui()

    def setup_ui(self):
        tk.Label(self.root, text="Enter Oracle DB Password:").pack(pady=(20, 5))

        self.password_entry = tk.Entry(self.root, show="*", width=30)
        self.password_entry.pack(pady=5)

        tk.Button(self.root, text="Connect & Fetch", command=self.handle_connect).pack(pady=20)

        self.status_label = tk.Label(self.root, text="", font=("Arial", 10))
        self.status_label.pack(pady=10)

    def handle_connect(self):
        password = self.password_entry.get()
        is_successful, message = cnx.connect_to_oracle(password)
        self.show_status(is_successful, message)

    def show_status(self, success: bool, message: str):
        color = "green" if success else "red"
        self.status_label.config(text=message, fg=color)

    def initialize_window(self):
        self.root.mainloop()