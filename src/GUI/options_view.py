import tkinter as tk
from tkinter import ttk
import sv_ttk

import src.Services.settings as settings
import constants as cta


class OptionsWindow:
    def __init__(self, root: tk.Tk, onCloseCallback=None):
        self.root = tk.Toplevel(root)
        self.root.title("Options")
        self.root.geometry("500x300")

        self.onCloseCallback = onCloseCallback

        self.settingsManager = settings.SettingsManager(cta.DIR_SETTINGS_GENERAL, cta.DIR_SETTINGS_ACCOUNT)

        self.root.protocol("WM_DELETE_WINDOW", self.onDestroy)

        self.setupUI()


    def onDestroy(self) -> None:
        if self.onCloseCallback:
            self.onCloseCallback()
        self.root.destroy()



    def setupUI(self) -> None:        
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
        self.generalSettingsTabContainer = ttk.Frame(self.generalTab, padding=16)
        self.generalSettingsTabContainer.pack(fill="both", expand=True)

        ttk.Label(
            self.generalSettingsTabContainer,
            text="Appearance",
            font=("Segoe UI", 10, "bold")
        ).grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 8))

        ttk.Label(self.generalSettingsTabContainer, text="Theme:").grid(row=1, column=0, sticky="w")
        self.theme_var = tk.StringVar(value="System")
        self.theme_box = ttk.Combobox(
            self.generalSettingsTabContainer,
            textvariable=self.theme_var,
            values=["System", "Light", "Dark"],
            state="readonly",
            width=14
        )
        

        ttk.Button(self.generalSettingsTabContainer, text="Apply", 
                   command=self.applyTheme).grid(row=20, column=5, sticky="w")


        self.theme_box.grid(row=1, column=1, sticky="ew", padx=(8, 0))
        self.theme_box.configure(font=("Segoe UI", 9))

        self.generalSettingsTabContainer.rowconfigure(2, minsize=12)

        self.generalSettingsTabContainer.columnconfigure(0, weight=1)
        self.generalSettingsTabContainer.columnconfigure(1, weight=2)


    def applyTheme(self) -> None:
        selectedTheme = self.theme_box.get()
        self.settingsManager.editDarkTheme(selectedTheme)
        sv_ttk.set_theme("dark") if selectedTheme == "Dark" else sv_ttk.set_theme("light")



    def setupAccountTabUI(self) -> None:
        pass
    
    
    def setupQueriesTabUI(self) -> None:
        pass
    
    
    def setupAnalyticsTabUI(self) -> None:
        pass