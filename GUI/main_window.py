import tkinter as tk

import Services.db_connection as cnx
import GUI.query_view as qryview
import constants as cta


class MainWindow:
    def __init__(self):
        self.oracleConnector = cnx.OracleConnector()

        self.root = tk.Tk()
        self.root.title(cta.APP_TITLE)
        self.root.geometry("800x600")
        
        self.setupMainUI()

        print(f"MAIN WINDOW CREATED\n")

        self.root.mainloop()


    def setupMainUI(self) -> None:
        self.mainFrame = tk.Frame(self.root, padx=30, pady=30, bg="#f7f7f7")
        self.mainFrame.pack(expand=True)

        titleLabel = tk.Label(self.mainFrame, text="Oracle DB Login", font=("Arial", 16, "bold"), bg="#f7f7f7")
        titleLabel.pack(pady=(0, 20))

        tk.Label(self.mainFrame, text="Enter Oracle DB Password:", font=("Arial", 12), bg="#f7f7f7").pack(pady=(0, 5))

        self.pswEntry = tk.Entry(self.mainFrame, show="*", font=("Arial", 12), width=30, relief="solid", bd=1)
        self.pswEntry.pack(pady=5, ipady=4)

        connectBtn = tk.Button(self.mainFrame, text="Connect", font=("Arial", 12, "bold"), bg="#4CAF50", fg="white",
                                activebackground="#45A049", padx=10, pady=5, command=self.handleConnection)
        connectBtn.pack(pady=20)        
        
        self.connectionStatusLabel = tk.Label(self.mainFrame, text="", font=("Arial", 10), bg="#f7f7f7")
        self.connectionStatusLabel.pack(pady=10)

        
    def handleConnection(self) -> None:
        password = self.pswEntry.get()
        isSuccessful = self.oracleConnector.connectToOracle(password)

        print(self.oracleConnector.connection)
        print(self.oracleConnector.cursor)

        self.showStatus(isSuccessful)

        if isSuccessful:            
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