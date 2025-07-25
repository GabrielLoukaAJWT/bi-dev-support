import tkinter as tk
from tkinter import ttk

import Services.analytics as analytics
import Services.database as db

class AnalyticsView:
    def __init__(self, root, loggingManager):
        self.root = tk.Toplevel(root)        
        self.root.title("Queries analytics")
        self.root.geometry("1500x800")
        self.root.attributes('-topmost', True)
        self.root.grab_set()

        self.loggerManager = loggingManager
        self.analyticsManager = analytics.AnalyticsManager(self.loggerManager)
        self.databaseManager = db.DatabaseManager()

        self.setupUI()

        self.fillQueriesTabTree()
        
        self.slowQueryLabel.bind("<Button-1>", self.selectQueryFromTreeView)

        print(F"ANALYTICS WINDOW CREATED")

        self.root.mainloop()

        

    def setupUI(self):
        self.root.configure(bg="#f7f7f7")

        self.mainFrame = tk.Frame(self.root, padx=20, pady=20, bg="#f7f7f7")        
        self.mainFrame.pack(fill="both", expand=True)

        # Title
        title = tk.Label(
            self.mainFrame,
            text="📊 Query Performance Analytics",
            font=("Arial", 20, "bold"),
            fg="#333333",
            bg="#f7f7f7"
        )
        title.pack(pady=(0, 20))

        # Summary section
        self.summaryFrame = tk.Frame(self.mainFrame, bg="#ffffff", relief="ridge", bd=2)
        self.summaryFrame.pack(fill="x", padx=10, pady=10)

        label_style = {"font": ("Arial", 11), "bg": "#ffffff", "fg": "#333"}

        self.totalQueriesLabel = tk.Label(self.summaryFrame, text=f"🧮 Total queries: {self.analyticsManager.computeTotalQueries()}", **label_style)
        self.totalQueriesLabel.pack(side="left", padx=30, pady=10)

        self.avgTimeLabel = tk.Label(self.summaryFrame, text=f"⏱ Avg Exec Time: {(self.getAverageExecTime())} sec", **label_style)
        self.avgTimeLabel.pack(side="left", padx=30, pady=10)

        self.slowQueryLabel = tk.Label(self.summaryFrame, text=f"🐢 Slowest Query: {self.getSlowestQuery()}", fg="#d9534f", bg="#ffffff", font = ("Arial", 11))
        self.slowQueryLabel.pack(side="left", padx=30, pady=10)
        self.slowQueryLabel.config(cursor="hand2")

        # Chart section
        self.chartFrame = tk.Frame(self.mainFrame, bg="#f7f7f7")
        self.chartFrame.pack(fill="both", expand=True, pady=(20, 10))

        frame_style = {"bg": "#ffffff", "padx": 10, "pady": 10, "font": ("Arial", 11, "bold"), "fg": "#444"}

        self.leftChart = tk.LabelFrame(self.chartFrame, text="Execution Time Distribution", **frame_style)
        self.leftChart.pack(side="left", fill="both", expand=True, padx=(0, 10))

        self.rightChart = tk.LabelFrame(self.chartFrame, text="Query Frequency by Hour", **frame_style)
        self.rightChart.pack(side="left", fill="both", expand=True, padx=(10, 0))

        # Table/log section
        self.tableFrame = tk.LabelFrame(self.mainFrame, text="🗂 Queries", bg="#ffffff", padx=10, pady=10, font=("Arial", 11, "bold"), height=200)
        self.tableFrame.pack(fill="both", expand=True, pady=10)

        style = ttk.Style()
        style.configure("Treeview.Heading", font=("Arial", 11, "bold"), background="#eaeaea")
        style.configure("Treeview", font=("Courier New", 10), rowheight=25)

        self.listOfQueriesViewTree = ttk.Treeview(
            self.tableFrame,
            columns=("ID", "Query", "Exec Time", "Timestamp", "Number of rows"),
            show="headings",
            selectmode="browse"
        )

        self.listOfQueriesViewTree.heading("ID", text="ID")
        self.listOfQueriesViewTree.heading("Query", text="Query")
        self.listOfQueriesViewTree.heading("Exec Time", text="Exec Time (s)")
        self.listOfQueriesViewTree.heading("Timestamp", text="Executed On")
        self.listOfQueriesViewTree.heading("Number of rows", text="Rows")

        self.listOfQueriesViewTree.column("ID", anchor="center", width=120)
        self.listOfQueriesViewTree.column("Query", anchor="w", width=400)
        self.listOfQueriesViewTree.column("Exec Time", anchor="center", width=120)
        self.listOfQueriesViewTree.column("Timestamp", anchor="center", width=180)
        self.listOfQueriesViewTree.column("Number of rows", anchor="center", width=140)

        self.listOfQueriesViewTree.pack(fill="both", expand=True)

        # Refresh button
        self.refreshButton = tk.Button(
            self.mainFrame,
            text="🔄 Refresh Analytics",
            font=("Arial", 11, "bold"),
            bg="#4CAF50",
            fg="white",
            padx=15,
            pady=8,
            relief="flat",
            cursor="hand2",
            activebackground="#45a049"
        )
        self.refreshButton.pack(pady=(10, 0))

        
            
    def fillQueriesTabTree(self):
        rows = self.analyticsManager.getRowsForTree()
        for row in rows:                    
            self.listOfQueriesViewTree.insert("", "end", values=row)


    def getSlowestQuery(self):
        id = self.analyticsManager.getQueryWithLongestExecTime()["id"] 
        name = self.analyticsManager.getQueryWithLongestExecTime()["name"]
        time = self.analyticsManager.getQueryWithLongestExecTime()["execTime"]
        return f"{name} | {time}"        


    def selectQueryFromTreeView(self, event=None):
        slowestId = self.analyticsManager.getQueryWithLongestExecTime()["id"] 

        for item_id in self.listOfQueriesViewTree.get_children():
            item = self.listOfQueriesViewTree.item(item_id)

            if item["values"][0] == slowestId: 
                self.listOfQueriesViewTree.selection_set(item_id)  
                self.listOfQueriesViewTree.focus(item_id)         
                self.listOfQueriesViewTree.see(item_id)  
                break


    def getAverageExecTime(self):
        return self.analyticsManager.computeAvgExecTime()

