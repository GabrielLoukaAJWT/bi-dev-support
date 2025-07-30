import threading
import oracledb
import tkinter as tk
from tkinter import scrolledtext
from tkinter import messagebox
import queue

import Services.db_connection as cnx
import Services.logging as log
import Services.database as db
import GUI.analytics_view as analytics_view


class QueryView:
    def __init__(self, root, oracleConnector: cnx.OracleConnector):        
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
        self.root.configure(bg="#f7f7f7")
        self.frame = tk.Frame(self.root, padx=20, pady=20, bg="#f7f7f7")
        self.frame.pack(fill="both", expand=True)

        headingFont = ("Arial", 14, "bold")
        labelFont = ("Arial", 12)
        inputFont = ("Courier New", 11)
        actionBtnFont = ("Arial", 12, "bold")
        gray = "#f7f7f7"

        tk.Label(
            self.frame,
            text="Enter SQL Query",
            font=headingFont,
            bg=gray,
            fg="#333"
        ).pack(pady=(0, 15))

        queryInputFrame = tk.Frame(self.frame, bg=gray)
        queryInputFrame.pack(fill="x", pady=(10, 20))

        tk.Label(
            queryInputFrame,
            text="Query Name",
            font=labelFont,
            anchor="w",
            bg=gray,
            fg="#444"
        ).pack(fill="x", padx=5, pady=(0, 5))

        self.queryNameEntry = tk.Entry(
            queryInputFrame,
            font=inputFont,
            relief="solid",
            bd=1,
            validate="key",
            validatecommand=((self.root.register(self.validateQueryNameForEntry)), '%P')
        )
        self.queryNameEntry.pack(fill="x", padx=5, ipady=5)

        tk.Label(
            queryInputFrame,
            text="SQL Query",
            font=labelFont,
            anchor="w",
            bg=gray,
            fg="#444"
        ).pack(fill="x", padx=5, pady=(15, 5))

        self.queryText = tk.Text(
            queryInputFrame,
            height=12,
            font=inputFont,
            relief="solid",
            bd=1
        )
        self.queryText.pack(fill="x", padx=5, pady=(0, 10))

        self.runQueryButton = tk.Button(
            self.frame,
            text="▶ Run Query",
            font=actionBtnFont,
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

        self.outputBox = scrolledtext.ScrolledText(
            self.frame,
            height=12,
            wrap=tk.NONE,
            font=("Courier New", 10),
            relief="solid",
            bd=1
        )
        self.outputBox.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))

        xScroll = tk.Scrollbar(self.frame, orient=tk.HORIZONTAL, command=self.outputBox.xview)
        xScroll.pack(side=tk.BOTTOM, fill=tk.X)
        self.outputBox.config(xscrollcommand=xScroll.set)

        self.statusLabel = tk.Label(
            self.frame,
            text="",
            font=("Arial", 10),
            fg="red",
            bg=gray
        )
        self.statusLabel.pack(pady=(10, 2))

        self.execTimeLabel = tk.Label(
            self.frame,
            text="",
            font=("Arial", 14),
            fg="gray",
            bg=gray
        )
        self.execTimeLabel.pack(pady=(0, 15))

        self.areLogsShown = False
        self.toggleLogsBtn = tk.Button(
            self.frame,
            text="🪵 Show Logs",
            font=("Arial", 10),
            command=self.toggleLogs,
            bg="#eeeeee",
            fg="#333",
            relief="flat",
            cursor="hand2"
        )
        self.toggleLogsBtn.pack(pady=(10, 0))

        self.logsFrame = tk.Frame(self.frame, bg="#f0f0f0", relief="groove", bd=1)
        self.logsBox = scrolledtext.ScrolledText(
            self.logsFrame,
            height=10,
            width=100,
            state="disabled",
            font=("Courier New", 10),
            wrap="word"
        )
        self.logsBox.pack(padx=10, pady=10, fill="both", expand=True)

        self.accessAnalyticsButton = tk.Button(
            self.frame,
            text="📈 Access Analytics",
            font=actionBtnFont,
            bg="#4CAF50",
            fg="white",
            activebackground="#45a049",
            padx=15,
            pady=8,
            command=self.openAnalyticsWindow,
            cursor="hand2"
        )
        self.accessAnalyticsButton.pack(pady=(10, 5), anchor="e")


    def runQueryThread(self, sql: str, queryName: str) -> None:
        self.runQueryButton.config(state="disabled")
        try:
            err = self.oracleConnector.runQuery(sql, queryName)

            if err:              
                self.statusLabel.config(text=err, fg="red")  
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

        self.statusLabel.config(text="⌛️ Running query...", fg="blue")
        self.execTimeLabel.config(text="")

        thread = threading.Thread(target=self.runQueryThread, args=(sql, queryName))
        thread.start()        

        self.displayLogsOnToggle()


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
            self.logsFrame.pack_forget()
            self.toggleLogsBtn.config(text="Show Logs")
        else:
            self.displayLogsOnToggle()
            self.logsFrame.pack(fill="both", expand=True, pady=(5, 10))
            self.toggleLogsBtn.config(text="Hide Logs")

        self.areLogsShown = not self.areLogsShown


    def displayLogsOnToggle(self) -> None:
        try:
            with open("./logs/queries.log", "r", encoding="utf-8") as f:
                log_content = f.read()
        except FileNotFoundError:
            log_content = "No log file found."

        self.logsBox.config(state="normal")
        self.logsBox.delete("1.0", "end")
        self.logsBox.insert("1.0", log_content)
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





    