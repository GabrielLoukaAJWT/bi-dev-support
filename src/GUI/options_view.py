import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

import src.Services.settings as settings
import src.Services.style as style_cust
import constants as cta


class OptionsWindow:
    def __init__(self, queryViewRef, onCloseCallback=None):
        self.queryViewRef = queryViewRef
        self.root = tk.Toplevel(self.queryViewRef.root)
        self.root.title("Options")
        self.root.geometry("600x300")

        self.onCloseCallback = onCloseCallback

        self.settingsManager = settings.SettingsManager(
                                cta.DIR_SETTINGS_GENERAL, 
                                cta.DIR_SETTINGS_ACCOUNT,
                                cta.DIR_SETTINGS_QUERIES
                            )

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
        self.notebook.add(self.queriesTab, text="Queries/Logs")
        # self.notebook.add(self.analyticsTab, text="Analytics")


    
    def setupGeneraTabUI(self) -> None:
        self.generalSettingsTabContainer = ttk.Frame(self.generalTab, padding=16)
        self.generalSettingsTabContainer.pack(fill="both", expand=True)

        ttk.Label(
            self.generalSettingsTabContainer,
            text="Appearance",
            font=("Segoe UI", 10, "bold")
        ).grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 8))

        ttk.Label(self.generalSettingsTabContainer, text="Theme:").grid(row=1, column=0, sticky="w")

        themeVarString = "Dark" if self.settingsManager.getBgTheme() else "Light"
        self.theme_varTheme = tk.StringVar(value=themeVarString)

        self.theme_box = ttk.Combobox(
            self.generalSettingsTabContainer,
            textvariable=self.theme_varTheme,
            values=["Light", "Dark"],
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


    def setupAccountTabUI(self) -> None:
        self.accountSettingsTabContainer = ttk.Frame(self.accTab, padding=16)
        self.accountSettingsTabContainer.pack(fill="both", expand=True)

        ttk.Label(
            self.accountSettingsTabContainer,
            text="Account information",
            font=("Segoe UI", 10, "bold")
        ).grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 8))

        ttk.Label(self.accountSettingsTabContainer, text="Username:").grid(row=1, column=0, sticky="w")
        ttk.Label(self.accountSettingsTabContainer, text="Oracle username:").grid(row=2, column=0, sticky="w")
        ttk.Label(self.accountSettingsTabContainer, text="Oracle connection string:").grid(row=3, column=0, sticky="w")

        currentUsername = self.settingsManager.getAccUsername()
        self.usernameEntry = ttk.Entry(self.accountSettingsTabContainer, width=40)
        self.usernameEntry.grid(row=1, column=2, sticky="w")
        self.usernameEntry.insert(0, currentUsername)

        currentOracleCredentials = self.settingsManager.getCredentialsSettings()
        self.oracleUserEntry = ttk.Entry(self.accountSettingsTabContainer, width=40)
        self.oracleUserEntry.grid(row=2, column=2, sticky="w")
        self.oracleUserEntry.insert(0, currentOracleCredentials["oracleUsername"])
        
        self.oracleDSNEntry = ttk.Entry(self.accountSettingsTabContainer, width=40)
        self.oracleDSNEntry.grid(row=3, column=2, sticky="w")
        self.oracleDSNEntry.insert(0, currentOracleCredentials["connectionString"])

        ttk.Button(self.accountSettingsTabContainer, text="Apply", 
                   command=self.applyNewUsername).grid(row=40, column=4, sticky="w")
        
    
    
    def setupQueriesTabUI(self) -> None:
        self.queriesSettingsTabContainer = ttk.Frame(self.queriesTab, padding=16)
        self.queriesSettingsTabContainer.pack(fill="both", expand=True)

        ttk.Label(
            self.queriesSettingsTabContainer,
            text="Queries & Logs",
            font=("Segoe UI", 10, "bold")
        ).grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 8))

        ttk.Label(self.queriesSettingsTabContainer, text="Show logs:").grid(row=1, column=0, sticky="w")

        themeVarString = self.settingsManager.getLogsShownMode()
        self.theme_varLogs = tk.StringVar(value=themeVarString)
        self.themeBoxLogs = ttk.Combobox(
            self.queriesSettingsTabContainer,
            textvariable=self.theme_varLogs,
            values=["Daily", "All-time"],
            state="readonly",
            width=14
        )
        

        ttk.Button(self.queriesSettingsTabContainer, text="Apply", 
                   command=self.applyLogsShownMode).grid(row=20, column=6, sticky="w")


        self.themeBoxLogs.grid(row=1, column=1, sticky="ew", padx=(8, 0))
        self.themeBoxLogs.configure(font=("Segoe UI", 9))

        self.queriesSettingsTabContainer.rowconfigure(2, minsize=12)

        self.queriesSettingsTabContainer.columnconfigure(0, weight=1)
        self.queriesSettingsTabContainer.columnconfigure(1, weight=2)
    
    
    def setupAnalyticsTabUI(self) -> None:
        pass




    def applyTheme(self) -> None:
        selectedTheme = self.theme_box.get()
        self.settingsManager.editDarkTheme(selectedTheme)
        
        if selectedTheme == "Dark":
            style_cust.setQueryViewStyleDark(self.queryViewRef.root)
            style_cust.setAnalyticsViewStyleDark(self.queryViewRef.analyticsPage)
        else:
            style_cust.setQueryViewStyle(self.queryViewRef.root)
            style_cust.setAnalyticsViewStyle(self.queryViewRef.analyticsPage)



    def applyNewUsername(self) -> None:
        usernameEntryValue = self.usernameEntry.get()

        if len(usernameEntryValue) >= 1 and len(usernameEntryValue) <= 30:
            self.settingsManager.editUsername(usernameEntryValue)
        else:
            messagebox.showinfo("Invalid username", "Username must be between 1 and 30 characters")

        self.usernameEntry.delete(0, tk.END)
        self.usernameEntry.insert(0, usernameEntryValue) 

        oracleUserEntryValue = self.oracleUserEntry.get()
        oracleDSNEntryValue = self.oracleDSNEntry.get()

        if len(oracleUserEntryValue) >= 1 and len(oracleDSNEntryValue) >= 1:
            self.settingsManager.editCredentialsOptions(oracleUserEntryValue, oracleDSNEntryValue)
        else:
            messagebox.showinfo("Invalid username(s)", "Username(s) must be above 1 character.")

        self.oracleUserEntry.delete(0, tk.END)
        self.oracleUserEntry.insert(0, oracleUserEntryValue)
        self.oracleDSNEntry.delete(0, tk.END)
        self.oracleDSNEntry.insert(0, oracleDSNEntryValue)



    def applyLogsShownMode(self) -> None :
        selectedLogsMode = self.themeBoxLogs.get()

        self.settingsManager.editLogsShownMode(selectedLogsMode)

        self.queryViewRef.displayLogsText()



