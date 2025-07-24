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

        print(F"ANALYTICS WINDOW CREATED")

        self.root.mainloop()

        

    def setupUI(self):
        self.mainFrame = tk.Frame(self.root, padx=20, pady=20, bg="#f7f7f7")        
        self.mainFrame.pack(fill="both", expand=True)

        # Title
        title = tk.Label(self.mainFrame, text="Query Performance Analytics", font=("Arial", 18, "bold"), bg="#f7f7f7")
        title.pack(pady=(0, 20))

        # Summary section (query count, avg time, etc.)
        self.summaryFrame = tk.Frame(self.mainFrame, bg="#ffffff", relief="groove", bd=1)
        self.summaryFrame.pack(fill="x", padx=10, pady=10)

        self.totalQueriesLabel = tk.Label(self.summaryFrame, text=f"Number of queries: {self.analyticsManager.computeTotalQueries()}", font=("Arial", 11), bg="#ffffff")
        self.totalQueriesLabel.pack(side="left", padx=20, pady=10)

        self.avgTimeLabel = tk.Label(self.summaryFrame, text="Avg Exec Time: 0.00s", font=("Arial", 11), bg="#ffffff")
        self.avgTimeLabel.pack(side="left", padx=20, pady=10)

        self.slowQueryLabel = tk.Label(self.summaryFrame, text="Slowest Query: N/A", font=("Arial", 11), bg="#ffffff")
        self.slowQueryLabel.pack(side="left", padx=20, pady=10)

        # Chart section
        self.chartFrame = tk.Frame(self.mainFrame, bg="#f7f7f7")
        self.chartFrame.pack(fill="both", expand=True, pady=(20, 10))

        # Left chart area
        self.leftChart = tk.LabelFrame(self.chartFrame, text="Execution Time Distribution", bg="#ffffff", padx=10, pady=10)
        self.leftChart.pack(side="left", fill="both", expand=True, padx=(0, 10))

        # Right chart area
        self.rightChart = tk.LabelFrame(self.chartFrame, text="Query Frequency by Hour", bg="#ffffff", padx=10, pady=10)
        self.rightChart.pack(side="left", fill="both", expand=True, padx=(10, 0))

        # Table/log section
        self.tableFrame = tk.LabelFrame(self.mainFrame, text="Queries", bg="#ffffff", padx=10, pady=10)
        self.tableFrame.pack(fill="both", expand=True, pady=10)

        self.listOfQueriesViewTree = ttk.Treeview(self.tableFrame, columns=("Query", "Exec Time", "Timestamp", "Number of rows"), show="headings")
        self.listOfQueriesViewTree.heading("Query", text="Query")
        self.listOfQueriesViewTree.heading("Exec Time", text="Exec Time (s)")
        self.listOfQueriesViewTree.heading("Timestamp", text="Executed on")
        self.listOfQueriesViewTree.heading("Number of rows", text="Number of rows")

        self.listOfQueriesViewTree.column("Query", anchor="w", width=400)
        self.listOfQueriesViewTree.column("Exec Time", anchor="center", width=100)
        self.listOfQueriesViewTree.column("Timestamp", anchor="center", width=180)
        self.listOfQueriesViewTree.column("Number of rows", anchor="center", width=180)

        self.listOfQueriesViewTree.pack(fill="both", expand=True)

        # Refresh button
        self.refreshButton = tk.Button(self.mainFrame, text="Refresh Analytics", font=("Arial", 11, "bold"),
                                       bg="#4CAF50", fg="white", padx=10, pady=5)
        self.refreshButton.pack(pady=(10, 0))
        
        

    
    def fillQueriesTabTree(self):
        rows = self.analyticsManager.getRowsForTree()
        for row in rows:                    
            self.listOfQueriesViewTree.insert("", "end", values=row)

