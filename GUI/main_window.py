import tkinter as tk
from tkinter import messagebox

import db_connection as cnx



def start_ui():
    root = tk.Tk()
    root.title("Oracle DB Connector")
    root.geometry("350x200")

    tk.Label(root, text="Enter Oracle DB Password:").pack(pady=(20, 5))

    password_entry = tk.Entry(root, show="*", width=30)
    password_entry.pack(pady=5)

    connect_button = tk.Button(root, text="Connect & Fetch", command= lambda: cnx.connect_to_oracle(password_entry.get()))
    connect_button.pack(pady=20)

    root.mainloop()