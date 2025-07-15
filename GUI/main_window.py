import tkinter as tk
from tkinter import messagebox

import db_connection as cnx


def on_connect_click():
    password = password_entry.get()
    result = cnx.connect_to_oracle(password)
    messagebox.showinfo("Oracle Connection Result", result)

def start_ui():
    root = tk.Tk()
    root.title("Oracle DB Connector")
    root.geometry("350x200")

    tk.Label(root, text="Enter Oracle DB Password:").pack(pady=(20, 5))

    global password_entry
    password_entry = tk.Entry(root, show="*", width=30)
    password_entry.pack(pady=5)

    connect_button = tk.Button(root, text="Connect & Fetch", command=cnx.connect_to_oracle)
    connect_button.pack(pady=20)

    root.mainloop()