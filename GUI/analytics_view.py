import tkinter as tk

class AnalyticsView:
    def __init__(self, root):
        self.root = tk.Toplevel(root)
        self.root.title("Queries analytics")
        self.root.geometry("1000x700")

        self.setupUI()

        print(F"ANALYTICS WINDOW CREATED")

        

    def setupUI(self):
        self.mainFrame = tk.Frame(self.root, padx=30, pady=30, bg="#f7f7f7")
        self.mainFrame.pack(expand=True)
        
        self.root.mainloop()