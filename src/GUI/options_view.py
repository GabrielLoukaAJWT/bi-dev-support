import tkinter as tk
from tkinter import ttk



class OptionsWindow:
    def __init__(self, onCloseCallback=None):
        self.root = tk.Tk()
        self.root.title("General options")
        self.root.geometry("500x300")

        self.onCloseCallback = onCloseCallback

        self.root.protocol("WM_DELETE_WINDOW", self.onDestroy)

        self.setupUI()


    def onDestroy(self) -> None:
        if self.onCloseCallback:
            self.onCloseCallback()
        self.root.destroy()


    def setupUI(self) -> None:
        self.style = ttk.Style(self.root)
        self.style.theme_use("default")
        self.style.configure("MainFrame.TFrame", background="#cccccc", relief="flat")

        self.mainFrame = ttk.Frame(self.root, padding=16, style="MainFrame.TFrame")
        self.mainFrame.pack(fill="both", expand=True)

        self.notebook = ttk.Notebook(self.mainFrame)
        self.notebook.pack(expand=True, fill="both")

        self.generalTab = ttk.Frame(self.notebook)
        self.accTab = ttk.Frame(self.notebook)
        self.queriesTab = ttk.Frame(self.notebook)
        self.analyticsTab = ttk.Frame(self.notebook)
        
        self.setupGeneraTabUI()
        self.setupAccountTabUI()
        self.setupQueriesTabUI()
        self.setupAnalyticsTabUI()

        self.notebook.add(self.generalTab, text="General")
        self.notebook.add(self.accTab, text="Account")
        self.notebook.add(self.queriesTab, text="Queries")
        self.notebook.add(self.analyticsTab, text="Analytics")


    
    def setupGeneraTabUI(self) -> None:
        container = ttk.Frame(self.generalTab, padding=16)
        container.pack(fill="both", expand=True)

        ttk.Label(
            container,
            text="Appearance",
            font=("Segoe UI", 10, "bold")
        ).grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 8))

        ttk.Label(container, text="Theme:").grid(row=1, column=0, sticky="w")
        self.theme_var = tk.StringVar(value="System")
        theme_box = ttk.Combobox(
            container,
            textvariable=self.theme_var,
            values=["System", "Light", "Dark"],
            state="readonly",
            width=14
        )
        theme_box.grid(row=1, column=1, sticky="ew", padx=(8, 0))
        theme_box.configure(font=("Segoe UI", 9))

        container.rowconfigure(2, minsize=12)

        ttk.Label(
            container,
            text="Behavior",
            font=("Segoe UI", 10, "bold")
        ).grid(row=3, column=0, columnspan=2, sticky="w", pady=(0, 8))

        self.show_logs_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(
            container,
            text="Show logs by default",
            variable=self.show_logs_var
        ).grid(row=4, column=0, columnspan=2, sticky="w", pady=(0, 4))

        container.columnconfigure(0, weight=1)
        container.columnconfigure(1, weight=2)





    def setupAccountTabUI(self) -> None:
        pass
    
    
    def setupQueriesTabUI(self) -> None:
        pass
    
    
    def setupAnalyticsTabUI(self) -> None:
        pass