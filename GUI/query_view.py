import tkinter as tk
from tkinter import NONE, scrolledtext
from tkinter import messagebox

import Services.db_connection as cnx


class QueryView:
    def __init__(self, root, oracleConnector: cnx.OracleConnector):
        self.oracleConnector = oracleConnector
        self.frame = tk.Frame(root)
        self.frame.pack(pady=20)

        tk.Label(self.frame, text="Enter SQL Query:").pack()

        self.query_text = tk.Text(self.frame, height=8, width=80)
        self.query_text.pack(pady=5)

        tk.Button(self.frame, text="Run Query", command=self.runQuery).pack(pady=10)

        self.output_box = scrolledtext.ScrolledText(self.frame, height=10, wrap=NONE)
        self.output_box.pack()

        self.status_label = tk.Label(self.frame, text="", font=("Arial", 10))          
        self.status_label.pack(pady=10)
        

    def runQuery(self):    
        sql = self.query_text.get("1.0", tk.END).strip()
        if not sql:
            messagebox.showwarning("Empty Query", "Please enter a query.")
            self.status_label.config(text="") 
            return

        err = self.oracleConnector.runQuery(sql)
        if err:              
            self.status_label.config(text=err, fg="red")  
        else:
            self.status_label.config(text="") 
            self.displayQueryOutput()


    def displayQueryOutput(self):
        self.output_box.delete("1.0", tk.END)
        if not self.oracleConnector.queryOutput:
            self.output_box.insert(tk.END, "No results found.")
            return
        formatted = self.formatRows(self.oracleConnector.columnsNames, self.oracleConnector.queryOutput)
        self.output_box.insert(tk.END, formatted)


    def calculateColumnWidths(self, columns, rows):
        widths = [len(col) for col in columns]
        for row in rows:
            for i, val in enumerate(row):
                widths[i] = max(widths[i], len(str(val)))
        return widths
    
    
    def formatRows(self, columns, rows):
        col_widths = self.calculateColumnWidths(columns, rows)

        header = " | ".join(col.ljust(col_widths[i]) for i, col in enumerate(columns))
        separator = "-+-".join("-" * w for w in col_widths)

        lines = [header, separator]

        for row in rows:
            line = " | ".join(str(val).ljust(col_widths[i]) for i, val in enumerate(row))
            lines.append(line)

        return "\n".join(lines)



    