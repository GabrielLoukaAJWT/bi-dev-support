import tkinter as tk
from tkinter import messagebox

import db_connection as cnx
import constants as cta


def handle_connection_labels(frame: tk.Frame, is_successful: bool):
    for widget in frame.winfo_children():
        widget.destroy()

    status = cta.DB_CONNECTION_SUCCESS if is_successful else cta.DB_CONNECTION_ERR
    label = tk.Label(frame, text=status, fg="green" if is_successful else "red")
    label.pack()



def start_ui():
    root = tk.Tk()
    root.title("Oracle DB Connector")
    root.geometry("500x300")

    tk.Label(root, text="Enter Oracle DB Password:").pack(pady=(20, 5))

    password_entry = tk.Entry(root, show="*", width=30)
    password_entry.pack(pady=5)

    status_frame = tk.Frame(root)
    status_frame.pack(pady=10)

    def on_connect():
        result = cnx.connect_to_oracle(password_entry.get())
        handle_connection_labels(status_frame, result)

    tk.Button(root, text="Connect & Fetch", command=on_connect).pack(pady=20)

    root.mainloop()