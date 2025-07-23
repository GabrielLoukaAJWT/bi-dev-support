import tkinter as tk
from tkinter import BOTH, BOTTOM, HORIZONTAL, NONE, X, Scrollbar, scrolledtext
from tkinter import messagebox
import oracledb

import Services.db_connection as cnx
import Services.logging as log
import Services.analytics as analytics

import GUI.analytics_view as analytics_view

class QueryView:
    def __init__(self, root, oracleConnector: cnx.OracleConnector):        
        self.root = root        
        self.oracleConnector = oracleConnector
        self.queryLoggerManager = log.QueryLoggerManager()   

        # self.queryLoggerManager.clearLogsFile()

        self.setupUI()


        print(F"QUERY VIEW CREATED")

    def setupUI(self):
        # main query view
        self.frame = tk.Frame(self.root, padx=20, pady=20, bg="#f7f7f7")
        self.frame.pack(fill="both", expand=True)

        tk.Label(self.frame, text="Enter SQL Query", font=("Arial", 14, "bold"), bg="#f7f7f7").pack(pady=(0, 10))

        self.query_text = tk.Text(self.frame, height=12, width=80, font=("Courier New", 11), relief="solid", bd=1)
        self.query_text.pack(pady=(0, 15))

        tk.Button(self.frame,
                text="Run Query",
                font=("Arial", 12, "bold"),
                bg="#2196F3",
                fg="white",
                activebackground="#1976D2",
                padx=10,
                pady=5,
                command=self.runQuery
                ).pack(pady=(0, 15))

        self.output_box = scrolledtext.ScrolledText(self.frame,
                                                    height=15,
                                                    wrap=tk.NONE,
                                                    font=("Courier New", 10),
                                                    relief="solid",
                                                    bd=1,
                                                    xscrollcommand=None)
        self.output_box.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)

        x_scroll = tk.Scrollbar(self.frame, orient=tk.HORIZONTAL, command=self.output_box.xview)
        x_scroll.pack(side=tk.BOTTOM, fill=tk.X)
        self.output_box.config(xscrollcommand=x_scroll.set)

        self.status_label = tk.Label(self.frame,
                                    text="",
                                    font=("Arial", 10),
                                    fg="red",
                                    bg="#f7f7f7")
        self.status_label.pack(pady=(10, 2))

        self.execTimeLabel = tk.Label(self.frame,
                                    text="",
                                    font=("Arial", 14),
                                    fg="gray",
                                    bg="#f7f7f7")
        self.execTimeLabel.pack(pady=(0, 10))


        # log panel
        self.show_logs = False
        self.toggle_logs_btn = tk.Button(self.frame,
                                        text="Show Logs",
                                        font=("Arial", 10),
                                        command=self.toggleLogs,
                                        bg="#eeeeee")
        self.toggle_logs_btn.pack(pady=(10, 0))

        self.logs_frame = tk.Frame(self.frame, bg="#f0f0f0", relief="groove", bd=1)
        self.logs_box = scrolledtext.ScrolledText(self.logs_frame,
                                                height=10,
                                                width=100,
                                                state="disabled",
                                                font=("Courier New", 10),
                                                wrap="word")
        self.logs_box.pack(padx=10, pady=10, fill="both", expand=True)

        # analytics 
        self.accessAnalyticsButton = tk.Button(self.frame,
                text="Access analytics",
                font=("Arial", 12, "bold"),
                bg="#2196F3",
                fg="white",
                activebackground="#1976D2",
                padx=10,
                pady=5,
                command=self.openAnalyticsWindow
        ).pack(pady=(0, 15), side=tk.TOP, anchor=tk.NE)


    def runQuery(self):    
        sql = self.query_text.get("1.0", tk.END).strip()
        if not sql:
            messagebox.showwarning("Empty Query", "Please enter a query.")
            self.status_label.config(text="") 
            self.execTimeLabel.config(text="")
            return

        err = self.oracleConnector.runQuery(sql)
        if err:              
            self.status_label.config(text=err, fg="red")  
            self.execTimeLabel.config(text="")
            self.queryLoggerManager.addLog("error", self.oracleConnector.currentQuery, err)
        else:
            self.status_label.config(text="") 
            text = f"{len(self.oracleConnector.currentQuery.rows)} rows in {str(self.oracleConnector.currentQuery.execTime)}"
            self.execTimeLabel.config(text=text)
            self.displayQueryOutput()
            self.queryLoggerManager.addLog("info", self.oracleConnector.currentQuery, err)

        self.displayLogsOnToggle()

    def displayQueryOutput(self):
        self.output_box.delete("1.0", tk.END)
        if not self.oracleConnector.currentQuery.rows:
            self.output_box.insert(tk.END, "No results found.")
            return
        formatted = self.formatRows(
            self.oracleConnector.currentQuery.columns, 
            self.oracleConnector.currentQuery.rows)
        self.output_box.insert(tk.END, formatted)


    def calculateColumnWidths(self, columns, rows):
        widths = [len(col) for col in columns]
        for row in rows:
            if len(row) != len(columns):
                raise ValueError("Row length does not match number of columns")
            for i, val in enumerate(row):
                if isinstance(val, oracledb.LOB):
                    val_str = "[LOB]"
                elif isinstance(val, bytes):
                    val_str = val.decode('utf-8', errors='replace')
                elif val is None:
                    val_str = ""
                else:
                    val_str = str(val)
                widths[i] = max(widths[i], len(val_str))
        return widths
    
    
    def formatRowSafely(self, row, col_widths):
        formatted = []
        for i, val in enumerate(row):
            if isinstance(val, oracledb.LOB):
                val_str = "[LOB]"
            elif isinstance(val, bytes):
                val_str = val.decode('utf-8', errors='replace')
            elif val is None:
                val_str = ""
            else:
                val_str = str(val)
            formatted.append(val_str.ljust(col_widths[i]))
        return " | ".join(formatted)


        
    def formatRows(self, columns, rows):
        col_widths = self.calculateColumnWidths(columns, rows)

        header = " | ".join(col.ljust(col_widths[i]) for i, col in enumerate(columns))
        separator = "-+-".join("-" * w for w in col_widths)

        lines = [header, separator]

        for row in rows:
            lines.append(self.formatRowSafely(row, col_widths))

        return "\n".join(lines)
    

    def toggleLogs(self):
        if self.show_logs:
            self.logs_frame.pack_forget()
            self.toggle_logs_btn.config(text="Show Logs")
        else:
            self.displayLogsOnToggle()
            self.logs_frame.pack(fill="both", expand=True, pady=(5, 10))
            self.toggle_logs_btn.config(text="Hide Logs")
        self.show_logs = not self.show_logs

    def displayLogsOnToggle(self):
        try:
            with open("./logs/queries.log", "r", encoding="utf-8") as f:
                log_content = f.read()
        except FileNotFoundError:
            log_content = "No log file found."

        self.logs_box.config(state="normal")
        self.logs_box.delete("1.0", "end")
        self.logs_box.insert("1.0", log_content)
        self.logs_box.see(tk.END)
        self.logs_box.config(state="disabled")

        f.close()

    def openAnalyticsWindow(self):
        analytics_view.AnalyticsView(self.root, self.queryLoggerManager)
        print("Accessing analytics window\n")







    