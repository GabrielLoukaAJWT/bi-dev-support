import threading
import oracledb

import tkinter as tk
from tkinter import scrolledtext
from tkinter import messagebox

from multiprocessing import Queue, Process
import queue

import Services.db_connection as cnx
import Services.logging as log
import Services.database as db

import GUI.analytics_view as analytics_view


class QueryView:
    def __init__(self, root, oracleConnector: cnx.OracleConnector):        
        self.root = root        
        self.tl = None

        self.oracleConnector = oracleConnector
        self.queryLoggerManager = log.QueryLoggerManager()   
        self.databaseManager = db.DatabaseManager()

        # have to create a process for running a query because it crashes when clicking the window while running        
        self.query_result_queue = queue.Queue()

        self.queryLoggerManager.clearLogsFile()
        self.setupUI()


        print(F"QUERY VIEW CREATED")

    def setupUI(self):
        self.root.configure(bg="#f7f7f7")
        self.frame = tk.Frame(self.root, padx=20, pady=20, bg="#f7f7f7")
        self.frame.pack(fill="both", expand=True)

        heading_font = ("Arial", 14, "bold")
        label_font = ("Arial", 12)
        input_font = ("Courier New", 11)
        action_button_font = ("Arial", 12, "bold")
        gray_bg = "#f7f7f7"

        # --- Title ---
        tk.Label(
            self.frame,
            text="Enter SQL Query",
            font=heading_font,
            bg=gray_bg,
            fg="#333"
        ).pack(pady=(0, 15))

        # --- Query Input Section ---
        query_input_frame = tk.Frame(self.frame, bg=gray_bg)
        query_input_frame.pack(fill="x", pady=(10, 20))

        tk.Label(
            query_input_frame,
            text="Query Name",
            font=label_font,
            anchor="w",
            bg=gray_bg,
            fg="#444"
        ).pack(fill="x", padx=5, pady=(0, 5))

        self.queryNameEntry = tk.Entry(
            query_input_frame,
            font=input_font,
            relief="solid",
            bd=1,
            validate="key",
            validatecommand=((self.root.register(self.validateQueryNameForEntry)), '%P')
        )
        self.queryNameEntry.pack(fill="x", padx=5, ipady=5)

        tk.Label(
            query_input_frame,
            text="SQL Query",
            font=label_font,
            anchor="w",
            bg=gray_bg,
            fg="#444"
        ).pack(fill="x", padx=5, pady=(15, 5))

        self.query_text = tk.Text(
            query_input_frame,
            height=12,
            font=input_font,
            relief="solid",
            bd=1
        )
        self.query_text.pack(fill="x", padx=5, pady=(0, 10))

        # --- Run Query Button ---
        self.runQueryButton = tk.Button(
            self.frame,
            text="▶ Run Query",
            font=action_button_font,
            bg="#2196F3",
            fg="white",
            activebackground="#1976D2",
            activeforeground="white",
            padx=15,
            pady=8,
            cursor="hand2",
            command=self.runQuery
        )
        self.runQueryButton.pack(pady=(0, 20))

        # --- Output Box ---
        self.output_box = scrolledtext.ScrolledText(
            self.frame,
            height=12,
            wrap=tk.NONE,
            font=("Courier New", 10),
            relief="solid",
            bd=1
        )
        self.output_box.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))

        x_scroll = tk.Scrollbar(self.frame, orient=tk.HORIZONTAL, command=self.output_box.xview)
        x_scroll.pack(side=tk.BOTTOM, fill=tk.X)
        self.output_box.config(xscrollcommand=x_scroll.set)

        # --- Status Labels ---
        self.status_label = tk.Label(
            self.frame,
            text="",
            font=("Arial", 10),
            fg="red",
            bg=gray_bg
        )
        self.status_label.pack(pady=(10, 2))

        self.execTimeLabel = tk.Label(
            self.frame,
            text="",
            font=("Arial", 14),
            fg="gray",
            bg=gray_bg
        )
        self.execTimeLabel.pack(pady=(0, 15))

        # --- Toggle Logs Button ---
        self.show_logs = False
        self.toggle_logs_btn = tk.Button(
            self.frame,
            text="🪵 Show Logs",
            font=("Arial", 10),
            command=self.toggleLogs,
            bg="#eeeeee",
            fg="#333",
            relief="flat",
            cursor="hand2"
        )
        self.toggle_logs_btn.pack(pady=(10, 0))

        # --- Logs Frame ---
        self.logs_frame = tk.Frame(self.frame, bg="#f0f0f0", relief="groove", bd=1)
        self.logs_box = scrolledtext.ScrolledText(
            self.logs_frame,
            height=10,
            width=100,
            state="disabled",
            font=("Courier New", 10),
            wrap="word"
        )
        self.logs_box.pack(padx=10, pady=10, fill="both", expand=True)

        # --- Access Analytics Button ---
        self.accessAnalyticsButton = tk.Button(
            self.frame,
            text="📈 Access Analytics",
            font=action_button_font,
            bg="#4CAF50",
            fg="white",
            activebackground="#45a049",
            padx=15,
            pady=8,
            command=self.openAnalyticsWindow,
            cursor="hand2"
        )
        self.accessAnalyticsButton.pack(pady=(10, 5), anchor="e")


    def runQueryThread(self, sql, query_name):
        try:
            err = self.oracleConnector.runQuery(sql, query_name)

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
                self.databaseManager.addQueryToDB(self.oracleConnector.currentQuery)

            self.query_result_queue.put(("success", err))

            self.runQueryButton.config(state="normal")
        except Exception as e:
            self.query_result_queue.put(("error", str(e)))


    def runQuery(self):    
        self.runQueryButton.config(state="disabled")

        sql = self.query_text.get("1.0", tk.END).strip()
        queryName = self.queryNameEntry.get()

        if not sql:
            messagebox.showwarning("Empty query", "Please enter a query.")
            self.status_label.config(text="") 
            self.execTimeLabel.config(text="")
            return
        
        if not queryName or not self.validateQueryNameForRun(queryName):
            messagebox.showwarning("Empty query name", "Please enter a valid query name.")
            self.status_label.config(text="") 
            self.execTimeLabel.config(text="")
            return

        self.status_label.config(text="⏳ Running query...", fg="blue")
        self.execTimeLabel.config(text="")

        thread = threading.Thread(target=self.runQueryThread, args=(sql, queryName))
        thread.start()        

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



    def openAnalyticsWindow(self):
        if self.tl is None:
            self.tl = analytics_view.AnalyticsView(self.root, self.queryLoggerManager)
            print("Accessing analytics window\n")


    def validateQueryNameForRun(self, queryName):
        return len(queryName) > 0 and len(queryName) <= 40


    def validateQueryNameForEntry(self, queryName):
        return len(queryName) <= 40





    