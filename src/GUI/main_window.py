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
        self.settingsManager = settings.SettingsManager(
                                cta.DIR_SETTINGS_GENERAL, 
                                cta.DIR_SETTINGS_ACCOUNT,
                                cta.DIR_SETTINGS_QUERIES
                            )

        self.root = tk.Tk()
        self.root.title(cta.APP_TITLE)
        self.root.geometry("800x700")
        
        self.setupMainUI()

        self.loadSavedCredentialsToUI()

        print(f"MAIN WINDOW CREATED\n")

        self.root.mainloop()


    def setupMainUI(self) -> None:
        isDark = self.settingsManager.getBgTheme()
        if isDark : 
            self.style = style_cust.setMainViewStyleDark(self.root) 
        else : 
            self.style = style_cust.setMainViewStyle(self.root)

        self.mainFrame = ttk.Frame(self.root, padding=(60, 30), style="MainLogin.TFrame")
        self.mainFrame.pack(expand=True)

        titleLabel = ttk.Label(self.mainFrame, text="Oracle DB Login", style="MainTitle.TLabel")
        titleLabel.pack(pady=(0, 20))

        ttk.Label(self.mainFrame, text="Username:", style="MainLabel.TLabel").pack(pady=(0, 5))
        self.usernameEntry = tk.Entry(self.mainFrame, font=("Arial", 12), width=30, relief="solid", bd=1)
        self.usernameEntry.pack(pady=5, ipady=4)
        
        ttk.Label(self.mainFrame, text="Connection string:", style="MainLabel.TLabel").pack(pady=(0, 5))
        self.connectionStringEntry = tk.Entry(self.mainFrame, font=("Arial", 12), width=30, relief="solid", bd=1)
        self.connectionStringEntry.pack(pady=5, ipady=4)

        ttk.Label(self.mainFrame, text="Password:", style="MainLabel.TLabel").pack(pady=(0, 5))

        self.pswEntry = tk.Entry(self.mainFrame, show="*", font=("Arial", 12), width=30, relief="solid", bd=1)
        self.pswEntry.pack(pady=5, ipady=4)

        self.connectBtn = ttk.Button(self.mainFrame, text="Connect", cursor="hand2", style="MainConnect.TButton", command=self.handleConnection)
        self.connectBtn.pack(pady=20)  

        self.connectionStatusLabel = ttk.Label(self.mainFrame, text="", style="MainConectionLabel.TLabel")  
        self.connectionStatusLabel.pack(pady=10)            

        self.checkboxVar = tk.IntVar(value=(1 if self.settingsManager.getSignInFlag() else 0))

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

        self.version_label = ttk.Label(self.mainFrame, text=f"{cta.APP_TITLE} v1.4.0", anchor="e", style="MainVersionLabel.TLabel")
        self.version_label.pack(side="bottom", fill="x")

        self.menubar = tk.Menu(self.root)
        self.helpManu = tk.Menu(self.menubar, tearoff=0)
        self.helpManu.add_command(label="About", command=self.show_about_dialog)
        self.menubar.add_cascade(label="Help", menu=self.helpManu)
        self.root.config(menu=self.menubar)

        
    def handleConnection(self) -> None:
        self.connectBtn.config(state="disabled")

        username = self.usernameEntry.get()
        connectionString = self.connectionStringEntry.get()
        password = self.pswEntry.get()

        isSuccessful = self.oracleConnector.connectToOracle(username, connectionString, password)
        print(isSuccessful)

        print(self.oracleConnector.connection)
        print(self.oracleConnector.cursor)

        self.showStatus(isSuccessful)

        if isSuccessful:            
            self.handleSaveSettingsCheckbox()
            self.root.update_idletasks()
            self.root.after(1000, self.clearRoot())   
            self.accessQueryView()
        else:
            self.connectBtn.config(state="normal")

        

    def showStatus(self, success: bool) -> None:
        self.connectionStatusLabel.pack(pady=10)   
         
        if success:
            self.connectionStatusLabel.configure(text=cta.DB_CONNECTION_SUCCESS, style="MainConectionLabelSuccess.TLabel")
        else:
            self.connectionStatusLabel.configure(text=cta.DB_CONNECTION_ERROR, style="MainConectionLabelFail.TLabel")

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
            signInFlag = True

            self.settingsManager.editSignInSettings(username, connectionString, signInFlag)
        else:
            self.settingsManager.editSignInSettings("", "", False)


    def loadSavedCredentialsToUI(self) -> None:
        value = self.settingsManager.getSignInFlag()
        credentials = self.settingsManager.getCredentialsSettings()

        if value:
            self.usernameEntry.insert(0, credentials["oracleUsername"])
            self.connectionStringEntry.insert(0, credentials["connectionString"])


    def show_about_dialog(self) -> None:
        about_text = (
            "SQL Companion v1.4.0\n\n"
            "Built by Gabriel Louka\n"
            "This software helps you connect to Oracle DBs,\n"
            "run queries, view stats, and analyze performance.\n\n"
        )
        messagebox.showinfo("About SQL Companion", about_text)

        