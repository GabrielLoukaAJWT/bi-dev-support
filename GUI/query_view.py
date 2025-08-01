import oracledb
import threading
from tkinter import ttk
import tkinter as tk
from tkinter import scrolledtext
from tkinter import messagebox
import queue

import Services.db_connection as cnx
import Services.logging as log
import Services.database as db
import GUI.analytics_view as analytics_view


class QueryView:
    def __init__(self, root: tk.Tk, oracleConnector: cnx.OracleConnector):        
        self.root = root        
        self.analyticsPage = None

        self.oracleConnector = oracleConnector
        self.queryLoggerManager = log.QueryLoggerManager()   
        self.databaseManager = db.DatabaseManager()
        
        self.query_result_queue = queue.Queue()

        # self.queryLoggerManager.clearLogsFile()
        self.setupUI()
        self.enableButtonAfterAnalyticsWindowClosed()

        print(F"QUERY VIEW CREATED")


    def setupUI(self) -> None:
        self.root.title("SQL Companion")
        self.root.configure(bg="#f7f7f7")

        if not hasattr(self, "frame"):
            self.frame = ttk.Frame(self.root, padding=16)
            self.frame.pack(fill="both", expand=True)
        else:
            self.frame.configure(padding=16)
            self.frame.pack(fill="both", expand=True)

        style = ttk.Style(self.root)
        style.theme_use("default")
        style.configure("Card.TFrame", background="#ffffff", relief="flat")
        style.configure("Header.TLabel", font=("Segoe UI", 14, "bold"), background="#f7f7f7", foreground="#222")
        style.configure("Label.TLabel", font=("Segoe UI", 11), background="#f7f7f7", foreground="#444")
        style.configure("Status.TLabel", font=("Segoe UI", 10), background="#f7f7f7", foreground="red")
        style.configure("Action.TButton", font=("Segoe UI", 11, "bold"))
        style.map("Action.TButton",
                background=[("active", "#1976D2"), ("!disabled", "#2196F3")],
                foreground=[("!disabled", "white")])

        main_pane = ttk.PanedWindow(self.frame, orient="horizontal")
        main_pane.pack(fill="both", expand=True)

        # Left card: query input
        left_card = ttk.Frame(main_pane, style="Card.TFrame", padding=16)
        main_pane.add(left_card, weight=1)

        ttk.Label(left_card, text="Enter SQL Query", style="Header.TLabel").grid(row=0, column=0, sticky="w")

        # Query name
        ttk.Label(left_card, text="Query Name", style="Label.TLabel").grid(row=1, column=0, sticky="w", pady=(12, 2))
        self.queryNameEntry = ttk.Entry(left_card, font=("Courier New", 11))
        vcmd = (self.root.register(self.validateQueryNameForEntry), "%P")
        self.queryNameEntry.configure(validate="key", validatecommand=vcmd)
        self.queryNameEntry.grid(row=2, column=0, sticky="ew", ipady=6)

        # SQL text
        ttk.Label(left_card, text="SQL Query", style="Label.TLabel").grid(row=3, column=0, sticky="w", pady=(12, 2))
        self.queryText = tk.Text(left_card, height=10, font=("Courier New", 11), relief="solid", bd=1, wrap="none")
        q_scroll_y = ttk.Scrollbar(left_card, orient="vertical", command=self.queryText.yview)
        q_scroll_x = ttk.Scrollbar(left_card, orient="horizontal", command=self.queryText.xview)
        self.queryText.configure(yscrollcommand=q_scroll_y.set, xscrollcommand=q_scroll_x.set)
        self.queryText.grid(row=4, column=0, sticky="nsew")
        q_scroll_y.grid(row=4, column=1, sticky="ns")
        q_scroll_x.grid(row=5, column=0, sticky="ew", pady=(2, 0))

        # Action bar (Run + Analytics)
        action_frame = ttk.Frame(left_card)
        action_frame.grid(row=6, column=0, sticky="ew", pady=(12, 0))
        self.runQueryButton = ttk.Button(action_frame, text="▶ Run Query", style="Action.TButton", command=self.runQuery)
        self.runQueryButton.pack(side="left")
        self.accessAnalyticsButton = ttk.Button(action_frame, text="📈 Access Analytics", style="Action.TButton", command=self.openAnalyticsWindow)
        self.accessAnalyticsButton.pack(side="left", padx=(8, 0))

        # Footer: status + exec time
        footer = ttk.Frame(left_card)
        footer.grid(row=7, column=0, sticky="ew", pady=(12, 0))
        self.statusLabel = ttk.Label(footer, text="", style="Status.TLabel")
        self.statusLabel.pack(side="left", fill="x", expand=True)
        self.execTimeLabel = ttk.Label(footer, text="", font=("Segoe UI", 14), foreground="#666")
        self.execTimeLabel.pack(side="right")

        # Configure expansion
        left_card.rowconfigure(4, weight=1)
        left_card.columnconfigure(0, weight=1)

        # Right card: output + logs
        right_card = ttk.Frame(main_pane, style="Card.TFrame", padding=16)
        main_pane.add(right_card, weight=2)

        ttk.Label(right_card, text="Query Output / Logs", style="Header.TLabel").grid(row=0, column=0, sticky="w")

        # Output box
        self.outputBox = scrolledtext.ScrolledText(right_card, height=12, wrap="none", font=("Courier New", 10), relief="solid", bd=1)
        self.outputBox.grid(row=1, column=0, sticky="nsew", pady=(4, 2))
        xScroll = ttk.Scrollbar(right_card, orient="horizontal", command=self.outputBox.xview)
        self.outputBox.configure(xscrollcommand=xScroll.set)
        xScroll.grid(row=2, column=0, sticky="ew")

        # Logs toggle
        toggle_frame = ttk.Frame(right_card)
        toggle_frame.grid(row=3, column=0, sticky="ew", pady=(12, 4))
        self.toggleLogsBtn = ttk.Button(toggle_frame, text="🪵 Show Logs", command=self.toggleLogs)
        self.toggleLogsBtn.pack(side="left")

        # Logs container (hidden initially)
        self.logsContainer = ttk.Frame(right_card, padding=4)
        self.logsContainer.grid(row=4, column=0, sticky="nsew")
        self.logsContainer.grid_remove()  # start hidden

        self.logsBox = scrolledtext.ScrolledText(
            self.logsContainer,
            height=10,
            font=("Courier New", 10),
            wrap="word",
            state="disabled",
            relief="solid",
            bd=1
        )
        self.logsBox.pack(fill="both", expand=True)

        right_card.rowconfigure(1, weight=1)
        right_card.rowconfigure(4, weight=1)
        right_card.columnconfigure(0, weight=1)

        # Keep internal flag
        self.areLogsShown = False



    def runQueryThread(self, sql: str, queryName: str) -> None:
        self.runQueryButton.config(state="disabled")
        try:
            err = self.oracleConnector.runQuery(sql, queryName)

            if err:              
                print(f"ERRROR BAD QUERY {err}")

                self.statusLabel.config(text=err, foreground="red")  
                self.execTimeLabel.config(text="")
                self.queryLoggerManager.addLog("error", self.oracleConnector.currentQuery, err)
            else:
                self.statusLabel.config(text="") 
                text = f"{len(self.oracleConnector.currentQuery.rows)} rows in {str(self.oracleConnector.currentQuery.execTime)}"
                self.execTimeLabel.config(text=text)

                self.displayQueryOutput()

                self.queryLoggerManager.addLog("info", self.oracleConnector.currentQuery, err)
                self.databaseManager.addQueryToDB(self.oracleConnector.currentQuery)
                self.query_result_queue.put(("success", err))

            self.displayLogs()

            self.runQueryButton.config(state="normal")

        except Exception as e:
            self.query_result_queue.put(("error", str(e)))


    def runQuery(self) -> None:            
        sql = self.queryText.get("1.0", tk.END).strip()
        queryName = self.queryNameEntry.get()

        if not sql:
            messagebox.showwarning("Empty query", "Please enter a query.")
            self.statusLabel.config(text="") 
            self.execTimeLabel.config(text="")
            return
        
        if not queryName or not self.validateQueryNameForRun(queryName):
            messagebox.showwarning("Empty query name", "Please enter a valid query name.")
            self.statusLabel.config(text="") 
            self.execTimeLabel.config(text="")
            return

        self.statusLabel.config(text="⌛️ Running query...", foreground="blue")
        self.execTimeLabel.config(text="")

        thread = threading.Thread(target=self.runQueryThread, args=(sql, queryName))
        thread.start()            
        

    def displayQueryOutput(self) -> None:
        self.outputBox.delete("1.0", tk.END)

        if not self.oracleConnector.currentQuery.rows:
            self.outputBox.insert(tk.END, "No results found.")
            return
        
        formatted = self.formatRows(
            self.oracleConnector.currentQuery.columns, 
            self.oracleConnector.currentQuery.rows)
        
        self.outputBox.insert(tk.END, formatted)


    def calculateColumnWidths(self, columns: list, rows: list) -> list[int]:
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
    
    
    def formatRowSafely(self, row: str, colWidths: list[int]) -> str:
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
            formatted.append(val_str.ljust(colWidths[i]))

        return " | ".join(formatted)

        
    def formatRows(self, columns: list, rows: list) -> str:
        col_widths = self.calculateColumnWidths(columns, rows)

        header = " | ".join(col.ljust(col_widths[i]) for i, col in enumerate(columns))
        separator = "-+-".join("-" * w for w in col_widths)

        lines = [header, separator]

        for row in rows:
            lines.append(self.formatRowSafely(row, col_widths))

        return "\n".join(lines)
    

    def toggleLogs(self) -> None:
        if self.areLogsShown:
            self.logsContainer.grid_remove()
            self.toggleLogsBtn.config(text="🪵 Show Logs")
        else:
            self.logsContainer.grid()
            self.toggleLogsBtn.config(text="🪵 Hide Logs")
        self.areLogsShown = not self.areLogsShown
        self.displayLogs()


    def displayLogs(self) -> None:
        logs = self.queryLoggerManager.getQueriesFromFile("./logs/queries.log")

        self.logsBox.config(state="normal")
        self.logsBox.delete("1.0", "end")

        for log_entry in logs:  # newest last
            self.logsBox.insert(tk.END, f"{log_entry}\n\n")

        self.logsBox.see(tk.END)
        self.logsBox.config(state="disabled")


    def openAnalyticsWindow(self) -> None:
        self.accessAnalyticsButton.config(state="disabled")
        self.analyticsPage = analytics_view.AnalyticsView(self.root, self.queryLoggerManager, onCloseCallback=self.enableButtonAfterAnalyticsWindowClosed)


    def enableButtonAfterAnalyticsWindowClosed(self) -> None:
        self.accessAnalyticsButton.config(state="normal")


    def validateQueryNameForRun(self, queryName: str) -> bool:
        return len(queryName) > 0 and len(queryName) <= 40


    def validateQueryNameForEntry(self, queryName) -> bool:
        return len(queryName) <= 40





    