import tkinter as tk
from tkinter import scrolledtext
from tkinter import messagebox

import Services.db_connection as cnx


class QueryView:
    def __init__(self, root, oracleConnector: cnx.OracleConnector):
        self.oracleConnector = oracleConnector
        self.frame = tk.Frame(root)
        self.frame.pack(pady=20)

        tk.Label(self.frame, text="Enter SQL Query:").pack()

        self.query_text = tk.Text(self.frame, height=6, width=70)
        self.query_text.pack(pady=5)

        tk.Button(self.frame, text="Run Query", command=self.run_query).pack(pady=10)

        self.output_box = scrolledtext.ScrolledText(self.frame, height=10, width=70)
        self.output_box.pack()

    def run_query(self):
        sql = self.query_text.get("1.0", tk.END).strip()
        if not sql:
            messagebox.showwarning("Empty Query", "Please enter a query.")
            return

        self.oracleConnector.run_query(sql)
