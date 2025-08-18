import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

import sv_ttk

import src.Services.db_connection as cnx
import src.Services.settings as settings
import src.Services.style as style_cust
import src.GUI.query_view as qryview
import constants as cta


class MainWindow:
    def __init__(self):
        self.oracleConnector = cnx.OracleConnector()
        self.settingsManager = settings.SettingsManager(cta.DIR_SETTINGS_GENERAL, cta.DIR_SETTINGS_ACCOUNT)

        self.root = tk.Tk()
        self.root.title(cta.APP_TITLE)
        self.root.geometry("800x700")
        
        self.style = style_cust.setMainViewStyle(self.root)
        self.setupMainUI()

        self.loadSavedCredentialsToUI()

        print(f"MAIN WINDOW CREATED\n")

        self.root.mainloop()


    def setupMainUI(self) -> None:
        # isDark = self.settingsManager.getBgTheme()
        # if isDark : sv_ttk.set_theme("dark") 

        # self.root.configure(bg="#F0F0F0")

        self.mainFrame = ttk.Frame(self.root, padding=(60, 30), style="Main.TFrame")
        self.mainFrame.pack(expand=True)

        titleLabel = tk.Label(self.mainFrame, text="Oracle DB Login", font=("Arial", 16, "bold"), bg="#ffffff")
        titleLabel.pack(pady=(0, 20))

        tk.Label(self.mainFrame, text="Username:", font=("Arial", 12), bg="#ffffff").pack(pady=(0, 5))
        self.usernameEntry = tk.Entry(self.mainFrame, font=("Arial", 12), width=30, relief="solid", bd=1)
        self.usernameEntry.pack(pady=5, ipady=4)
        
        tk.Label(self.mainFrame, text="Connection string:", font=("Arial", 12), bg="#ffffff").pack(pady=(0, 5))
        self.connectionStringEntry = tk.Entry(self.mainFrame, font=("Arial", 12), width=30, relief="solid", bd=1)
        self.connectionStringEntry.pack(pady=5, ipady=4)

        tk.Label(self.mainFrame, text="Password:", font=("Arial", 12), bg="#ffffff").pack(pady=(0, 5))

        self.pswEntry = tk.Entry(self.mainFrame, show="*", font=("Arial", 12), width=30, relief="solid", bd=1)
        self.pswEntry.pack(pady=5, ipady=4)

        connectBtn = tk.Button(self.mainFrame, text="Connect", font=("Arial", 12, "bold"), bg="#4CAF50", fg="white", cursor="hand2",
                                activebackground="#45A049", padx=10, pady=5, command=self.handleConnection)
        connectBtn.pack(pady=20)        
        
        self.connectionStatusLabel = tk.Label(self.mainFrame, text="", font=("Arial", 10), bg="#ffffff")
        self.connectionStatusLabel.pack(pady=10)

        self.checkboxVar = tk.IntVar(value=(1 if self.settingsManager.checkboxVarSettings else 0))

        self.checkbox = tk.Checkbutton(self.mainFrame, 
                                       text="Save credentials", 
                                       variable=self.checkboxVar, 
                                       onvalue=1, 
                                       offvalue=0,    
                                       cursor="hand2"                                    
                                    )
        self.checkbox.config(bg="lightgrey", fg="blue", font=("Arial", 12), 
                   relief="raised", padx=10, pady=5)
        self.checkbox.pack(padx=40, pady=40)

        self.version_label = tk.Label(self.mainFrame, text=f"{cta.APP_TITLE} v1.3.1", anchor="e", bg="#ffffff")
        self.version_label.pack(side="bottom", fill="x")

        self.menubar = tk.Menu(self.root)
        self.helpManu = tk.Menu(self.menubar, tearoff=0)
        self.helpManu.add_command(label="About", command=self.show_about_dialog)
        self.menubar.add_cascade(label="Help", menu=self.helpManu)
        self.root.config(menu=self.menubar)

        
    def handleConnection(self) -> None:
        username = self.usernameEntry.get()
        connectionString = self.connectionStringEntry.get()
        password = self.pswEntry.get()

        isSuccessful = self.oracleConnector.connectToOracle(username, connectionString, password)

        print(self.oracleConnector.connection)
        print(self.oracleConnector.cursor)

        self.showStatus(isSuccessful)

        if isSuccessful:            
            self.handleSaveSettingsCheckbox()
            self.root.update_idletasks()
            self.root.after(1000, self.clearRoot())   
            self.accessQueryView()

        

    def showStatus(self, success: bool) -> None:
        if success:
            self.connectionStatusLabel.config(text=cta.DB_CONNECTION_SUCCESS, fg="green")  
        else:
            self.connectionStatusLabel.config(text=cta.DB_CONNECTION_ERROR, fg="red")  

        self.connectionStatusLabel.update()


    def clearRoot(self) -> None:
        for widget in self.root.winfo_children():
            widget.destroy()        

    
    def accessQueryView(self) -> None:
        self.queryView = qryview.QueryView(self.root, self.oracleConnector)
        self.root.state('zoomed') 

    
    def handleSaveSettingsCheckbox(self) -> None:
        if self.checkboxVar.get() == 1:
            username = self.usernameEntry.get()
            connectionString = self.connectionStringEntry.get()
            password = self.pswEntry.get()
            signInFlag = True

            self.settingsManager.editSignInSettings(username, connectionString, password, signInFlag)
        else:
            self.settingsManager.editSignInSettings("", "", "", False)


    def loadSavedCredentialsToUI(self) -> None:
        value = self.settingsManager.checkboxVarSettings
        credentials = self.settingsManager.credentialsSettings

        if value == 1:
            self.usernameEntry.insert(0, credentials["username"])
            self.connectionStringEntry.insert(0, credentials["connectionString"])
            # self.pswEntry.insert(0, credentials["pwd"])


    def show_about_dialog(self) -> None:
        about_text = (
            "SQL Companion v1.3.1\n\n"
            "Built by Gabriel Louka\n"
            "This software helps you connect to Oracle DBs,\n"
            "run queries, view stats, and analyze performance.\n\n"
            # "© 2025 Gabriel Louka. All rights reserved."
        )
        messagebox.showinfo("About SQL Companion", about_text)

        