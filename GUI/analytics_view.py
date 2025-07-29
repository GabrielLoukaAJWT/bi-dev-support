import queue
import threading
import tkinter as tk
from tkinter import Widget, ttk

import matplotlib
import matplotlib.pyplot as plt
import matplotlib.backends.backend_tkagg as tkplot
from  matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

import numpy as np

import Services.analytics as analytics
import Services.database as db

import GUI.query_view as query_view


class AnalyticsView:
    def __init__(self, root, loggingManager, on_close_callback=None):
        self.root = tk.Toplevel(root)        
        self.root.title("Queries analytics")
        self.root.state('zoomed')
        
        self.on_close_callback = on_close_callback

        self.loggerManager = loggingManager
        self.analyticsManager = analytics.AnalyticsManager(self.loggerManager)
        self.databaseManager = db.DatabaseManager()

        self.query_result_queue = queue.Queue()

        self.setupUI()        
        self.setupPlotSettings()
        self.getPlots()
        self.fillQueriesTabTree()
        
        self.slowQueryLabel.bind("<Button-1>", self.selectQueryFromTreeView)
        self.root.protocol("WM_DELETE_WINDOW", self.onDestroy)

        print(F"ANALYTICS WINDOW CREATED")

        self.root.mainloop()


    def onDestroy(self):
        if self.on_close_callback:
            self.on_close_callback()
        self.root.destroy()

        
    def setupUI(self):
        print(f"SETING UP THE MAIN UI")
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

        self.totalQueriesLabel = tk.Label(self.summaryFrame, text=f"🧮 Total queries: {self.analyticsManager.computeTotalQueries()}",font = ("Arial", 11))
        self.totalQueriesLabel.pack(side="left", padx=30, pady=10)

        self.avgTimeLabel = tk.Label(self.summaryFrame, text=f"⏱ Avg Exec Time: {self.analyticsManager.computeAvgExecTime()} sec", font = ("Arial", 11))
        self.avgTimeLabel.pack(side="left", padx=30, pady=10)

        self.slowQueryLabel = tk.Label(self.summaryFrame, text=f"🐢 Slowest Query: {self.getSlowestQuery()}" , bg="#fff56e", font = ("Arial", 11))
        self.slowQueryLabel.pack(side="left", padx=30, pady=10)
        self.slowQueryLabel.config(cursor="hand2")

        self.mostCommonErrorLabel = tk.Label(self.summaryFrame, text=f"⚠️ Common error: {self.analyticsManager.getMostCommonErrorLog()}" , bg="#ffa962", font = ("Arial", 11))
        self.mostCommonErrorLabel.pack(side="left", padx=30, pady=10)

        # Chart section
        frame_style = {"bg": "#ffffff", "padx": 10, "pady": 10, "font": ("Arial", 11, "bold"), "fg": "#444"}

        self.chartFrame = tk.LabelFrame(self.mainFrame, text="📈 General stats", height=500, **frame_style)
        self.chartFrame.pack(fill=tk.BOTH, expand=True, pady=(10, 10))

        self.leftChart = tk.LabelFrame(self.chartFrame, text="Correlation between number of rows and execution time", **frame_style)
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
            activebackground="#45a049",
            command=self.refreshAnalytics
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


    def refreshAnalytics(self):
        self.totalQueriesLabel.config(text=f"🧮 Total queries: {self.analyticsManager.computeTotalQueries()}")
        self.avgTimeLabel.config(text=f"⏱ Avg Exec Time: {self.analyticsManager.computeAvgExecTime()} sec")
        self.slowQueryLabel.config(text=f"🐢 Slowest Query: {self.getSlowestQuery()}")
        
        self.getPlots()
        self.fillQueriesTabTree()
        
                    
    def fillQueriesTabTree(self):
        for row in self.listOfQueriesViewTree.get_children():
            self.listOfQueriesViewTree.delete(row)

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
            return "None"


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
        self.mainFrame.after(0, self.clearUiAfterDeletion)

    
    def clearUiAfterDeletion(self):
        self.totalQueriesLabel.config(text="Number of queries: 0")
        self.avgTimeLabel.config(text="Avg Exec Time: 0 sec")
        self.slowQueryLabel.config(text="🐢 Slowest Query: None")

        for row in self.listOfQueriesViewTree.get_children():
            self.listOfQueriesViewTree.delete(row)

        for widget in self.leftChart.winfo_children():
            widget.destroy()
            
        for widget in self.rightChart.winfo_children():
            widget.destroy()


    def setupPlotSettings(self):
        plt.style.use('_mpl-gallery')

        # since matplotlib has to work on the main thread, but im using a thread for plotting (because might have some huge plots),
        # the app stays blocked (not crashing though)
        # also, im not generating a GUI specifically for the plots (for now), its just binded to the canvas
        matplotlib.use('agg')


    def threadCorrelation(self):
        try:            
            self.showExecTimeCorrelation()
            self.query_result_queue.put(("success", "canvas created"))

        except Exception as e:
            self.query_result_queue.put(("error", str(e)))
    
    
    def threadQueriesPerHour(self):
        try:            
            self.showQueriesPerHour()
            self.query_result_queue.put(("success", "canvas created"))

        except Exception as e:
            self.query_result_queue.put(("error", str(e)))


    def showExecTimeCorrelation(self):
        execTimes = self.analyticsManager.getExecTimes()
        nbRows = self.analyticsManager.getNbRowsOutput()

        self.y = np.array(execTimes)
        self.x = np.array(nbRows)

        self.fig1, self.ax1 = plt.subplots(figsize=(3, 3))
        self.ax1.scatter(self.x, self.y, color="#2196F3", edgecolor="white", alpha=0.8, linewidth=0.6)

        self.ax1.set_xlabel("Number of Rows", fontsize=12)
        self.ax1.set_ylabel("Execution Time (s)", fontsize=12)
        self.ax1.tick_params(axis='x', labelrotation=45)
        self.ax1.grid(True)

        plt.tight_layout()
        
        self.canvas1 = tkplot.FigureCanvasTkAgg(self.fig1, master=self.leftChart)
        self.canvas1.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    
    def showQueriesPerHour(self):    
        hours, counts = self.analyticsManager.getNbQueriesPerHour()

        self.fig2, self.ax2 = plt.subplots(figsize=(3, 3))
        self.ax2.bar(hours, counts, color="#4CAF50")
        self.ax2.set_xticks(hours)
        self.ax2.set_xlabel("Hour of Day", fontsize=12)
        self.ax2.set_ylabel("Number of Queries", fontsize=12)
        self.ax2.grid(axis="y", linestyle="--", alpha=0.6)

        plt.tight_layout()
        
        self.canvas2 = tkplot.FigureCanvasTkAgg(self.fig2, master=self.rightChart)
        self.canvas2.get_tk_widget().pack(fill=tk.BOTH, expand=True)


    def getPlots(self):
        print(f"CREATING THE PLOTS")
        for widget in self.leftChart.winfo_children():
            widget.destroy()
            
        for widget in self.rightChart.winfo_children():
            widget.destroy()

        thread1 = threading.Thread(target=self.threadCorrelation)
        thread1.start() 
        
        thread2 = threading.Thread(target=self.threadQueriesPerHour)
        thread2.start() 