import queue
import threading
import tkinter as tk
from tkinter import ttk
from tkinter import simpledialog, messagebox
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.backends.backend_tkagg as tkplot
import numpy as np
import mplcursors as mpl
import pyperclip
import sv_ttk

import src.Services.analytics as analytics
import src.Services.database as db
import src.Services.logging as log
import src.Services.settings as settings
import src.Services.style as style_cust
import constants as cta


class AnalyticsView:
    def __init__(self, root: tk.Tk, loggingManager: log.QueryLoggerManager, onCloseCallback=None):
        self.root = tk.Toplevel(root)        
        self.root.title("SQL Analytics")
        self.root.state('zoomed')
        
        self.onCloseCallback = onCloseCallback

        self.style = style_cust.setAnalyticsViewStyle(self.root)

        self.loggerManager = loggingManager
        self.analyticsManager = analytics.AnalyticsManager(self.loggerManager, cta.DIR_LOCAL_DB)
        self.databaseManager = db.DatabaseManager(cta.DIR_LOCAL_DB)
        self.settingsManager = settings.SettingsManager(cta.DIR_SETTINGS_GENERAL, cta.DIR_SETTINGS_ACCOUNT)

        self.plotsQueue = queue.Queue()

        self.setupUI()        
        self.setupPlotSettings()
        self.getPlots()
        self.fillQueriesTabTree()
        
        self.slowQueryLabel.bind("<Button-1>", self.selectSlowestQueryFromTree)
        self.root.protocol("WM_DELETE_WINDOW", self.onDestroy)

        print(F"ANALYTICS WINDOW CREATED")

        self.root.mainloop()


    def onDestroy(self) -> None:
        if self.onCloseCallback:
            self.onCloseCallback()
        self.root.destroy()

        
    def setupUI(self) -> None:
        print(f"SETING UP THE MAIN UI")
        # isDark = self.settingsManager.getBgTheme()
        # sv_ttk.set_theme("dark") if isDark else sv_ttk.set_theme("light")
        self.mainFrame = ttk.Frame(self.root, style="AVMainFrame.TFrame", padding=(20, 20))        
        self.mainFrame.pack(fill="both", expand=True)

        title = ttk.Label(self.mainFrame, text="📊 Query Performance Analytics", style="AVTitle.TLabel")
        title.pack(pady=(0, 20))

        self.summaryFrame = ttk.Frame(self.mainFrame, style="AVSummaryFrame.TFrame")
        self.summaryFrame.pack(fill="x", padx=10, pady=10)

        self.totalQueriesLabel = ttk.Label(self.summaryFrame, text=f"🧮 Total Queries: {self.analyticsManager.computeTotalQueries()}", style="AVTotLabel.TLabel")
        self.totalQueriesLabel.pack(side="left", padx=30, pady=10)

        self.avgTimeLabel = ttk.Label(self.summaryFrame, text=f"⏱ Avg Exec Time: {self.analyticsManager.computeAvgExecTime()} sec", style="AVExecLabel.TLabel")
        self.avgTimeLabel.pack(side="left", padx=30, pady=10)

        self.slowQueryLabel = ttk.Label(self.summaryFrame, text=f"🐢 Slowest Query: {self.getSlowestQuery()}", style="AVSlowestLabel.TLabel")
        self.slowQueryLabel.pack(side="left", padx=30, pady=10)
        self.slowQueryLabel.config(cursor="hand2")

        self.mostCommonErrorLabel = ttk.Label(self.summaryFrame, text=f"⚠️ Most Common Error: {self.analyticsManager.getMostCommonErrorLog()}", style="AVErrLabel.TLabel")
        self.mostCommonErrorLabel.pack(side="left", padx=30, pady=10)

        frame_style = {"bg": "#D3EEFF", "padx": 10, "pady": 10, "font": ("Arial", 11, "bold"), "fg": "#444"}

        self.chartFrame = tk.LabelFrame(self.mainFrame, text="📈 General Stats", height=500, **frame_style)
        self.chartFrame.pack(fill=tk.BOTH, expand=True, pady=(10, 10))

        self.leftChart = tk.LabelFrame(self.chartFrame, text="Correlation Between Number of Rows and Execution Time", **frame_style)
        self.leftChart.pack(side="left", fill="both", expand=True, padx=(0, 10))

        self.rightChart = tk.LabelFrame(self.chartFrame, text="Query Frequency by Hour Today", **frame_style)
        self.rightChart.pack(side="left", fill="both", expand=True, padx=(10, 0))

        self.tableFrame = tk.LabelFrame(self.mainFrame, text="🗂 Queries", **frame_style , height=100)
        self.tableFrame.pack(fill="both", expand=True, pady=10)

        self.listOfQueriesViewTree = ttk.Treeview(
            self.tableFrame,
            columns=("ID ↕", "Query ↕", "Exec Time ↕", "User ↕", "Timestamp ↕", "Number of rows ↕"),
            show="headings",
            selectmode="browse"
            # style="AVTreeview.Heading"
        )

        for col in self.listOfQueriesViewTree["columns"]:
            self.listOfQueriesViewTree.heading(
                col, 
                text=col, 
                command=lambda _col=col: self.treeview_sort_column(self.listOfQueriesViewTree, _col, False)
            )



        self.listOfQueriesViewTree.column("ID ↕", anchor="center", width=120)
        self.listOfQueriesViewTree.column("Query ↕", anchor="w", width=400)
        self.listOfQueriesViewTree.column("Exec Time ↕", anchor="center", width=120)
        self.listOfQueriesViewTree.column("User ↕", anchor="center", width=120)
        self.listOfQueriesViewTree.column("Timestamp ↕", anchor="center", width=180)
        self.listOfQueriesViewTree.column("Number of rows ↕", anchor="center", width=140)

        self.listOfQueriesViewTree.pack(fill="both", expand=True)

        self.menuPopup = tk.Menu(self.root, tearoff=0)
        self.menuPopup.add_command(label="Edit query name", command=self.editNamePopup)
        self.menuPopup.add_command(label="Copy code to clipboard", command=self.copyCodeToClipboard)
        self.menuPopup.add_separator()
        self.menuPopup.add_command(label="Delete query from DB", command=self.deleteByID)
        
        self.listOfQueriesViewTree.bind("<Button-3>", self.query_selection_popup)


        self.refreshButton = ttk.Button(
            self.mainFrame,
            text="🔄 Refresh Analytics",
            style="AVAction.TButton",
            cursor="hand2",
            command=self.refreshAnalytics
        )
        self.refreshButton.pack(pady=(10, 0))

        self.deleteDbButton = ttk.Button(
            self.mainFrame, 
            text="🗑️ Delete local DB",
            cursor="hand2",
            style="AVClear.TButton",                                        
            command=self.deleteDB
        )
        self.deleteDbButton.pack(pady=(10, 0), anchor="e")


    def refreshAnalytics(self) -> None:
        self.totalQueriesLabel.config(text=f"🧮 Total Queries: {self.analyticsManager.computeTotalQueries()}")
        self.avgTimeLabel.config(text=f"⏱ Avg Exec Time: {self.analyticsManager.computeAvgExecTime()} sec")
        self.slowQueryLabel.config(text=f"🐢 Slowest Query: {self.getSlowestQuery()}")
        self.mostCommonErrorLabel.config(text=f"⚠️ Most Common Error: {self.analyticsManager.getMostCommonErrorLog()}")
        
        self.getPlots()
        self.fillQueriesTabTree()
        
                    
    def fillQueriesTabTree(self) -> None:
        for row in self.listOfQueriesViewTree.get_children():
            self.listOfQueriesViewTree.delete(row)

        rows = self.analyticsManager.getRowsForTree()

        for row in rows:                    
            self.listOfQueriesViewTree.insert("", "end", values=row)        


    def getSlowestQuery(self) -> str:
        query = self.analyticsManager.getQueryWithLongestExecTime()

        if query:
            name = query["name"]
            time = query["execTime"]
            
            return f"{name} | {time}"        
        else:
            return "None"


    def selectSlowestQueryFromTree(self, event=None) -> None:
        slowestId = self.analyticsManager.getQueryWithLongestExecTime()["id"] 

        for item_id in self.listOfQueriesViewTree.get_children():
            item = self.listOfQueriesViewTree.item(item_id)

            if item["values"][0] == slowestId: 
                self.listOfQueriesViewTree.selection_set(item_id)  
                self.listOfQueriesViewTree.focus(item_id)         
                self.listOfQueriesViewTree.see(item_id)  
                break
    

    def deleteDB(self) -> None:
        self.databaseManager.clearDB()
        self.mainFrame.after(0, self.clearUiAfterDeletion)

    
    def clearUiAfterDeletion(self) -> None:
        self.totalQueriesLabel.config(text="🧮 Total Queries: 0")
        self.avgTimeLabel.config(text="⏱ Avg Exec Time: 0 sec")
        self.slowQueryLabel.config(text="🐢 Slowest Query: None")

        for row in self.listOfQueriesViewTree.get_children():
            self.listOfQueriesViewTree.delete(row)

        for widget in self.leftChart.winfo_children():
            widget.destroy()
            
        for widget in self.rightChart.winfo_children():
            widget.destroy()


    def setupPlotSettings(self) -> None:
        plt.style.use('_mpl-gallery')

        # since matplotlib has to work on the main thread, but im using a thread for plotting (because might have some huge plots),
        # the app stays blocked (not crashing though)
        # also, im not generating a GUI specifically for the plots (for now), its just binded to the canvas
        matplotlib.use('agg')


    def threadCorrelation(self) -> None:
        try:            
            self.showExecTimeCorrelation()
            self.plotsQueue.put(("success", "canvas created"))

        except Exception as e:
            self.plotsQueue.put(("error", str(e)))
    
    
    def threadQueriesPerHour(self) -> None:
        try:            
            self.showQueriesPerHour()
            self.plotsQueue.put(("success", "canvas created"))

        except Exception as e:
            self.plotsQueue.put(("error", str(e)))


    def showExecTimeCorrelation(self) -> None:
        execTimes = self.analyticsManager.getExecTimes()
        nbRows = self.analyticsManager.getNbRowsOutput()

        self.y = np.array(execTimes)
        self.x = np.array(nbRows)

        self.fig1, self.ax1 = plt.subplots(figsize=(3, 3))
        self.scatter = self.ax1.scatter(self.x, self.y, color="#2196F3", edgecolor="white", alpha=0.8, linewidth=0.6)

        self.ax1.set_xlabel("Number of Rows", fontsize=12)
        self.ax1.set_ylabel("Execution Time (s)", fontsize=12)
        self.ax1.tick_params(axis='x', labelrotation=45)
        self.ax1.grid(True)

        cursor = mpl.cursor(self.scatter, hover=mpl.HoverMode.Transient)
        cursor.connect('add', self.update_annot)

        plt.tight_layout()
        
        self.canvas1 = tkplot.FigureCanvasTkAgg(self.fig1, master=self.leftChart)
        self.canvas1.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    
    def update_annot(self, sel) -> None:    
        x, y = sel.target
        ind = sel.index
        
        if x and y and ind:
            sel.annotation.set_text(f'{self.x[ind]} rows in {self.y[ind]} s')
        else:
            return

    
    def showQueriesPerHour(self) -> None:    
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
    


    def getPlots(self) -> None:
        print(f"CREATING THE PLOTS")
        for widget in self.leftChart.winfo_children():
            widget.destroy()
            
        for widget in self.rightChart.winfo_children():
            widget.destroy()

        thread1 = threading.Thread(target=self.threadCorrelation)
        thread1.start() 
        
        thread2 = threading.Thread(target=self.threadQueriesPerHour)
        thread2.start() 


    def treeview_sort_column(self, tv: ttk.Treeview, col:str, reverse:bool) -> None:
        def try_num(val: str):
            try:
                return float(val)
            except ValueError:
                return val.lower() if isinstance(val, str) else val

        sortedList = [(try_num(tv.set(k, col)), k) for k in tv.get_children('')]
        sortedList.sort(reverse=reverse)

        for index, (val, k) in enumerate(sortedList):
            tv.move(k, '', index)

        tv.heading(col, command=lambda: self.treeview_sort_column(tv, col, not reverse))

        

    def query_selection_popup(self, event) -> None:
        item = self.listOfQueriesViewTree.identify_row(event.y)
        item_id = self.listOfQueriesViewTree.identify_row(event.y)

        self.listOfQueriesViewTree.selection_remove(self.listOfQueriesViewTree.selection())
        self.listOfQueriesViewTree.selection_set(item_id)
        self.listOfQueriesViewTree.focus(item_id)
        
        try:
            self.menuPopup.tk_popup(event.x_root, event.y_root)
        finally:
            self.menuPopup.grab_release()


    def editNamePopup(self) -> None:
        selectedQuery = self.listOfQueriesViewTree.focus()

        if selectedQuery:
            currentQueryName = self.listOfQueriesViewTree.item(selectedQuery, "values")[1]
            currentQueryID = self.listOfQueriesViewTree.item(selectedQuery, "values")[0]

            newName = simpledialog.askstring(
                "",
                "New name (max 40 chars)",
                initialvalue=currentQueryName
            )

            if newName and len(newName) <= 40 and newName.strip():
                self.databaseManager.editQueryName(currentQueryID, newName)
                self.listOfQueriesViewTree.set(selectedQuery, 
                                               column=self.listOfQueriesViewTree["columns"][1], 
                                               value=newName.strip()
                                            )
            else:
                messagebox.showinfo("No change", "Query name was not changed.")
        else:
            return
        


    def deleteByID(self) -> None:
        selectedQuery = self.listOfQueriesViewTree.focus()

        if selectedQuery:
            currentQueryID = self.listOfQueriesViewTree.item(selectedQuery, "values")[0]
            if self.databaseManager.deleteQueryByID(currentQueryID):
                self.listOfQueriesViewTree.delete(selectedQuery)
                self.refreshAnalytics()
            else:
                messagebox.showinfo("No change", "Failed to delete query.")        
        else:
            return
        

    def copyCodeToClipboard(self) -> None:
        selectedQuery = self.listOfQueriesViewTree.focus()

        if selectedQuery:
            currentQueryID = self.listOfQueriesViewTree.item(selectedQuery, "values")[0]
            code = self.databaseManager.getQueryById(currentQueryID)["code"]
            pyperclip.copy(code)
                   
        else:
            return