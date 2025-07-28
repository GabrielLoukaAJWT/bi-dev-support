import queue
import threading
import tkinter as tk
from tkinter import ttk

import matplotlib
import matplotlib.pyplot as plt
import matplotlib.backends.backend_tkagg as tkplot
from  matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

import numpy as np

import Services.analytics as analytics
import Services.database as db

class AnalyticsView:
    def __init__(self, root, loggingManager):
        self.root = tk.Toplevel(root)        
        self.root.title("Queries analytics")
        self.root.geometry("1500x800")
        # self.root.attributes('-topmost', True)
        # self.root.grab_set()

        self.loggerManager = loggingManager
        self.analyticsManager = analytics.AnalyticsManager(self.loggerManager)
        self.databaseManager = db.DatabaseManager()

        self.setupUI()

        self.fillQueriesTabTree()

        self.setupPlot()
        self.getPlots()
        
        self.slowQueryLabel.bind("<Button-1>", self.selectQueryFromTreeView)

        self.query_result_queue = queue.Queue()

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

        self.slowQueryLabel = tk.Label(self.summaryFrame, text=f"🐢 Slowest Query: {self.getSlowestQuery()}" , bg="#ffffff", font = ("Arial", 11))
        self.slowQueryLabel.pack(side="left", padx=30, pady=10)
        self.slowQueryLabel.config(cursor="hand2")

        self.mostCommonErrorLabel = tk.Label(self.summaryFrame, text=f"⚠️ Common error: {self.getMostCommonError()}" , bg="#ffa962", font = ("Arial", 11))
        self.mostCommonErrorLabel.pack(side="left", padx=30, pady=10)

        # Chart section
        self.chartFrame = tk.Frame(self.mainFrame, bg="#f7f7f7", height=500)
        self.chartFrame.pack(fill="both", expand=True, pady=(20, 10))

        frame_style = {"bg": "#ffffff", "padx": 10, "pady": 10, "font": ("Arial", 11, "bold"), "fg": "#444"}

        self.leftChart = tk.LabelFrame(self.chartFrame, text="Execution Time Distribution", **frame_style)
        self.leftChart.pack(side="left", fill="both", expand=True, padx=(0, 10))

        self.rightChart = tk.LabelFrame(self.chartFrame, text="Query Frequency by Hour", **frame_style)
        self.rightChart.pack(side="left", fill="both", expand=True, padx=(10, 0))

        # Table/log section
        self.tableFrame = tk.LabelFrame(self.mainFrame, text="🗂 Queries", bg="#ffffff", padx=10, pady=10, font=("Arial", 11, "bold"), height=100)
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

        self.deleteDbButton = tk.Button(
            self.mainFrame,
            text="🗑️ Delete Local DB",
            font=("Arial", 10, "bold"),
            bg="#f44336",
            fg="white",
            activebackground="#d32f2f",
            padx=12,
            pady=6,
            cursor="hand2",
            command=self.deleteDB
        )
        self.deleteDbButton.pack(pady=(10, 0), anchor="e")


                    
    def fillQueriesTabTree(self):
        rows = self.analyticsManager.getRowsForTree()
        for row in rows:                    
            self.listOfQueriesViewTree.insert("", "end", values=row)        


    def getSlowestQuery(self):
        query = self.analyticsManager.getQueryWithLongestExecTime()
        if query:
            id = query["id"] 
            name = query["name"]
            time = query["execTime"]
            return f"{name} | {time}"        
        else:
            return ""


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
    

    def getMostCommonError(self):
        return self.analyticsManager.getMostCommonErrorLog()
    

    def deleteDB(self):
        self.databaseManager.clearDB()
        self.mainFrame.after(0, self.updateUI)

    
    def updateUI(self):
        self.totalQueriesLabel.config(text="Number of queries: 0")
        self.avgTimeLabel.config(text="Avg Exec Time: 0.00s")
        self.slowQueryLabel.config(text="🐢 Slowest Query: None")

        for row in self.listOfQueriesViewTree.get_children():
            self.listOfQueriesViewTree.delete(row)


    def setupPlot(self):
        plt.style.use('_mpl-gallery')
        matplotlib.use('agg')


    def plotThread(self):
        try:

            x = 0.5 + np.arange(8)
            y = [4.8, 5.5, 3.5, 4.6, 6.5, 6.6, 2.6, 3.0]

            # plot
            fig, ax = plt.subplots()

            ax.bar(x, y, width=1, edgecolor="white", linewidth=0.7)

            ax.set(xlim=(0, 8), xticks=np.arange(1, 8),
                ylim=(0, 8), yticks=np.arange(1, 8))
            
            canvas = tkplot.FigureCanvasTkAgg(fig, master=self.leftChart)
            canvas._tkcanvas.pack(fill=tk.BOTH, expand=True)
        
            self.query_result_queue.put(("success", "canvas created"))

        except Exception as e:
            self.query_result_queue.put(("error", str(e)))


    def getPlots(self):
        thread = threading.Thread(target=self.plotThread)
        thread.start() 